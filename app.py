# Entry point for the Finance Planner app

from app import create_app
from app.config import DevelopmentConfig
from app import db
from flask_migrate import Migrate

# Create the Flask app instance with the configuration
app = create_app(DevelopmentConfig)
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Run the app in debug mode for development
    app.run(debug=True)