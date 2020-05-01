from config import envconfig

__all__ = ['CacheDB']
_dbconfs = envconfig.gets('DB_HOST','DB_PORT','DB_USER','DB_PASSWD','DB_NAME','DB_AUTHDB')
if tuple(filter(lambda x:bool(x), _dbconfs)):
    from .mongo import tempdb
    CacheDB = tempdb(*_dbconfs)
else:
    from .sqlite import tempdb
    print('No DB config found. Use SQLite3 memory db.')
    CacheDB = tempdb()