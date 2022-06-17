import logging
import secrets

SECRET_KEY = secrets.token_hex(30)

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

# Logger
LOG_LEVEL = logging.INFO
LOG_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
LOG_FILE = 'taixBackups'

# App environments
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_PRODUCTION = 'production'
APP_ENV = APP_ENV_PRODUCTION
