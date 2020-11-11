from sqlalchemy import Column, MetaData, create_engine, or_, String, JSON, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta, datetime
from json import dumps, loads

_meta = MetaData()
_Base = declarative_base(metadata=_meta)


class tempdb():
    class cvcache(_Base):
        __tablename__ = 'cvcache'

        cvid = Column(String(50), primary_key = True, autoincrement = False, nullable = False)
        imglist = Column(JSON(), nullable = False)
        expiretime = Column(DateTime(), nullable = False)

        def todict(self, args = ['cvid', 'imglist', 'expiretime']):
            d = {}
            for key in args:
                d[key] = loads(getattr(self,key,'[]')) if key == 'imglist' else getattr(self,key,None)
            return d

        def toJson(self):
            d=self.todict()
            d['expiretime'] = d['expiretime'].strftime('%Y-%m-%d %H:%M:%S')

    def _check_Tables(self, *tables):
        existTables = self._engine.table_names()
        return dict(zip(tables, [ t in existTables for t in tables]))

    def _check_Empty(self):
        return len(self._engine.table_names()) == 0

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
            session.close()
            return None
        if bool(inSession):
            return query.first()
        qd = query.first().todict()
        session.close()
        return qd

    def getCache(self, cvid):
        cache = self._getCache(cvid)
        if cache:
            now = datetime.now()
            return cache['imglist'] if now <= cache['expiretime'] else None
        return None

    def Cache(self, cvid, imglist):
        session = self.rawsession()
        cache = self._getCache(cvid, session)
        if cache:
            cache.update({'imglist': dumps(imglist), 'expiretime': datetime.now() + self._TTL})
        else:
            session.add(self.cvcache(
                cvid = cvid,
                imglist = dumps(imglist),
                expiretime = datetime.now() + self._TTL
            ))
        
        return self._sessioncommit(session)