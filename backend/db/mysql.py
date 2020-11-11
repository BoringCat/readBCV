from .sql_base import tempdb as _Base, create_engine, sessionmaker
import logging

class tempdb(_Base):
    def __init__(self, host = "localhost", port = 3306, user = "readbcv", password = "readbcv", 
                 database = "readbcv", fatherlog = None, pool_size = 10, KeyTTL = timedelta(days=7)):
        self._log = fatherlog.getChild('TempDB') if fatherlog else logging.getLogger('TempDB')
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._pool_size = pool_size
        self._TTL = KeyTTL
        self._Session = self._connect_db()
        self._create_DB()
        
    def _connect_db(self):
        # 创建DBSession类型:
        self._log.getChild('_connect_db').debug(
            'mysql+pymysql://%s:%s@%s:%s/%s' % (self._user, self._password, self._host, self._port, self._database)
        )
        self._engine = create_engine(
            'mysql+pymysql://%s:%s@%s:%s/%s' % (self._user, self._password, self._host, self._port, self._database),
            pool_size=self._pool_size,
            pool_recycle=900,
            pool_pre_ping=True
        )
        return sessionmaker(bind = self._engine)

    def _create_DB(self):
        if self._check_Empty():
            self._log.getChild('_create_DB').warning('Table "cvcache" is not exist. Create!')
            super()._create_DB()
