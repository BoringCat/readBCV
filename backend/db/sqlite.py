from .sql_base import tempdb as _Base, create_engine, sessionmaker
import os
import logging

class tempdb(_Base):
    def __init__(self, database = None, fatherlog = None, pool_size = 10):
        self._log = fatherlog.getChild('TempDB') if fatherlog else logging.getLogger('TempDB')
        self._database = database
        self._pool_size = pool_size
        self._Session = self._connect_db()
        self._create_DB()
        
    def _connect_db(self):
        # 创建DBSession类型:
        db = ':memory:'
        if self._database:
            db = '%s?%s' % (os.path.abspath(self._database),'check_same_thread=False')
        address = 'sqlite:///%s' % db
        self._log.getChild('_connect_db').debug(address)
        self._engine = create_engine(address)
        self._engine.execute('PRAGMA secure_delete = ON')
        self._engine.execute('PRAGMA auto_vacuum = FULL')
        return sessionmaker(bind = self._engine)