from flask_login import LoginManager

__author__ = 'hughson.simon@gmail.com'

login_manager = LoginManager()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
