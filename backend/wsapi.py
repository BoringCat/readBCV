from utils import createLogger, GetCVAsync
from asyncio import Event as Lock, get_event_loop, sleep, get_event_loop
import websockets
from json import dumps, loads
from config import envconfig
from utils import getCVid

fatherlog = createLogger('ReadBCV')
getcv = GetCVAsync(fatherlog)

def disconnect(msg):
    '''WebSocket格式化断开信息

    args:
      - msg: 信息
    '''
    return dumps({
        'action': "disconnect",
        'msg': msg
    },ensure_ascii=False,separators=(',',':'))

def response(**msg):
    '''WebSocket格式化返回信息

    args:
      - **msg: 信息键值对
    '''
    b = {'action': "response"}
    b.update(msg)
    return dumps(b,ensure_ascii=False,separators=(',',':'))

async def readbcv(websocket:websockets.server.WebSocketServerProtocol, path):
    '''WebSocket处理函数

    kwargs:
      - websocket: websocket对象
      - path: 连接的路径
    '''
    global fatherlog, getcv
    logger = fatherlog.getChild('ws')
    econf = envconfig
    glo_path = econf.get('APP_PATH', '/')
    lock = Lock(loop=get_event_loop())
    logger.debug('path = %s' % path)
    if path != glo_path:
        await websocket.close(1001, "Path error")
        return
    async def callback(status, msg, fromcache = False):
        '''回调函数

        kwargs:
          - status: 回调过来的状态
          - cvid: cv的ID
          - msg: 要返回的信息（包括错误信息）
        '''
        if status:                  # 如果分析正常
            await websocket.send(response(status=True, imgs=msg, fromcache=fromcache))
        else:                       # 分析失败
            if msg:                 # B站返回状态码
                errmsg = '服务器返回%d' % msg.status_code
                await websocket.send(response(status = False, errmsg = errmsg))
            else:                   # 其他错误
                await websocket.send(response(status = False, errmsg = '内部错误'))
        lock.set()                  # 解除阻塞
        logger.getChild('callback').debug('UnLock!')

    try:                            # 尝试获取请求内容
        postdict = loads(await websocket.recv())
    except Exception:
        await websocket.send(disconnect('出错'))
        await websocket.close(1001, "error")
        return
    url = postdict.get('BURL', None)
    if not url:
        await websocket.send(disconnect('出错'))
        await websocket.close(1001, "error")
    status, msg = getcv.Get(url, websocket.request_headers, callback, get_event_loop()) # 提交任务到队列
    logger.debug('Status: %s, msg: %s' % (status, msg))
    if not status:                      # 提交失败（一般是被DOS或爬，导致队列已满）（或者代码出错:(）
        await (websocket.close(1001, "服务器限制") if msg == 'Full' else websocket.close(1001, "内部错误"))
        return
    logger.debug('WaitLock!')
    await lock.wait()                   # 阻塞，等待回调
    logger.debug('UnLock!')
    await websocket.close()             # 信息在回调处发送，这里直接关闭链接