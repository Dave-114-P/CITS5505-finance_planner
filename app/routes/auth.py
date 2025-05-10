from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
import hashlib
from app.forms.authform import LoginForm, RegisterForm

# Define blueprint for auth routes
bp = Blueprint("auth", __name__)

# Helper function to hash password (SHA-256, simple version for now)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@bp.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():  # Use Flask-WTF's validate_on_submit
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password matches (hash)
        if user and user.password == hash_password(password):
            login_user(user)
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

    return render_template("register.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    # Handle user logout
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))