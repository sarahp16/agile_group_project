from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    city = StringField('City', validators=[DataRequired()])
    suburb = StringField('Suburb', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
