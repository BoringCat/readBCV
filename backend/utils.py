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
    if not _isinit: _init_logconfig()
    return logging.getLogger(name)

def _init_logconfig():
    view = envconfig.get('VIEW', False)
    debug = envconfig.get('DEBUG', False)
    logconfig = {
        'level': logging.DEBUG if debug else logging.INFO if view else logging.WARN,
        'format': "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s",
        'datefmt': "%Y-%m-%d %H:%M:%S"
    }
    logging.basicConfig(**logconfig)
    _isinit = True
    
def setLogLevel(name, level):
    logging.getLogger(name).setLevel(level)

def start_loop(loop:asyncio.BaseEventLoop):
    loop.run_forever()

def readCV(webtext):
    bs = BeautifulSoup(webtext, features="html.parser")
    haveHead = bs.find('meta', {'data-hid': "og:image"})
    head_img = haveHead.attrs.get('content') if haveHead else None
    ulist = tuple(filter(lambda x:bool(x), map(lambda x:x.attrs.get('data-src'), bs.find('div','article-holder').find_all('img'))))
    return { 'header': head_img, 'contents': ['@'.join(u.split('@')[:-1]) if '@' in u else u for u in ulist] }

def getCVid(url):
    return int(url.split('/')[-1][2:])

class GetCVAsync():
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
        headers.pop('Host', None)
        headers.pop('Upgrade', None)
        headers.pop('Connection', None)
        headers.pop('Origin', None)
        for k in list(headers.keys()):
            if 'websocket' in k.lower():
                headers.pop(k, None)

    async def GetQueue(self, interval = 10):
        while self._GoRUN:
            try:
                (url, reqheader, callback, loop) = self._getqueue.get()
                self.filter_headers(reqheader)
                self._log.debug('reqheader = %s' % str(reqheader))
                res = self._session.get(url, headers = reqheader)
                if res.status_code == 200:
                    cvid = getCVid(url)
                    asyncio.run_coroutine_threadsafe(callback(True, cvid, readCV(res.text), loop),loop)
                else:
                    asyncio.run_coroutine_threadsafe(callback(False, None, res, loop),loop)
            except Empty:
                pass
            except Exception as err:
                self._log.getChild('GetQueue').error("Type: %s, msg: %s" % (type(err),str(err)))
                asyncio.run_coroutine_threadsafe(callback(False, None, None, loop),loop)
            finally:
                await asyncio.sleep(interval)

    def Get(self, url, reqheader, callback, loop):
        try:
            self._getqueue.put((url, reqheader, callback, loop))
        except Full:
            return False, 'Full'
        except:
            return False, 'Unknown'
        return True, 'Async'