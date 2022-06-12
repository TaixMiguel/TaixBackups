import secrets

SECRET_KEY = secrets.token_hex(30)

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

# App environments
APP_ENV = 'production'
