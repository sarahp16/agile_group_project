from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

from app import db
from app.models import UsersInfo

class RegistrationForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    city = StringField('City', validators=[DataRequired()])
    suburb = StringField('Suburb', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
