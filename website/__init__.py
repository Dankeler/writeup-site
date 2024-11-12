from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_NAME = "database.db"

def app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .models import Writeup
    from . import routes

    app.register_blueprint(routes.app) 

    with app.app_context():
        db.create_all()

    return app
