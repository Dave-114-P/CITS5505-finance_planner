from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy database
db = SQLAlchemy()

# Initialize Flask-Login manager
login_manager = LoginManager()

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    from app.config import Config  # # # Move the import here to avoid circular import issues
    app.config.from_object(Config)

    # Initialize database with app
    db.init_app(app)

    # Initialize login manager with app
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import and register blueprints (routes)
    from app.routes import main, auth, upload, goals, visualise, share, estimation, transaction
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(goals.bp)
    app.register_blueprint(visualise.bp)
    app.register_blueprint(share.bp)
    app.register_blueprint(estimation.bp)
    app.register_blueprint(transaction.bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Define user loader for Flask-Login
    from app.models.user import User    # # # Move the import here to avoid circular import issues
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app