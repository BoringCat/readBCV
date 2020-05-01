from config import envconfig
from utils import createLogger

_dblog = createLogger('db.__init__')
__all__ = ['CacheDB']
_dbconfs = list(envconfig.gets('DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB'))
_dblog.debug('_dbconfs: %s' % str(dict(zip(['DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB'],_dbconfs))))
if tuple(filter(lambda x:bool(x), _dbconfs)):
    from .mongo import tempdb
    CacheDB = tempdb(*_dbconfs)
else:
    from .sqlite import tempdb
    print('No DB config found. Use SQLite3 memory db.')
    CacheDB = tempdb()