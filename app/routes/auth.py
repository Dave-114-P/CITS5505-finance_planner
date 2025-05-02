# Authentication routes: login, register, logout

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
import hashlib

# Define blueprint for auth routes
bp = Blueprint("auth", __name__)

def hash_password(password):
    # Hash the password using SHA-256 (not secure for production; use bcrypt in real apps)
    return hashlib.sha256(password.encode()).hexdigest()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.password == hash_password(password):
            login_user(user)
            return redirect(url_for("index", username=username))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    # Registration route
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for("auth.register"))
        new_user = User(
            username=username,
            email=email,
            password=hash_password(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@bp.route("/logout")
@login_required
def logout():
    # Logout route
    # Logout the user and redirect to the index page
    logout_user()
    return redirect(url_for("index"))
