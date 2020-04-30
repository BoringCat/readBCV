from utils import createLogger, GetCVAsync
from asyncio import Event as Lock, get_event_loop, sleep, get_event_loop
import websockets
from json import dumps, loads
from config import envconfig

def disconnect(msg):
    return dumps({
        'action': "disconnect",
        'msg': msg
    },ensure_ascii=False,separators=(',',':'))

def response(**msg):
    b = {'action': "response"}
    b.update(msg)
    return dumps(b,ensure_ascii=False,separators=(',',':'))

async def readbcv(websocket:websockets.server.WebSocketServerProtocol, path):
    fatherlog = createLogger('readbcv_ws')
    econf = envconfig()
    glo_path = econf.get('WebSocket_Path', '/')
    lock = Lock(loop=get_event_loop())
    getcv = GetCVAsync(fatherlog)
    fatherlog.debug('path = %s' % path)
    if path != glo_path:
        await websocket.close_connection()
        return
    async def unlock():
        lock.set()
    async def callback(status, msg, loop):
        if status:
            await websocket.send(response(status=True, imgs=msg))
        else:
            if msg:
                errmsg = '服务器返回%d' % msg.status_code
                await websocket.send(response(status = False, errmsg = errmsg))
            else:
                await websocket.send(response(status = False, errmsg = '内部错误'))
        lock.set()
        fatherlog.getChild('callback.lock.is_set').debug(lock.is_set())
        fatherlog.getChild('callback').debug('UnLock!')

    try:
        postdict = loads(await websocket.recv())
    except Exception:
        await websocket.send(disconnect('出错'))
        await websocket.close(1001, "error")
        return
    url = postdict.get('BCVURL', None)
    if not url:
        await websocket.send(disconnect('出错'))
        await websocket.close(1001, "error")
    getcv.Get(url, websocket.request_headers, callback, get_event_loop())
    fatherlog.debug('WaitLock!')
    await lock.wait()
    fatherlog.debug('UnLock!')
    await websocket.close()