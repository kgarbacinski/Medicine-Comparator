from flask import render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, InputRequired
from flask_wtf import FlaskForm
from .models import User, Token, register_user, update_token_status


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=20)])
    password = StringField('Password', validators=[InputRequired(), Length(min=5, max=20)])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    token = StringField('Token', validators=[InputRequired(), Length(max=15)])
    submit = SubmitField('Register')


class MainPage(MethodView):

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)


class LoginView(MethodView):
    def __init__(self, template_name):
        self.template_name = template_name

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return render_template('base.html')

    def get(self):
        form = LoginForm()
        return render_template(self.template_name, form=form)


class SignupView(MethodView):
    def __init__(self, template_name):
        self.template_name = template_name

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            password = generate_password_hash(form.password.data, 'sha256')
            email = form.email.data
            token = Token.query.filter_by(token=form.token.data).first()
            if token is None or token.is_used is False:
                flash("Invalid token, please try again")
                return redirect(url_for('signup', form=form))
            else:
                is_super_user = 1
                user = User(username, password, email, is_super_user, token_id=token.token_id)
                update_token_status(token.token_id)
                register_user(user)
                flash("Your account has been created successfully")
                return redirect(url_for('main_page', form=form))
        return "<h1>Blad<h1>"

    def get(self):
        form = RegisterForm()
        return render_template(self.template_name, form=form)
