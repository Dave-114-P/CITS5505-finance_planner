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
    # These lines are only for development and should be removed in production
    with app.app_context():
        db.drop_all()
        db.create_all()
        from scripts import (
            populate_dummy_users,
            populate_categoriesin,
            populate_income,
            populate_spending,
            populate_categories,
        )
        # Populate the database with sample data
        populate_dummy_users.populate_users()
        populate_categoriesin.populate_categoriesin()
        populate_categories.populate_categories()
        populate_income.populate_incomes()
        populate_spending.populate_spendings()
    app.run(host='127.0.0.1',port=5000,debug=True)