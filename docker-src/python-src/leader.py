from sys import path_hooks, stdout
import socketio, json
from redis import asyncio as aioredis
from loguru import logger
import gpio_interface
import logging
from redis import DataError
from aiohttp import web
import aiohttp_cors
import secrets
import asyncio, importlib.util, traceback, pathlib, os

ID_BYTES = 3

## SOCKETIO ENTRYPOINTS
sio = socketio.AsyncServer(async_mode="aiohttp")


@sio.event
async def connect(sid, environ, auth):
    print("[SIO] Connection by ", sid)


@sio.event
async def disconnect(sid):
    print("[SIO] Disconnection by ", sid)


@sio.on("editing")
async def handle_editing(sid, data):
    pass


## AIOHTTP ENTRYPOINTS
routes = web.RouteTableDef()


@routes.get("/")
@logger.catch
async def hello(request):
    return web.Response(text="OK")


@routes.get("/authorized")
@logger.catch
async def get_scope(request):
    logger.info(
        f"Got request for authorization with headers: {request.headers} and cookies: {request.cookies}"
    )
    return web.Response(status=204)


async def db_get_userdata(db, id):
    primary_key = await db.get(f"cookies:{id}")
    user_account = await db.hgetall(primary_key)
    # Below filters down on the incorrect implementations
    # of authenticators so that there is no info leakage
    user_account_limited = {
        "name": user_account["name"],
        "pfp": user_account["pfp"],
        "rank": user_account["rank"],
    }
    return user_account_limited


@routes.get("/whoami/{cookie}")
@logger.catch
async def get_user_info(request):
    try:
        # cookie = request.cookies["id"].split(":")[1]
        cookie = request.match_info["cookie"].split(":")[1]
    except KeyError:
        return web.json_response(status=400, data={"message": "No cookie"})
    try:
        userdata = await db_get_userdata(request.app["db"], cookie)
        return web.json_response(data=userdata)
    except DataError:
        return web.json_response(status=400, data={"message": "Not a user"})
    except KeyError:
        return web.json_response(status=400, data={"message": "User not well defined"})


@routes.get("/configuration")
@logger.catch
async def get_config(request):
    res = {}
    # Get name of website
    res["name"] = os.environ.get("NAME", "TECBERRY.ml")
    res["dnt"] = bool(os.environ.get("OPT_OUT_TELEMETRY", False))
    # Build list of authenticators for the login page
    res["authenticators"] = []
    for namespace, module in request.app["authenticators"].items():
        method = {}
        method["id"] = namespace
        method["text"] = module.button_text
        method["link"] = module.routes[0].path
        method["button_classes"] = module.button_classes_tailwindcss
        res["authenticators"].append(method)
    # Version number in case backend changes
    res["version"] = 1
    return web.json_response(res)


@routes.get("/monitor")
@logger.catch
async def monitor_progress(request):
    return web.json_response({"message": "OK", "running": request.app["running"]})

@routes.post("/monitor")
@logger.catch
async def start_progress(request):
    asyncio.create_task(gpio_interface.start_execution(request.app["running"],request.app["db"]))
    return web.json_response({"message": "OK", "running": request.app["running"]})

@routes.get("/logs")
@logger.catch
async def get_logs(request):
    return web.json_response({"message": "OK", "logs": gpio_interface.current_messages})


@routes.get("/scheduler")
@logger.catch
async def get_scheduler(request):
    try:
        execution_settings = await request.app["db"].hgetall('settings')
        return web.json_response(execution_settings)
    finally:
        pass


@routes.post("/scheduler")
@logger.catch
async def set_scheduler(request):
    try:
        data = await request.json()
        settings = data.get('settings')
        safe_data = {
            "device_exec_order": data.get("enabled", ""),
            "on_start_code": data.get("on_start_code", ""),
            "on_end_code": data.get("on_end_code", ""),
            "duration": int(settings.get("total_duration")),
            "offset": int(settings.get("offset")),
            "amplitude": int(settings.get("amplitude")),
            "phase_shift": int(settings.get("phase_shift")),
            "period": int(settings.get("period")),
        }
        request.app["running"]["settings"] = {
            "duration":safe_data["duration"],
            "offset": safe_data["offset"],
            "amplitude": safe_data["amplitude"],
            "phase_shift": safe_data["phase_shift"],
            "period": safe_data["period"],
            "on_start_code": safe_data.get("on_start_code",''),
            "on_end_code": safe_data.get("on_end_code",''),
            "device_exec_order": safe_data.get("device_exec_order",''),
        }
        ok = await request.app["db"].hset("settings",mapping=safe_data)
        return web.json_response({"message":"OK"})
    except json.JSONDecodeError:
        return web.json_response({"message": "Malformed request"}, status=400)
    except KeyError:
        return web.json_response({"message": "Missing arguments"}, status=400)


@routes.get("/devices")
@logger.catch
async def get_devices(request):
    try:
        list_of_devs = await request.app["db"].lrange("devs", 0, -1)
        async with request.app["db"].pipeline(transaction=True) as pipe:
            for definition in list_of_devs:
                pipe.hgetall(f"devs:{definition}")
            res = await (pipe.execute())
        for item in res:
            item["id"] = list_of_devs.pop(0)
            item["public"] = json.loads(item.get("public", "{}"))
            item["private"] = json.loads(item.get("private", "{}"))
        return web.json_response({"message": "OK", "devices": res}, status=200)
    except json.JSONDecodeError:
        return web.json_response({"message": "Malformed request"}, status=400)


@routes.post("/devices")
@logger.catch
async def set_device(request):
    try:
        data = await request.json()
        name = data["name"].replace(" ","_")
        generated_id = secrets.token_hex(ID_BYTES)
        id_exists = True
        while id_exists:
            test_exists = await request.app["db"].exists(f"devs:{generated_id}")
            if test_exists == 0:
                id_exists = False
            else:
                generated_id = secrets.token_hex(ID_BYTES)
        async with request.app["db"].pipeline(transaction=True) as pipe:
            ok = await (
                pipe.hset(f"devs:{generated_id}", key="name", value=name)
                .rpush(f"devs", generated_id)
                .execute()
            )
        if ok:
            return web.json_response({"message": "OK"}, status=200)
        else:
            return web.json_response({"message": "DB refused"}, status=500)
    except KeyError:
        return web.json_response({"message": "Name not specified"}, status=400)
    except json.JSONDecodeError:
        return web.json_response({"message": "Malformed request"}, status=400)


@routes.delete("/devices/{id}")
@logger.catch
async def delete_device(request):
    try:
        id = request.match_info["id"]
        async with request.app["db"].pipeline(transaction=True) as pipe:
            ok = await (pipe.delete(f"devs:{id}").lrem(f"devs", 1, id).execute())
        return web.json_response({"message": "OK"}, status=200)
    except KeyError:
        return web.json_response({"message": "ID not specified"}, status=400)


@routes.post("/devices/{id}")
@logger.catch
async def update_devices(request):
    try:
        id = request.match_info["id"]
        data = await request.json()
        try:
            public_vars = json.dumps(data.pop("public", {}))
            private_vars = json.dumps(data.pop("private", {}))
            data["public"] = public_vars
            data["private"] = private_vars
        except KeyError:
            return web.json_response({"message": "General failure"}, status=500)
        except TypeError:
            return web.json_response({"message": "Disallowed datatype"}, status=400)

        safe_data = {
            "public": data.get("public", ""),
            "private": data.get("private", ""),
            "definition": data.get("definition", "")
            if data.get("definition", "") != None
            and data.get("definition", "NOT_AN_ITEM") != None
            else "",
            "desc": data.get("desc", "No description"),
        }

        ok = await request.app["db"].hset(f"devs:{id}", mapping=safe_data)
        return web.json_response({"message": "OK"}, status=200)

    except KeyError:
        return web.json_response({"message": "ID not specified"}, status=400)
    except json.JSONDecodeError:
        return web.json_response({"message": "Malformed request"}, status=400)
    except DataError:
        return web.json_response({"message": "ID does not exist"}, status=400)


@routes.get("/definitions")
@logger.catch
async def get_definitions(request):
    try:
        list_of_defs = await request.app["db"].lrange("defs", 0, -1)
        async with request.app["db"].pipeline(transaction=True) as pipe:
            for definition in list_of_defs:
                pipe.hgetall(f"defs:{definition}")
            res = await (pipe.execute())
        for item in res:
            item["id"] = list_of_defs.pop(0)
        return web.json_response({"message": "OK", "definitions": res}, status=200)
    except json.JSONDecodeError:
        return web.json_response({"message": "Malformed request"}, status=400)


@routes.post("/definitions")
@logger.catch
async def set_definition(request):
    try:
        data = await request.json()
        name = data["name"].strip().replace(" ","_")
        generated_id = secrets.token_hex(ID_BYTES)
        id_exists = True
        while id_exists:
            test_exists = await request.app["db"].exists(f"defs:{generated_id}")
            if test_exists == 0:
                id_exists = False
            else:
                generated_id = secrets.token_hex(ID_BYTES)
        async with request.app["db"].pipeline(transaction=True) as pipe:
            ok = await (
                pipe.hset(f"defs:{generated_id}", key="name", value=name)
                .rpush(f"defs", generated_id)
                .execute()
            )
        if ok:
            return web.json_response({"message": "OK"}, status=200)
        else:
            return web.json_response({"message": "DB refused"}, status=500)
    except KeyError:
        return web.json_response({"message": "Name not specified"}, status=400)
    except json.JSONDecodeError:
        return web.json_response({"message": "Malformed request"}, status=400)


@routes.delete("/definitions/{id}")
@logger.catch
async def delete_definition(request):
    try:
        id = request.match_info["id"]
        async with request.app["db"].pipeline(transaction=True) as pipe:
            ok = await (pipe.delete(f"defs:{id}").lrem(f"defs", 1, id).execute())
        return web.json_response({"message": "OK"}, status=200)
    except KeyError:
        return web.json_response({"message": "ID not specified"}, status=400)


@routes.post("/definitions/{id}")
@logger.catch
async def update_definition(request):
    try:
        id = request.match_info["id"]
        data = await request.json()
        sanitize_list = lambda a: ",".join(
            set([x.strip().replace(" ", "_") for x in a.split(",")])
        )
        safe_data = {
            "public": sanitize_list(data.get("public", "")),
            "private": sanitize_list(data.get("private", "")),
            "code": data.get("code", ""),
            "desc": data.get("desc", "No description"),
        }
        ok = await request.app["db"].hset(f"defs:{id}", mapping=safe_data)
        return web.json_response({"message": "OK"}, status=200)
    except KeyError:
        return web.json_response({"message": "ID not specified"}, status=400)
    except json.JSONDecodeError:
        return web.json_response({"message": "Malformed request"}, status=400)
    except DataError:
        return web.json_response({"message": "ID does not exist"}, status=400)

@logger.catch
async def make():
    logger.remove()
    if os.environ.get("LOGGING_DEBUG", ""):
        severity = int(os.environ.get("LOGGING_DEBUG", ""))
        if severity < 10:
            logger.add(stdout,filter=lambda record: "special" not in record["extra"], level=severity, backtrace=True, diagnose=True)
        else:
            logger.add(stdout,filter=lambda record: "special" not in record["extra"], level=severity)
    else:
        logger.add(stdout,filter=lambda record: "special" not in record["extra"])
    logger.add(gpio_interface.log_special_messages, backtrace=True, filter=lambda record: "special" in record["extra"], format="{time:YYYY-MM-DD HH:mm:ss.SSS} ;|#| {file}:{line} ;|#| {message}")
    logger.info("Initialized logger")
    if os.environ.get("LOGGING_FILE", ""):
        logger.add(
            os.environ.get("LOGGING_FILE", ""), retention="3 days", rotation="500 KB",filter=lambda record: "special" not in record["extra"]
        )
    app = web.Application(logger=logger)

    app["authenticators"] = {}

    for path in pathlib.Path(
        os.environ.get("AUTH_LOCATIONS", "/var/lib/peltier_controller/authenticators")
    ).iterdir():
        if path.suffix != ".py":
            continue
        spec = importlib.util.spec_from_file_location(path.name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            app.add_routes(mod.routes)
            logger.info(
                f"Added routes from {path.name}: {[ f'{route.method} {route.path}' for route in mod.routes]}"
            )
        except AttributeError as error:
            logger.error(
                f"Unable to add routes from {path.name}, module does not export routes:\n {traceback.format_exc()}"
            )
        try:
            app["authenticators"][mod.namespace] = mod
        except:
            logger.error(f"Module doesn't export namespace:\n {traceback.format_exc()}")

    app.add_routes(routes)
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
    for route in list(app.router.routes()):
        cors.add(route)
    sio.attach(app)
    redis = await aioredis.Redis(
        host=os.environ.get("REDIS_HOST", "redis_db"),
        port=int(os.environ.get("REDIS_PORT", 6379)),
        decode_responses=True,
    )
    await redis.ping()
    app["db"] = redis
    execution_settings = await redis.hgetall('settings')
    app["running"] = {
        "running": False,
        "time_elapsed": 0,
        "devices": {},
        "settings": {},
    }
    app["running"]["settings"] = {
            "duration":int(execution_settings.get("duration",300)),
            "offset": int(execution_settings.get("offset",25)),
            "amplitude": int(execution_settings.get("amplitude",55)),
            "phase_shift": int(execution_settings.get("phase_shift",0)),
            "period": int(execution_settings.get("period",150)),
            "on_start_code": execution_settings.get("on_start_code",''),
            "on_end_code": execution_settings.get("on_end_code",''),
            "device_exec_order": execution_settings.get("device_exec_order",''),
        }
    return app


if __name__ == "__main__":
    web.run_app(make(), port=3636, access_log=logger)
