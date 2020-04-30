from os import environ as sysenv

__all__ = ['envconfig']

def _envtranslate(x):
    if type(x) == str:
        if x.isnumeric():
            return int(x)
        elif x.count('.') == 1 and x.replace('.','').isnumeric():
            return float(x)
        elif x.lower() in ['true', 'false']:
            return x.lower() == 'true'
        return x
    elif type(x) == tuple and len(x) == 2:
        return (x[0],_envtranslate(x[1]))
    return x


class _NoneLog():
    def _allNone(self, *args, **kwargs):
        pass
    def getChild(self, name):
        return self
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except Exception:
            return self._allNone

class envconfig():
    def __init__(self, fatherlog = None):
        if not fatherlog:
            self._log = _NoneLog()
        else:
            self._log = fatherlog.getChild('envconfig')
        self.reload()
        # 习惯兼容层
        self.get = self.readConfig
        self.gets = self.readConfigs
        self.getdict = self.readConfigdict

    def reload(self):
        self._log.debug('重新读取环境变量')
        self._setting = {}
        self._setting.update(map(_envtranslate,sysenv.items()))

    def readConfig(self, Name, Default = None):
        self._log.debug('读取 "%s" ' % Name)
        return self._setting.get(Name,Default)

    def readConfigs(self, *Names, Default = None):
        self._log.debug('读取 %s ' % Names)
        return ( self._setting.get(Name,Default) for Name in Names )

    def readConfigdict(self, *Names, Default = None):
        self._log.debug('读取 %s ' % Names)
        return { Name:self._setting.get(Name,Default) for Name in Names }
