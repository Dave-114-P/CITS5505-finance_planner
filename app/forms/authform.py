from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_wtf import FlaskForm


# WTForms for Login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")  # Add a SubmitField for the form's submit button


# WTForms for Registration
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female"), ("prefer not to say", "Prefer not to say")], validators=[Optional()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Create Account")  # Add a SubmitField for the form's submit button