import logging
from config import envconfig
from bs4 import BeautifulSoup
import asyncio
from threading import Thread
from queue import Queue, Empty, Full
from config import envconfig
from requests import session
from i18n import t
import re
import json

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

def br2Newline(obj):
    for br in obj.find_all('br'):
        br.replace_with('\n')
    return obj

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

    def _url_filter(self, baseurl, url):
        '''分析URL

        **你不应该在外部调用它！**

        args:
        - baseurl: 当前页面的URL
        - url: data-src的URL

        return:
        - url: 完整链接
        '''
        if not url.startswith('http'):
            if url.startswith('//'):
                return 'https:' + url
            elif url.startswith('/'):
                return 'https://www.bilibili.com' + url
            else:
                return baseurl + url
        return ('https:%s' % url[5:]) if url[:5] == 'http:' else url

    def readCV(self, baseurl, webtext, isBV = False, userAgents = None, locale = 'zh_CN'):
        '''分析图片们

        **你不应该在外部调用它！**

        args:
        - webtext: 页面HTML文本
        '''
        bs = BeautifulSoup(webtext, features="html.parser")
        if isBV:
            head_img, title = self._readBV(webtext)
            haveHead = bs.find('meta', {'property': "og:image"})    # 获取封面
            head_img = haveHead.attrs.get('content') if haveHead else None
            return { 'contents': [{ 'url': head_img, 'title': t('cover', locale), 'figcaption': title }], 'header': {} }
        haveHead = bs.find('meta', {'data-hid': "og:image"})    # 获取封面
        head_img = self._url_filter(baseurl, haveHead.attrs.get('content')) if haveHead else None
        imgs = list(filter(                                     # 过滤分割图片（`cut-off-\d+`）
            lambda x:'cut-off' not in ('\n'.join(x.attrs.get('class',[]))),
            bs.find('div','article-holder').find_all('img')
        ))
        ulist = []
        for img in imgs:
            data_src = img.attrs.get('data-src')
            if not data_src:
                continue
            # 如果是视频链接
            if 'video-card' in img.attrs.get('class', []):
                self._log.getChild('readCV').getChild('video-card').debug('is video-card')
                aids = img.attrs.get('aid')              # 目前是用aid，也就是av号（2020/05/30）
                if aids:
                    for aid in aids.split(','):
                        acimg, atitle = self.av_in_cv(aid, userAgents)
                        if acimg:
                            # 返回视频封面， 视频标题， 标签
                            ulist.append({'url': acimg, 'figcaption': atitle, 'title': t('video_cover', locale)})
                bids = img.attrs.get('bvid')              # 如果用改成BV号，可能需要修改代码
                if bids:
                    for bid in bids.split(','):
                        bcimg, btitle = self.bv_in_cv(bid, userAgents)
                        if bcimg:
                            # 返回视频封面， 视频标题， 标签
                            ulist.append({'url': bcimg, 'figcaption': btitle, 'title': t('video_cover', locale)})
                continue
            # 获取图片原图
            raw_src = self._url_filter(baseurl, '@'.join(data_src.split('@')[:-1]) if '@' in data_src else data_src)
            figcaptions = img.parent('figcaption')
            if figcaptions:
                ulist.append({'url': raw_src, 'figcaption': '\n'.join(map(lambda x:x.text, map(br2Newline, figcaptions)))})
            else:
                ulist.append({'url': raw_src})
        return {
            'header': head_img,
            'contents': ulist
        }

    def _readBV(self, webtext, id = None, isav = False):
        '''分析视频封面和标题

        **你不应该在外部调用它！**

        args:
        - webtext: 页面HTML文本
        - id: 视频ID
        - isav: 是否为AV

        return:
        - head_imd: 视频封面
        - title: 视频标题
        '''
        bs = BeautifulSoup(webtext, features="html.parser")
        haveHead = bs.find('meta', {'property': "og:image"})    # 获取封面
        title = bs.find('h1', {'class': "video-title"}).attrs.get('title')
        if isav and id:
            title = self._getBV_from_av(id, bs) + ': ' + title
        head_img = self._url_filter("https://www.bilibili.com/video/%s" % (id or ''), haveHead.attrs.get('content')) if haveHead else None
        return head_img, title

    def _getBV_from_av(self, aid, bs:BeautifulSoup):
        '''从AV号中获取BV号

        **你不应该在外部调用它！**

        args:
        - aid: AV号
        - bs: 分析AV用的BeautifulSoup

        return:
        - bvid: BV号
        '''
        scriptlist = list(filter(lambda x: aid in (x.string or ''), bs.find_all('script') ))
        for script in scriptlist:
            trysearch = re.search(r'__INITIAL_STATE__[ ]?=[ ]?(?P<j>[\S \n]+)}[ ]*;', script.string)
            if trysearch:
                jsonstr = trysearch.groupdict()['j'] + '}'
                j = json.loads(jsonstr)
                bvid = j.get('videoData',{}).get('bvid',None)
                if bvid:
                    return bvid

    def av_in_cv(self, aid, userAgents):
        '''分析CV中的AV

        **你不应该在外部调用它！**

        args:
        - aid: AV号
        - userAgents: 请求时的用户头部

        return:
        - head_imd: 视频封面
        - title: 视频标题
        '''
        res = self._session.get('https://www.bilibili.com/video/av%s' % aid, headers=userAgents)
        if res.status_code == 200:
            return self._readBV(res.text, aid, True)
        else:
            return None, None

    def bv_in_cv(self, bvid, userAgents):
        '''分析CV中的BV

        **你不应该在外部调用它！**

        args:
        - bvid: BV号
        - userAgents: 请求时的用户头部

        return:
        - head_imd: 视频封面
        - title: 视频标题
        '''
        res = self._session.get('https://www.bilibili.com/video/BV%s' % bvid, headers=userAgents)
        if res.status_code == 200:
            return self._readBV(res.text)
        else:
            return None, None

    async def GetQueue(self, interval = 10):
        '''获取CV图片列表队列

        **你不应该在外部调用它！**  
        
        kwargs:
          - interval: 每次分析的间隔（单位：秒）（默认：10）
        '''
        from db import CacheDB
        while self._GoRUN:
            try:
                (url, reqheader, locale, callback, loop) = self._getqueue.get()
                cache = CacheDB.getCache(getCVid(url)[1])   # 读缓存，判断是否能从缓存返回
                if cache:
                    asyncio.run_coroutine_threadsafe(callback(True, cache, True),loop)
                    continue
                self.filter_headers(reqheader)
                self._log.debug('reqheader = %s' % str(reqheader))
                res = self._session.get(url, headers = reqheader)
                if res.status_code == 200 and res.url == url:
                    isbv, cvid = getCVid(url)
                    imgs = self.readCV(url, res.text, isbv, reqheader, locale)
                    CacheDB.Cache(cvid, imgs)     # 写入缓存
                    asyncio.run_coroutine_threadsafe(callback(True, imgs),loop)
                else:
                    asyncio.run_coroutine_threadsafe(callback(False, res.status_code if res.url == url else t('page_not_found', locale) ),loop)
                await asyncio.sleep(interval)
            except Empty:
                pass
            except Exception as err:
                self._log.getChild('GetQueue').error("Type: %s, msg: %s" % (type(err),str(err)))
                asyncio.run_coroutine_threadsafe(callback(False, None, None),loop)
                await asyncio.sleep(interval)

    def Get(self, url, reqheader, locale, callback, loop):
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
            self._getqueue.put((url, reqheader, locale, callback, loop))
        except Full:
            return False, 'Full'
        except:
            return False, 'Unknown'
        return True, 'Async'