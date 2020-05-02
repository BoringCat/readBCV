from config import envconfig
from utils import createLogger

_dblog = createLogger('db.__init__')
__all__ = ['CacheDB']
_dbType = str(envconfig.get('DB_TYPE')).lower()
_dbconfs = list(envconfig.gets('DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB'))
_dblog.getChild('_dbType').debug(_dbType)
_dblog.getChild('_dbconfs').debug(str(dict(zip(['DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB'],_dbconfs))))

def loadSQLite():
    from .sqlite import tempdb
    return tempdb()

def loadMySQL(dbconfs):
    if tuple(filter(lambda x:bool(x), dbconfs)):
        from .mysql import tempdb
        return tempdb(*dbconfs)
    else:
        _dblog.getChild('loadMySQL').warning('No MySQL/Mariadb DB config found. Use SQLite3 memory db.')
        return loadSQLite()

def loadMongo(dbconfs):
    if tuple(filter(lambda x:bool(x), dbconfs)):
        from .mongo import tempdb
        return tempdb(*dbconfs)
    else:
        _dblog.getChild('loadMongo').warning('No MySQL/Mariadb DB config found. Use SQLite3 memory db.')
        return loadSQLite()

if _dbType == 'sqlite':
    CacheDB = loadSQLite()
elif _dbType == 'mysql':
    CacheDB = loadMySQL(_dbconfs[:-1])
elif _dbType == 'mariadb':
    CacheDB = loadMySQL(_dbconfs[:-1])
elif _dbType == 'mongo':
    CacheDB = loadMongo(_dbconfs)
else:
    _dblog.warning('DB_TYPE NOT SET! Use SQLite3 memory db.')
    CacheDB = loadSQLite()