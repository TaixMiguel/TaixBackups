from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

app_bp = Blueprint('app', __name__, template_folder='templates')
db = SQLAlchemy()
migrate = Migrate()

from . import routes


def create_app() -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py', silent=True)
    configure_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(app_bp)
    return app


def configure_logging(app):
    del app.logger.handlers[:]
    loggers = [app.logger]
    handlers = get_handlers(app)

    for log in loggers:
        for handler in handlers:
            log.addHandler(handler)
        log.propagate = False
        log.setLevel(app.config['LOG_LEVEL'])


def get_handlers(app) -> []:
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter(app))
    console_handler.setLevel(app.config['LOG_LEVEL'])
    handlers.append(console_handler)

    if app.config['LOG_FILE']:
        file_handler = logging.FileHandler(app.config['LOG_FILE'])
        file_handler.setFormatter(verbose_formatter(app))
        file_handler.setLevel(app.config['LOG_LEVEL'])
        handlers.append(file_handler)

    return handlers


def verbose_formatter(app):
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt=app.config['LOG_DATE_FORMAT']
    )
