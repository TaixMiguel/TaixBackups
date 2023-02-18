import os
from pathlib import Path

from app import kTaixBackups
from app.configApp import ConfigApp

configApp: ConfigApp = ConfigApp()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = configApp.get_value(kTaixBackups.Config.Application.ROOT, kTaixBackups.Config.Application.SECRET_KEY, 'django-insecure-gzh1)=p6c*$eog8nag#c!(%xf7sjgg8n+u)w%$ro!=0tghoh7a')
DEBUG = configApp.get_value_boolean(kTaixBackups.Config.Application.ROOT, kTaixBackups.Config.Application.DEBUG_MODE, True)
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backups.apps.BackupsConfig',
    'daemon.apps.DaemonConfig',
    'django_rq',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': configApp.get_value(kTaixBackups.Config.BBDD.ROOT, kTaixBackups.Config.BBDD.ENGINE, 'django.db.backends.sqlite3'),
        'NAME': configApp.get_value(kTaixBackups.Config.BBDD.ROOT, kTaixBackups.Config.BBDD.NAME, os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-es'
TIME_ZONE = os.environ.get('TZ', 'UTC')
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration of Django-RQ
RQ_QUEUES = {
    'default': {
        'HOST': configApp.get_value(kTaixBackups.Config.DjangoRQ.ROOT, kTaixBackups.Config.DjangoRQ.HOST, 'localhost'),
        'PORT': configApp.get_value_integer(kTaixBackups.Config.DjangoRQ.ROOT, kTaixBackups.Config.DjangoRQ.PORT, 6379),
        'DB': configApp.get_value_integer(kTaixBackups.Config.DjangoRQ.ROOT, kTaixBackups.Config.DjangoRQ.DB, 0),
        'DEFAULT_TIMEOUT': configApp.get_value_integer(kTaixBackups.Config.DjangoRQ.ROOT, kTaixBackups.Config.DjangoRQ.TIMEOUT, 360),
    }
}

# Configuration of log
level_log = configApp.get_value(kTaixBackups.Config.Log.ROOT, kTaixBackups.Config.Log.LEVEL_LOG, 'INFO')
path_log = configApp.get_value(kTaixBackups.Config.Log.ROOT, kTaixBackups.Config.Log.PATH, BASE_DIR)
n_files_log = configApp.get_value_integer(kTaixBackups.Config.Log.ROOT, kTaixBackups.Config.Log.NUMBER_FILES_LOG, 7)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': level_log, 'handlers': ['file', 'file_rq']},
    'handlers': {
        'file': {
            'level': level_log,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(path_log, 'taixBackups.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': n_files_log,
            'formatter': 'app',
        },
        'file_rq': {
            'level': level_log,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(path_log, 'taixBackups_rq.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': n_files_log,
            'formatter': 'app',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': level_log,
            'propagate': True
        },
        'rq.worker': {
            'handlers': ['file_rq'],
            'level': level_log,
            'propagate': True
        },
    },
    'formatters': {
        'app': {
            'format': (
                u'%(asctime)s [%(levelname)-8s] '
                '(%(module)s.%(funcName)s) %(message)s'
            ),
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
    },
}

if DEBUG:
    LOGGING['root']['handlers'] = ['file', 'file_rq', 'console']
    LOGGING['handlers']['console'] = {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'console'}
    LOGGING['formatters']['console'] = {'format': u'[%(levelname)-8s] (%(module)s.%(funcName)s) %(message)s'}
