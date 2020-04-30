import logging
import sys
from bs4 import BeautifulSoup
import asyncio
from threading import Thread
from queue import Queue, Empty
from config import envconfig
from requests import session

_isinit = False

__all__ = [ 'createLogger', 'setLogLevel', 'GetCVAsync' ]

def createLogger(name):
    if not _isinit: _init_logconfig()
    return logging.getLogger(name)

def _init_logconfig():
    view = '--view' in sys.argv
    debug = '--debug' in sys.argv
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
    ulist = tuple(filter(lambda x:bool(x), map(lambda x:x.attrs.get('data-src'), bs.find('div','article-holder').find_all('img'))))
    return ['@'.join(u.split('@')[:-1]) if '@' in u else u for u in ulist]

class GetCVAsync():
    def __init__(self, fatherlog):
        self._log = fatherlog.getChild('GetCVAsync')
        self._econf = envconfig()
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
            self.GetQueue(self._econf.get('GetInterval', 1)),
            self._getloop
        )
        self._session = session()

    def filter_headers(self, headers):
        headers.pop('Host')
        headers.pop('Upgrade')
        headers.pop('Connection')
        for k in list(headers.keys()):
            if 'websocket' in k.lower():
                headers.pop(k)

    async def GetQueue(self, interval = 1):
        while self._GoRUN:
            try:
                (url, reqheader, callback, loop) = self._getqueue.get()
                await asyncio.sleep(5)
                self.filter_headers(reqheader)
                self._log.debug('reqheader = %s' % str(reqheader))
                res = self._session.get(url, headers = reqheader)
                if res.status_code == 200:
                    asyncio.run_coroutine_threadsafe(callback(True, readCV(res.text), loop),loop)
                else:
                    asyncio.run_coroutine_threadsafe(callback(False, res, loop),loop)
            except Empty:
                pass
            except Exception:
                asyncio.run_coroutine_threadsafe(callback(False, None, loop),loop)
            finally:
                await asyncio.sleep(interval)

    def Get(self, url, reqheader, callback, loop):
        self._getqueue.put((url, reqheader, callback, loop))
        return True, 'Async'