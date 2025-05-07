from app import create_app, db
from app.models.income import Income
from datetime import datetime

def populate_incomes():
    from app.models.incategory import Categoryin
    """Populate the incomes table with sample data."""

    # Check if the categoriesin table is populated
    categories = Categoryin.query.all()
    if not categories:
        print("❌ Categoriesin table is empty. Please populate it first!")
        return

    # Map category names to their IDs
    category_map = {category.category: category.id for category in categories}

    # Sample income data
    sample_incomes = [
        {"user_id": 1, "amount": 50.0, "category_name": "Interest", "date": datetime(2025, 5, 1), "description": "Interest income"},
        {"user_id": 1, "amount": 120.0, "category_name": "Salary", "date": datetime(2025, 5, 2), "description": "Monthly salary"},
        {"user_id": 1, "amount": 200.0, "category_name": "Salary", "date": datetime(2025, 5, 3), "description": "Additional salary"},
        {"user_id": 2, "amount": 350.0, "category_name": "Salary", "date": datetime(2025, 4, 1), "description": "Salary payment"},
        {"user_id": 2, "amount": 25.0, "category_name": "Cashback", "date": datetime(2025, 4, 2), "description": "Cashback reward"},
    ]

    # Add sample data to the database
    for income_data in sample_incomes:
        category_id = category_map.get(income_data["category_name"])
        if not category_id:
            print(f"⚠️ Category '{income_data['category_name']}' not found. Skipping this income entry.")
            continue

        new_income = Income(
            user_id=income_data["user_id"],
            amount=income_data["amount"],
            category_id=category_id,  # Use category ID from the map
            date=income_data["date"],
            description=income_data.get("description")
        )
        db.session.add(new_income)
    
    # Commit the changes
    db.session.commit()
    print("✅ Sample incomes populated successfully!")

if __name__ == "__main__":
    # Initialize the Flask app
    app = create_app()
    # Set up the application context
    with app.app_context():
        # Populate the incomes table
        populate_incomes()