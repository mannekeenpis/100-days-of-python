from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, Email, Required
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    emailaddress = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Choose a password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name = StringField("What's your name? ", validators=[DataRequired()])
    emailaddress = StringField("Email address: ", validators=[DataRequired(), Email()])
    password = PasswordField("Choose a password: ", validators=[DataRequired()])
    submit = SubmitField("Register")