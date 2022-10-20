from sys import path_hooks
import socketio
from redis import asyncio as aioredis
from aiohttp import web
import asyncio, importlib.util, traceback, pathlib, os

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
async def hello(request):
	return web.Response(text="OK")


@routes.get("/authorized")
async def get_scope(request):
	print(request.headers)
	return web.Response(status=204)

@routes.get("/configuration")
async def get_config(request):
	# Get name, get list of auth
	res = {}
	res["authenticators"] = {}
	res["name"] = os.environ.get("NAME","TECBERRY.ML")
	for nmspc,module in request.app["authenticators"].items():
		res["authenticators"][nmspc] = module.routes[0].path
	res["version"] = 1
	return web.json_response(res)


async def make():
	app = web.Application()
	app["authenticators"] = {}

	for path in pathlib.Path(os.environ.get("AUTH_LOCATIONS","/var/lib/peltier_controller/authenticators")).iterdir():
		if path.suffix != ".py":
			continue
		spec = importlib.util.spec_from_file_location(path.name, path)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		try:
			app.add_routes(mod.routes)
			print(f"Added routes from {path.name}: {*mod.routes,}")
		except AttributeError as error:
			traceback.print_exc()
			print(
				f"Unable to add routes from {path.name}, module does not export routes"
			)
		try:
			app["authenticators"][mod.namespace] = mod
		except:
			traceback.print_exc()
			print("Module doesn't export namespace")

	app.add_routes(routes)
	sio.attach(app)
	redis = await aioredis.Redis(host=os.environ.get("REDIS_HOST","redis_db"), port=int(os.environ.get("REDIS_PORT",6379)))
	app["db"] = redis
	return app


if __name__ == "__main__":
	web.run_app(make(), port=3636)
