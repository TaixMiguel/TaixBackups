APP_NAME = 'Generador de Backups'
APP_VERSION = '0.1.0_alpha'

class Config:
    class Application:
        ROOT = 'app'
        DEBUG_MODE = 'debugMode'
        SECRET_KEY = 'secretKey'

    class DjangoRQ:
        ROOT = 'djangoRQ'
        DB = 'db'
        HOST = 'host'
        PORT = 'port'
        TIMEOUT = 'timeout'

    class Log:
        ROOT = 'log'
        LEVEL_LOG = 'levelLog'
        PATH = 'path'
