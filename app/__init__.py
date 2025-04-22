# Initialize the Flask app, database, and login manager

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Initialize SQLAlchemy database
db = SQLAlchemy()

# Initialize Flask-Login manager
login_manager = LoginManager()

def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Configure app settings
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database with app
    db.init_app(app)

    # Initialize login manager with app
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import and register blueprints (routes)
    from app.routes import auth, upload, goals, visualise, share
    app.register_blueprint(auth.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(goals.bp)
    app.register_blueprint(visualise.bp)
    app.register_blueprint(share.bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Define user loader for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app