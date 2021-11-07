from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, InputRequired
from flask_wtf import FlaskForm


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
