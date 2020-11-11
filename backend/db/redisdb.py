import redis
from datetime import timedelta, datetime
from base64 import b64encode, b64decode
from traceback import format_exc
import logging
import json

class tempdb():
    def __init__(self, host = 'localhost', port = 6379, password = None, KeyTTL = timedelta(days=7),
                 database = 0, encoding = "UTF-8", decode_responses = True, fatherlog = None):
        self._log = fatherlog.getChild('TempDB') if fatherlog else logging.getLogger('TempDB')
        self._host = host
        self._port = port
        self._password = password
        self._db = database
        self._encoding = encoding
        self._decode_responses = decode_responses
        self._TTL = KeyTTL
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
            return json.loads(cachestr)
        except Exception as err:
            self._log.getChild('_getCache').error(format_exc())
            return None

    def getCache(self, cvid):
        return self._getCache(cvid)
    
    def Cache(self, cvid, imglist):
        cache = self._getCache(cvid)
        try:
            if cache:
                self._db.expire(cvid, int(self._TTL.total_seconds()))
            status = self._db.set(cvid, json.dumps(imglist), ex=int(self._TTL.total_seconds()))
            return status, None
        except Exception as err:
            self._log.getChild('_getCache').error(format_exc())
            return False, str(err)
        return True, None