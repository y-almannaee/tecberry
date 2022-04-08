import socketio
from aiohttp import web 
import asyncio

## SOCKETIO ENTRYPOINTS
sio = socketio.AsyncServer(async_mode="aiohttp")

@sio.event
async def connect(sid, environ, auth):
	print('[SIO] Connection by ', sid)

@sio.event
async def disconnect(sid):
	print('[SIO] Disconnection by ', sid)

@sio.on('editing')
async def handle_editing(sid, data):
	pass

## AIOHTTP ENTRYPOINTS
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
	return web.Response(text="OK")

@routes.get('/authorized')
async def get_scope(request):
	print(request.headers)
	return web.Response(status=204)

app = web.Application()
app.add_routes(routes)
sio.attach(app)

if __name__ == "__main__":
	web.run_app(app,port=3636)