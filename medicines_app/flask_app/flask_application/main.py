import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
import jwt


LOGIN_MANAGER = LoginManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = os.environ("SECRET_KEY")

    db.init_app(app)

    LOGIN_MANAGER.login_view = 'login'
    LOGIN_MANAGER.init_app(app)
    LOGIN_MANAGER.login_message = "You're logged in successfully"


    from .views import HomePage, SignupView, LoginView, SearchView
    app.add_url_rule('/', view_func=HomePage.as_view('main_page', template_name='home.html'))
    app.add_url_rule('/signup', view_func=SignupView.as_view('signup', template_name='signup.html'))
    app.add_url_rule('/login', view_func=LoginView.as_view('login', template_name='login.html'))
    app.add_url_rule('/search_result', view_func=SearchView.as_view('table', template_name='search_result.html'))
    create_database(app)

    Session(app)

    return app


def create_database(app):

    if not path.exists('../../models/database.db'):
        db.create_all(app=app)
        print('db created')

