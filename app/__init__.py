from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os
from app.config import DevelopmentConfig

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# CSRF Protection
csrf = CSRFProtect()

def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config_name = DevelopmentConfig
        app.config.from_object(config_name)
    else:
        app.config.from_object(config)

    # Load configuration from the config module
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)  # Initialize CSRF protection
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import and register blueprints
    from app.routes import (
        main, auth, upload, goals, visualise,
        share, estimation, transaction, api, income, profile
    )
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(goals.bp)
    app.register_blueprint(visualise.bp)
    app.register_blueprint(share.bp)
    app.register_blueprint(estimation.bp)
    app.register_blueprint(transaction.bp)
    app.register_blueprint(income.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(profile.bp)

    # Define a root route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Import models (to initialize tables and avoid circular imports)
    from app.models import (
        User, Spending, Category, Goal, Post,
        Categoryin, Income
    )

    # Define user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Health check endpoint
    @app.route("/health")
    def health():
        return {"status": "ok"}, 200
    
     # Import routes after initializing app and db
    with app.app_context():
        db.create_all()

    return app