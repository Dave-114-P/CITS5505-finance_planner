from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize SQLAlchemy for spending and category
db = SQLAlchemy()
migrate = Migrate()

# Initialize login manager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Load configuration
    from app.config import Config
    app.config.from_object(Config)

    # Setup multiple database binds
    app.config["SQLALCHEMY_BINDS"] = {
        "spending": "sqlite:///spending.db",
        "category": "sqlite:///category.db"
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize databases
    db.init_app(app)

    # Initialize migration (optional: bind to one db or global db)
    migrate.init_app(app,db)

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import and register blueprints
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


    # Define user loader
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
