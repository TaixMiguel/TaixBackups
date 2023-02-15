APP_NAME = 'Generador de Backups'
APP_VERSION = '0.1.0_alpha'

class Config:
    class Application:
        ROOT = 'app'
        DEBUG_MODE = 'debugMode'
        SECRET_KEY = 'secretKey'

    class BBDD:
        ROOT = 'bbdd'
        ENGINE = 'engine'
        NAME = 'name'

    class DjangoRQ:
        ROOT = 'djangoRQ'
        DASHBOARD = 'dashboard'
        DB = 'db'
        HOST = 'host'
        PORT = 'port'
        TIMEOUT = 'timeout'

    class Log:
        ROOT = 'log'
        NUMBER_FILES_LOG = 'numberOfLogsFile'
        LEVEL_LOG = 'levelLog'
        PATH = 'path'

    class MQTT:
        ROOT = 'mqtt'
        SWITCH_ENABLED = 'enabled'
        PASS = 'password'
        SERVER = 'server'
        USER = 'username'

class Backup:
    STATUS_COMPLETE: str = 'COMPLETE'
    STATUS_ERROR: str = 'ERROR'
    STATUS_PDTE: str = 'PDTE'

class MQTT:
    TOPIC: str = '/taixBackups/'
    BACKUP_GLOBAL: str = 'global'
