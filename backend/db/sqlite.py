from sqlalchemy import Column, MetaData, create_engine, or_, Integer, JSON, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import logging
from datetime import timedelta, datetime
from json import dumps, loads

_meta = MetaData()
_Base = declarative_base(metadata=_meta)


class tempdb():
    class cvcache(_Base):
        __tablename__ = 'cvcache'

        cvid = Column(Integer(), primary_key = True, autoincrement = False, nullable = False)
        imglist = Column(JSON(), nullable = False)
        cachetime = Column(DateTime(), nullable = False)

        def todict(self, args = ['cvid', 'imglist', 'cachetime']):
            d = {}
            for key in args:
                d[key] = loads(getattr(self,key,'[]')) if key == 'imglist' else getattr(self,key,None)
            return d

        def toJson(self):
            d=self.todict()
            d['cachetime'] = d['cachetime'].strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self, fatherlog = None, pool_size = 10):
        self._log = fatherlog.getChild('TempDB') if fatherlog else logging.getLogger('TempDB')
        self._pool_size = pool_size
        self._Session = self._connect_db()
        self._create_DB()
        
    def _connect_db(self):
        # 创建DBSession类型:
        self._log.getChild('_connect_db').debug('sqlite://')
        self._engine = create_engine('sqlite://',
            pool_size=self._pool_size,
            pool_pre_ping=True
        )
        return sessionmaker(bind = self._engine)

    def _create_DB(self):
        _meta.create_all(self._engine)

    # 获取session
    def rawsession(self) -> Session:
        return self._Session()

    # 提交数据库会话
    def _sessioncommit(self, session, close = True):
        result = False
        errmsg = None
        try:
            session.commit()
            result = True
        except Exception as err:
            session.rollback()
            result = False
            errmsg = str(err)
            self._log.getChild('_sessioncommit').warning('数据库提交失败 %s' % errmsg)
        finally:
            if close: session.close()
        return result, errmsg

    def _getCache(self, cvid, inSession:Session = None):
        session = inSession if bool(inSession) else self.rawsession()
        query = session.query(self.cvcache).filter(self.cvcache.cvid == cvid)
        if not query.count():
            return None
        if bool(inSession):
            return query.first()
        qd = query.first().todict()
        session.close()
        return qd

    def getCache(self, cvid, TTL = timedelta(days=7)):
        cache = self._getCache(cvid)
        if cache:
            now = datetime.now()
            return cache['imglist'] if (now - cache['cachetime']) < TTL else None
        return None

    def Cache(self, cvid, imglist):
        session = self.rawsession()
        cache = self._getCache(cvid, session)
        if cache:
            cache.update({'imglist': dumps(imglist), 'cachetime': datetime.now()})
        else:
            session.add(self.cvcache(
                cvid = cvid,
                imglist = dumps(imglist),
                cachetime = datetime.now()
            ))
        
        return self._sessioncommit(session)