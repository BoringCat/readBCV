from utils import createLogger, GetCVAsync
from asyncio import Event as Lock, get_event_loop, sleep, get_event_loop
import websockets
from json import dumps, loads
from config import envconfig
from utils import getCVid
from db import CacheDB as db

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
    econf = envconfig
    glo_path = econf.get('APP_PATH', '/')
    lock = Lock(loop=get_event_loop())
    getcv = GetCVAsync(fatherlog)
    fatherlog.debug('path = %s' % path)
    if path != glo_path:
        await websocket.close(1001, "Path error")
        return
    async def callback(status, cvid, msg, loop):
        if status:
            db.Cache(cvid, msg)
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
    cache = db.getCache(getCVid(url))
    if cache:
        lock.set()
        await websocket.send(response(status=True, imgs=cache, fromcache=True))
        await websocket.close()
        return
    status, msg = getcv.Get(url, websocket.request_headers, callback, get_event_loop())
    if not status:
        await (websocket.close(1001, "服务器限制") if msg == 'Full' else websocket.close(1001, "内部错误"))
        return
    fatherlog.debug('WaitLock!')
    await lock.wait()
    fatherlog.debug('UnLock!')
    await websocket.close()