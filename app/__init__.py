from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app_bp = Blueprint('app', __name__, template_folder='templates')
db = SQLAlchemy()
migrate = Migrate()

from . import routes


def create_app() -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(app_bp)
    check_database_exist('database.db', app)
    return app


def check_database_exist(database_uri: str, app: Flask) -> None:
    from os.path import exists
    if not exists(database_uri):
        # TODO: añadir línea al log
        print(f"Se procede a crear la BBDD {database_uri}")
        db.create_all(app=app)
