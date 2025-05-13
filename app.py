# Entry point for the Finance Planner app

from app import create_app
from app.config import DevelopmentConfig
from app import db
from flask_migrate import Migrate

# Create the Flask app instance with the configuration
app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Run the app in debug mode for development
    # Use the app's context to drop and create all tables
    with app.app_context():
        db.drop_all()
        db.create_all()
        from scripts import populate_categories
        populate_categories.populate_categories()
        from scripts import populate_categoriesin
        populate_categoriesin.populate_categoriesin()
    app.run(debug=True)