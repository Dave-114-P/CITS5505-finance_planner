# Entry point for the Finance Planner app

from app import create_app

# Hardcode configuration settings (previously in config.py)
class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = "your-secret-key-here"  # Replace with a secure key in production

    # SQLite database URI
    SQLALCHEMY_DATABASE_URI = "sqlite:///finance.db"

    # Disable SQLAlchemy modification tracking for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Create the Flask app instance with the configuration
app = create_app()
app.config.from_object(Config)
app.config['DEBUG'] = True  # Enable debug mode for development

if __name__ == "__main__":
    # Run the app in debug mode for development
    app.run(debug=True)