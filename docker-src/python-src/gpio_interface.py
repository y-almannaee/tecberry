from loguru import logger
import traceback
import copy
import json
import asyncio
import helpers
import math
from datetime import datetime
from RestrictedPython import (
    compile_restricted,
    safe_builtins,
    limited_builtins,
)

current_messages = []


def log_special_messages(message):
    current_messages.insert(0, message)


exposed_functions_and_vars = {
    "sleep": asyncio.sleep,
    "math": math,
    "print": logger.bind(special=True).opt(depth=1).info,
    "mail": None,  # NOT IMPLEMENTED
    "string_to_addr": helpers.convert_str_to_addr,
    "string_to_pin": helpers.convert_str_to_pin,
    "average": helpers.calculate_list_average,
}


@logger.catch
async def start_execution(state: dict, database) -> None:
    """state = {"running": False,
    "time_elapsed": 0,
    "devices": {},
    "settings": {},}

    devices = {
            id_number: name, desc, definition(idstring), public(json), private(json)
        }

    settings = {
            duration: int, period: int, amp: int, offset: int, phase_shift: int,
            device_exec_order: string[],
            on_start_code: string,
            on_end_code: string,
        }"""
    list_of_devs = await database.lrange("devs", 0, -1)
    broad_definition_vars = helpers.create_dot_dict({})
    devices_exposed = helpers.create_dot_dict({})
    async with database.pipeline(transaction=True) as pipe:
        for dev in list_of_devs:
            pipe.hgetall(f"devs:{dev}")
        res = await (pipe.execute())
    for item in res:
        item["id"] = list_of_devs.pop(0)
        if item["id"] not in state["settings"]["device_exec_order"]:
            continue
        item["public"] = json.loads(item.get("public", "{}"))
        item["private"] = json.loads(item.get("private", "{}"))
        item["definition_id"] = item.get("definition", "")
        item["definition"] = await database.hgetall(f"defs:{item.get('definition','')}")
        state["devices"][item["id"]] = item
    last_state = copy.deepcopy(state)
    if not state["running"]:
        state["running"] = True
        state["time_elapsed"] = 0
        if state["settings"].get("on_start_code", ""):
            result_start = await aexec(
                state["settings"].get("on_start_code", ""),
                "<start code>",
                {
                    "__builtins__": {**safe_builtins, **limited_builtins, "__import__": helpers.safe_import},
                    **exposed_functions_and_vars,
                    "Devices": devices_exposed,
                },
            )
            logger.debug(result_start)
    offset = state["settings"].get("offset")
    amplitude = state["settings"].get("amplitude")
    phase_shift = state["settings"].get("phase_shift")
    duration = state["settings"].get("duration")
    period = state["settings"].get("period")
    order = state["settings"].get("device_exec_order").split(",")
    start_time = datetime.now()
    while state["time_elapsed"] < duration * 60:
        x = (datetime.now() - start_time).total_seconds()
        state["time_elapsed"] = x
        td = offset + amplitude * math.sin(
            (math.pi * 2 * (x / 60 + phase_shift)) / period
        )
        for id in order:
            dev = state["devices"][id]
            logger.bind(special=True).opt(depth=1).info(
                f"Currently executing device #{id} for desired temperature of {td:.2f} celsius"
            )
            if dev["definition"]:
                devices_exposed_local = copy.deepcopy(state["devices"])
                devices_exposed_local.pop(f"{id}")
                for key,value in devices_exposed_local.items():
                    devices_exposed_local[key].pop("private")
                broad_definition_vars = helpers.create_dot_dict({})
                for device,device_dict in devices_exposed_local.items():
                    if device_dict.get("definition_id","") and device_dict.get("definition_id","") not in broad_definition_vars:
                        broad_definition_vars[device_dict.get("definition_id")] = helpers.create_dot_dict(
                            {}
                        )
                    for key, value in device_dict.get("public",{}).items():
                        if key not in broad_definition_vars[device_dict.get("definition_id")]:
                            broad_definition_vars[device_dict.get("definition_id")][key] = [value]
                        else:
                            broad_definition_vars[device_dict.get("definition_id")][key].append(value)
                provided_globals = {
                    "__builtins__": {**safe_builtins, **limited_builtins, "__import__": helpers.safe_import},
                    **exposed_functions_and_vars,
                    "secret_c0f6g9": f"<device {dev['name']}#{dev['id']}>",
                    "Devices": devices_exposed_local,
                    "Definitions": broad_definition_vars,
                    "Scheduler": helpers.create_dot_dict(
                        {
                            "temperature_desired": td,
                            "time_elapsed": x,
                        }
                    ),
                    "Self": helpers.create_dot_dict(
                        {
                            "Public": helpers.create_dot_dict(dev["public"]),
                            "Private": helpers.create_dot_dict(dev["private"]),
                        }
                    ),
                }
                result_dev = await aexec(
                    dev["definition"].get("code", ""),
                    f"<device {dev['name']}#{dev['id']}>",
                    provided_globals,
                )
                for device, dictionary in provided_globals["Devices"].items():
                    state["devices"][device.split("_")[-1]]["public"] = dictionary.get(
                        "public", {}
                    )
                    public_vars = json.dumps(dictionary.get("public", {}))
                    await database.hset(f"devs:{id}", "public", public_vars)
                state["devices"][id]["public"] = provided_globals["Self"]["Public"]
                public_vars = json.dumps(provided_globals["Self"].get("Public", {}))
                state["devices"][id]["private"] = provided_globals["Self"]["Private"]
                private_vars = json.dumps(provided_globals["Self"].get("Private", {}))
                await database.hset(
                    f"devs:{id}",
                    mapping={"public": public_vars, "private": private_vars},
                )
            else:
                logger.bind(special=True).opt(depth=1).info(f"Device {id} doesn't export definition")
        await asyncio.sleep(5)
        logger.debug(state["devices"])
    else:
        state["running"] = False
        state["time_elapsed"] = duration
        if state["settings"].get("on_end_code", ""):
            result_end = await aexec(
                state["settings"].get("on_end_code", ""),
                "<end code>",
                {
                    "__builtins__": {**safe_builtins, **limited_builtins, "__import__": helpers.safe_import},
                    **exposed_functions_and_vars,
                    "Devices": devices_exposed,
                },
            )
            logger.debug(result_end)
        logger.bind(special=True).opt(depth=1).info("DONE")


@logger.catch
async def aexec(code, filename, globals_dict):
    # Don't clutter locals
    locs = {}
    # Restore globals later
    globs = globals().copy()
    try:
        # bytecode = compile_restricted(f"async def func():\n    " + code.replace("\n", "\n    "), filename=filename, mode="exec")
        bytecode = compile(
            f"async def func():\n    " + code.replace("\n", "\n    "),
            filename=filename,
            mode="exec",
        )
    except SyntaxError:
        result = "No result"
        logger.bind(special=True).opt(depth=1).exception(f"Syntax error in user written code <{filename}>")
    try:
        exec(bytecode, globals_dict, locs)
        # Don't expect it to return from the coro.
        result = await locs["func"]()
        logger.debug(f"Function {filename} returned with result {result}")
    except BaseException:
        result = "No result"
        logger.bind(special=True).opt(depth=1).exception(f"General error in user executed code <{filename}>")
    try:
        globals().clear()
        # Inconsistent state
    finally:
        globals().update(**globs)
    return result, locs
