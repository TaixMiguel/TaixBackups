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
    check_database_exist('database.db', app)
    return app


def configure_logging(app):
    del app.logger.handlers[:]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter(app))
    console_handler.setLevel(app.config['LOG_LEVEL'])
    handlers.append(console_handler)
    for log in loggers:
        for handler in handlers:
            log.addHandler(handler)
        log.propagate = False
        log.setLevel(logging.DEBUG)


def verbose_formatter(app):
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt=app.config['LOG_DATE_FORMAT']
    )


def check_database_exist(database_uri: str, app: Flask) -> None:
    from os.path import exists
    if not exists(database_uri):
        # TODO: añadir línea al log
        print(f"Se procede a crear la BBDD {database_uri}")
        db.create_all(app=app)
