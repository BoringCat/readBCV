from config import envconfig
import logging

_dblog = logging.getLogger('db.__init__')
__all__ = ['CreateDB']
_dbType = str(envconfig.get('DB_TYPE')).lower()
_dbconfs = list(envconfig.gets('DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB'))
_dblog.getChild('_dbType').debug(_dbType)
_dblog.getChild('_dbconfs').debug(str(dict(zip(['DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB'],_dbconfs))))

class createdb():
    def __init__(self, dbtype, dbconfs, dblog):
        self._dbtype = dbtype
        self._dbconfs = tuple(filter(lambda x:bool(x), dbconfs))
        self._log = dblog
        if not self._dbconfs:
            self._dbtype = 'sqlite'
            self._log.getChild('loadMongo').warning('No DB config found. Use SQLite3 memory db.')
    
    def __call__(self):
        if self._dbtype == 'sqlite':
            from .sqlite import tempdb
        elif self._dbtype in ('mysql', 'mariadb'):
            from .mysql import tempdb
        elif self._dbtype == 'mongo':
            from .mongo import tempdb
        elif not self._dbtype:
            from .sqlite import tempdb
            self._log.warning('DB_TYPE NOT SET! Use SQLite3 memory db.')
        else:
            from .sqlite import tempdb
            self._log.warning('DB_TYPE UNKNOWN! Use SQLite3 memory db.')
        return tempdb(*self._dbconfs)
    
CreateDB = createdb(_dbType, _dbconfs, _dblog)