from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from os import environ

database_path = f'mysql://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@{environ.get("DB_HOST")}/{environ.get("DB_NAME")}'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        db.create_all()

        return db
