import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Достаем токен для работы программы через главную страницу (не API)
load_dotenv()
token_flask = os.getenv("APP_TOKEN")

app_flask = Flask(__name__)
app_flask.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")

app_flask.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///repos.db"
app_flask.config["SQLALCHEMY_MIGRATE_REPO"] = "migrate"

db = SQLAlchemy(app_flask)
migrate = Migrate(app_flask, db)

# TODO: Seems unused, remove?
# from app import models

with app_flask.app_context():
    db.create_all()
