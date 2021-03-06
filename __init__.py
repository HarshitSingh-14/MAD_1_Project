# The folder containing this __init__.py file will become a python package which can be imported
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import *
from .auth import *
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def start_myApp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'this is a secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qsjrkwcvohermr:39203386e31c617f0584da912f020e6691e542dae815a3cd14e75c42ac78e3c7@ec2-35-168-145-180.compute-1.amazonaws.com:5432/dbud169edkki14
'
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Course, Log

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
