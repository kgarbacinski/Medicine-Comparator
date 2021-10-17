import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


LOGIN_MANAGER = LoginManager()
db = SQLAlchemy()
SECRET_KEY = os.urandom(32)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = SECRET_KEY
    db.init_app(app)
    LOGIN_MANAGER.login_view = 'login'
    LOGIN_MANAGER.init_app(app)
    LOGIN_MANAGER.login_message = "You're logged in succsesfully"

    from .views import MainPage, SignupView, LoginView
    app.add_url_rule('/', view_func=MainPage.as_view('main_page', template_name='home.html'))
    app.add_url_rule('/signup', view_func=SignupView.as_view('signup', template_name='signup.html'))
    app.add_url_rule('/login', view_func=LoginView.as_view('login', template_name='login.html'))
    create_database(app)
    return app


def create_database(app):

    if not path.exists('database.db'):
        db.create_all(app=app)
        print("Created database")

