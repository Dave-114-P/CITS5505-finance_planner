from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_wtf import FlaskForm


# WTForms for Login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")  # Add a BooleanField for "Remember Me"
    submit = SubmitField("Login")  # Add a SubmitField for the form's submit button


# WTForms for Registration
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female"), ("prefer not to say", "Prefer not to say")], validators=[Optional()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Create Account")  # Add a SubmitField for the form's submit button

# WTForms for Password Forgot
class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

# WTForms for Password Reset
class ResetPasswordForm(FlaskForm):
    """
    A form for resetting a user's password.
    """
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Reset Password')