# User model for login, registration, and role management

from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # Table name in the database
    __tablename__ = "users"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    role = db.Column(db.String(20), default="user")

    # One-to-many relationships
    spendings = db.relationship("Spending", backref="user", lazy=True)
    goals = db.relationship("Goal", backref="user", lazy=True)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
