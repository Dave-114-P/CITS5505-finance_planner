# User model for login, registration, and role management

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    # Table name in the database
    __tablename__ = "users"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), default="user")

    # One-to-many relationships
    spendings = db.relationship("Spending", backref="user", lazy=True)
    goals = db.relationship("Goal", backref="user", lazy=True)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
    
    # Method to set password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password, password)
