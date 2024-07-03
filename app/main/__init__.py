from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from dotenv import load_dotenv

from app.main.config import config_by_name


load_dotenv()

db = SQLAlchemy()

flask_bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_name):
    config = config_by_name[config_name]

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.debug = config.DEBUG
    app.config["ERROR_404_HELP"] = False  # disable the default error message
    db.init_app(app)
    flask_bcrypt.init_app(app)

    migrate.init_app(app, db)

    return app
