from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.authform import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm

# Define blueprint for auth routes
bp = Blueprint("auth", __name__)

# Enhance password security
def hash_password(password):
    return generate_password_hash(password)

@bp.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():  # Use Flask-WTF's validate_on_submit
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data  # Get the value of the "Remember Me" checkbox
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password matches (hash)
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember_me)  # Pass "remember=remember_me" to login_user
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    # Handle user registration
    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():  # Use Flask-WTF's validate_on_submit
        username = form.username.data
        email = form.email.data
        gender = form.gender.data
        password = form.password.data

        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or Email already exists. Please choose another.", "danger")
            return redirect(url_for("auth.register"))

        # Save new user with hashed password
        new_user = User(
            username=username,
            email=email,
            gender=gender,
            password=hash_password(password)  # IMPORTANT: Save hashed password
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))
    else:
        # Debugging: Print form errors in the console
        print(f"Form errors: {form.errors}")
        # Return a 400 Bad Request response if validation fails
        return render_template("register.html", form=form), 400


@bp.route("/logout")
@login_required
def logout():
    # Handle user logout
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

from flask import session, abort, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature


@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    Route for the "Forgot Password" page.
    """
    form = ForgotPasswordForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        user = User.query.filter_by(username=username, email=email).first()

        if user:
            token = serializer.dumps(user.id)
            reset_url = url_for("auth.reset_password_form", token=token, _external=True, url_scheme='https')

            # Send email (replace flash with email sending in production)
            flash(f'<a href="{reset_url}" class="alert-link">Click here to reset your password</a>', "info")
        else:
            flash("If the provided information is correct, a password reset link will be sent.", "info")

        return redirect(url_for("auth.forgot_password"))

    return render_template("forgot_password.html", form=form)


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password_form(token):
    """
    Enhanced route for resetting the password directly after verification.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        user_id = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        flash("The password reset link has expired. Please request a new one.", "danger")
        return redirect(url_for("auth.forgot_password"))
    except BadSignature:
        flash("Invalid password reset link.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.get_or_404(user_id)

    # Initialize the form
    form = ResetPasswordForm()

    if form.validate_on_submit():
        password = form.password.data
        user.set_password(password)
        db.session.commit()

        flash("Your password has been updated!", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form, token=token)