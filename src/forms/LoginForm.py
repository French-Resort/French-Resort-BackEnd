from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    user_email = EmailField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')