from .sql_base import tempdb as _Base, create_engine, sessionmaker
import logging

class tempdb(_Base):
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
            pool_recycle=900,
            pool_pre_ping=True
        )
        return sessionmaker(bind = self._engine)