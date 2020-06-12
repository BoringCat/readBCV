import redis
from datetime import timedelta, datetime
from base64 import b64encode, b64decode
import logging
import json

class tempdb():
    def __init__(self, host = 'localhost', port = 6379, password = None,
                 database = 0, encoding = "UTF-8", decode_responses = True, fatherlog = None):
        self._log = fatherlog.getChild('TempDB') if fatherlog else logging.getLogger('TempDB')
        self._host = host
        self._port = port
        self._password = password
        self._db = database
        self._encoding = encoding
        self._decode_responses = decode_responses
        self._connectDB()

    def _connectDB(self):
        connect_args = {}
        if self._host != 'localhost':
            connect_args['host'] = self._host
        if self._port != 6379:
            connect_args['port'] = self._port
        if self._password:
            connect_args['password'] = self._password
        if self._db != 0:
            connect_args['db'] = self._db
        connect_args['encoding'] = self._encoding
        connect_args['decode_responses'] = self._decode_responses
        self._db = redis.StrictRedis(**connect_args)

    def _getCache(self, cvid):
        cachestr = self._db.get(cvid)
        if not cachestr:
            return None
        try:
            cjson = json.loads(cachestr)
            return {
                'cachetime': datetime.fromtimestamp(cjson['cachetime']),
                'imglist': json.loads(b64decode(cjson['imglist'].encode('UTF-8')))
            }
        except Exception as err:
            self._log.getChild('_getCache').error(str(err))
            return None

    def getCache(self, cvid, TTL = timedelta(days=7)):
        cache = self._getCache(cvid)
        if cache:
            now = datetime.now()
            return cache['imglist'] if (now - cache['cachetime']) < TTL else None
        return None
    
    def Cache(self, cvid, imglist):
        datas = {
            'imglist': b64encode(json.dumps(imglist, ensure_ascii=False).encode('UTF-8')).decode('UTF-8'),
            'cachetime': datetime.now().timestamp()
        }
        try:
            status = self._db.set(cvid, json.dumps(datas, ensure_ascii=False))
            return status, None
        except Exception as err:
            self._log.getChild('Cache').error(str(err))
            return False, str(err)
        return True, None