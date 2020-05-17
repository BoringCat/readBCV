import logging
from config import envconfig
from bs4 import BeautifulSoup
import asyncio
from threading import Thread
from queue import Queue, Empty, Full
from config import envconfig
from requests import session

_isinit = False

__all__ = [ 'createLogger', 'setLogLevel', 'GetCVAsync' ]

def createLogger(name):
    '''创建一个Logger对象。用于格式化日志输出

      args:
        - name: 根对象命名
    '''
    if not _isinit: _init_logconfig()
    return logging.getLogger(name)

# 初始化Logger
def _init_logconfig():
    '''创建一个Logger对象。用于格式化日志输出

    **你不应该在外部调用它！**
    '''
    # 检查日志输出等级，VIEW: 输出到info级、DEBUG: 输出到DEBUG级（覆盖VIEW）
    view = envconfig.get('VIEW', False)
    debug = envconfig.get('DEBUG', False)
    logconfig = {
        'level': logging.DEBUG if debug else logging.INFO if view else logging.WARN,
        'format': "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s",
        'datefmt': "%Y-%m-%d %H:%M:%S"
    }
    logging.basicConfig(**logconfig)
    _isinit = True

# 设置日志输出等级，用于取消某些包的DEBUG输出
def setLogLevel(name, level):
    '''设置日志输出等级，可以用于取消某些包的DEBUG输出

    **你不应该在外部调用它！**

      args:
        - name: 对象日志命名
        - level: logger的等级
    '''
    logging.getLogger(name).setLevel(level)

def start_loop(loop:asyncio.BaseEventLoop):
    '启动asyncio循环'
    loop.run_forever()

def readCV(webtext, isBV = False):
    '''分析图片们

    **你不应该在外部调用它！**

    args:
      - webtext: 页面HTML文本
    '''
    bs = BeautifulSoup(webtext, features="html.parser")
    if isBV:
        haveHead = bs.find('meta', {'property': "og:image"})    # 获取封面
        head_img = haveHead.attrs.get('content') if haveHead else None
        return { 'header': head_img, 'contents': [] }
    haveHead = bs.find('meta', {'data-hid': "og:image"})    # 获取封面
    head_img = haveHead.attrs.get('content') if haveHead else None
    imgs = list(filter(                                     # 过滤分割图片（`cut-off-\d+`）
        lambda x:'cut-off' not in ('\n'.join(x.attrs.get('class',[]))),
        bs.find('div','article-holder').find_all('img')
    ))
    ulist = []
    for img in imgs:
        data_src = img.attrs.get('data-src')
        if not data_src:
            continue
        raw_src = '@'.join(data_src.split('@')[:-1]) if '@' in data_src else data_src
        figcaptions = img.parent('figcaption')
        if figcaptions:
            ulist.append({'url': raw_src, 'figcaption': '\n'.join(map(lambda x:x.text,figcaptions))})
        else:
            ulist.append({'url': raw_src})
    return { 
        'header': head_img,
        'contents': ulist
    }

def getCVid(url):
    '''获取CV的ID

    **你不应该在外部调用它！**

    args:
      - url: CV的URL
    
    return:
      - bool: 是否为BV
      - id
    '''
    id = url.split('/')[-1]
    return id.lower().startswith('bv'), id

class GetCVAsync():
    '''异步获取CV图片类
    kwargs:
      - fatherlog: logger对象
    
    funcs:
      - Get(url, reqheader, callback, loop)
    '''
    def __init__(self, fatherlog):
        self._log = fatherlog.getChild('GetCVAsync')
        self._econf = envconfig
        self._getloop = asyncio.new_event_loop()
        self._getthread = Thread(
            target=start_loop,
            args=(self._getloop,),
            daemon=True,
            name='GetCVAsync-GetThread'
        )
        self._GoRUN = True
        self._getthread.start()
        self._maxQueue = self._econf.get('maxQueue', 2048)
        self._getqueue = Queue(self._maxQueue)
        self._getcoro = asyncio.run_coroutine_threadsafe(
            self.GetQueue(self._econf.get('GetInterval', 10)),
            self._getloop
        )
        self._session = session()

    def filter_headers(self, headers):
        '''过滤无用头部避免出错

        **你不应该在外部调用它！**  
        
        kwargs:
          - headers: 头部dict
        '''
        headers.pop('Host', None)
        headers.pop('Upgrade', None)
        headers.pop('Connection', None)
        headers.pop('Origin', None)
        for k in list(headers.keys()):
            if 'websocket' in k.lower():
                headers.pop(k, None)

    async def GetQueue(self, interval = 10):
        '''获取CV图片列表队列

        **你不应该在外部调用它！**  
        
        kwargs:
          - interval: 每次分析的间隔（单位：秒）（默认：10）
        '''
        from db import CacheDB
        while self._GoRUN:
            try:
                (url, reqheader, callback, loop) = self._getqueue.get()
                cache = CacheDB.getCache(getCVid(url)[1])   # 读缓存，判断是否能从缓存返回
                if cache:
                    asyncio.run_coroutine_threadsafe(callback(True, cache, True),loop)
                    continue
                self.filter_headers(reqheader)
                self._log.debug('reqheader = %s' % str(reqheader))
                res = self._session.get(url, headers = reqheader)
                if res.status_code == 200:
                    isbv, cvid = getCVid(url)
                    imgs = readCV(res.text, isbv)
                    CacheDB.Cache(cvid, imgs)     # 写入缓存
                    asyncio.run_coroutine_threadsafe(callback(True, imgs),loop)
                else:
                    asyncio.run_coroutine_threadsafe(callback(False, res),loop)
                await asyncio.sleep(interval)
            except Empty:
                pass
            except Exception as err:
                self._log.getChild('GetQueue').error("Type: %s, msg: %s" % (type(err),str(err)))
                asyncio.run_coroutine_threadsafe(callback(False, None, None),loop)
                await asyncio.sleep(interval)

    def Get(self, url, reqheader, callback, loop):
        '''异步获取CV图片列表
        kwargs:
          - url: CV的URL
          - reqheader: 用户的请求头
          - callback: websocket的回调
          - callback: 回调所在的asyncio loop
        
        return:
          (status:bool, errmsg:str)
        '''
        try:
            self._getqueue.put((url, reqheader, callback, loop))
        except Full:
            return False, 'Full'
        except:
            return False, 'Unknown'
        return True, 'Async'