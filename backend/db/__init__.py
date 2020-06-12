from config import envconfig
import logging

_dblog = logging.getLogger('db.__init__')
__all__ = ['CreateDB']
_dbType = str(envconfig.get('DB_TYPE')).lower()
_dbconfs = dict(zip(
    ['host', 'port', 'user', 'password', 'database', 'authdb'],
    list(envconfig.gets('DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB'))
))
_dblog.getChild('_dbType').debug(_dbType)
_dblog.getChild('_dbconfs').debug(str(_dbconfs))

class createdb():
    def __init__(self, dbtype, dbconfs, dblog):
        self._dbtype = dbtype
        self._dbconfs = dict(filter(lambda x:bool(x[1]), dbconfs.items()))
        self._log = dblog
        if not self._dbconfs:
            self._dbtype = 'sqlite'
            self._log.getChild('createdb').warning('No DB config found. Use SQLite3 memory db.')
    
    def __call__(self, fatherlog = None):
        if self._dbtype == 'sqlite':
            self._dbconfs.pop('host', None)
            self._dbconfs.pop('port', None)
            self._dbconfs.pop('user', None)
            self._dbconfs.pop('password', None)
            self._dbconfs.pop('authdb', None)
            from .sqlite import tempdb
        elif self._dbtype in ('mysql', 'mariadb'):
            self._dbconfs.pop('authdb', None)
            from .mysql import tempdb
        elif self._dbtype == 'mongo':
            from .mongo import tempdb
        elif self._dbtype == 'redis':
            from .redisdb import tempdb
            # redisDB Only Support HOST, PORT, PASSWORD, DB
            self._dbconfs.pop('user', None)
            self._dbconfs.pop('authdb', None)
        elif not self._dbtype:
            from .sqlite import tempdb
            self._dbconfs = {}
            self._log.warning('DB_TYPE NOT SET! Clean all configs! Use SQLite3 memory db.')
        else:
            from .sqlite import tempdb
            self._dbconfs = {}
            self._log.warning('DB_TYPE UNKNOWN! Clean all configs! Use SQLite3 memory db.')
        return tempdb(**self._dbconfs, fatherlog=fatherlog)
    
CreateDB = createdb(_dbType, _dbconfs, _dblog)