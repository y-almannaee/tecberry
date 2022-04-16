from sys import path_hooks
import socketio
from redis import asyncio as aioredis
from aiohttp import web
import asyncio, importlib.util, pathlib

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


async def make():
	app = web.Application()

	for path in pathlib.Path("/var/lib/peltier_controller/authenticators").iterdir():
		if path.suffix != ".py":
			continue
		spec = importlib.util.spec_from_file_location(path.name, path)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		try:
			app.add_routes(mod.EXPORTED.routes)
			print(f"Added routes from {path.name}: {*mod.EXPORTED.routes,}")
		except AttributeError:
			print(
				f"Unable to add routes from {path.name}, module does not export routes"
			)

	app.add_routes(routes)
	sio.attach(app)
	redis = await aioredis.Redis()
	app["db"] = redis
	return app


if __name__ == "__main__":
	web.run_app(make(), port=3636)
