from mongoengine import (connect, DynamicDocument,
    DictField, StringField, DateTimeField, Q)
import logging
from datetime import timedelta, datetime

class tempdb():
    class cvcache(DynamicDocument):
        cvid = StringField()
        imglist = DictField()
        expiretime = DateTimeField()

        def todict(self, args = ['cvid', 'imglist', 'expiretime']):
            d = {}
            for key in args:
                d[key] = getattr(self,key,None)
            return d
        
        def toJson(self):
            return dict(
                cvid = self.cvid,
                imglist = self.imglist,
                expiretime = self.expiretime.strftime('%Y-%m-%d %H:%M:%S')
            )

    def __init__(self, host = "localhost", port = 27017, user = "readbcv", KeyTTL = timedelta(days=7),
                 password = "readbcv", database = "readbcv", authdb = None, fatherlog = None):
        self._log = fatherlog.getChild('TempDB') if fatherlog else logging.getLogger('TempDB')
        self._host = host
        self._port = port
        self._username = user
        self._password = password
        self._dbname = database
        self._authdb = authdb or database
        self._TTL = KeyTTL
        self._connectDB()

    def _connectDB(self):
        self._log.getChild('_connect_db').debug('mongo://%s:%s@%s:%s/%s'
                % (self._username, self._password, self._host, self._port, self._dbname))
        self._db = connect(self._dbname, host=self._host, port=self._port, 
            username=self._username, password=self._password, authentication_source=self._authdb)

    def _getCache(self, cvid):
        query = self.cvcache.objects(cvid = cvid)
        if not query:
            return None
        return query[0]

    def getCache(self, cvid, TTL = timedelta(days=7)):
        cache = self._getCache(cvid)
        if cache:
            now = datetime.now()
            return cache.imglist if now <= cache.expiretime else None
        return None

    def Cache(self, cvid, imglist):
        cache = self._getCache(cvid)
        if cache:
            cache.imglist = imglist
            cache.expiretime = datetime.now() + self._TTL
            try:
                cache.save()
            except Exception as err:
                return False, str(err)
            return True, None
        else:
            newCache = self.cvcache(
                cvid = cvid,
                imglist = imglist,
                expiretime = datetime.now() + self._TTL
            )
            try:
                newCache.save()
            except Exception as err:
                return False, str(err)
            return True, None