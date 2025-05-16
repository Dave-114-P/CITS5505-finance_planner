from app import create_app, db
from datetime import datetime, timedelta

def populate_incomes():
    from app.models.income import Income  # Assuming Income model exists
    from app.models.incategory import Categoryin  # Assuming categories are also used for incomes

    """Populate the incomes table with sample data."""

    # Check if the categories table is populated
    categories = Categoryin.query.all()
    if not categories:
        print("❌ Categories table is empty. Please populate it first!")
        return

    # Map category names to their IDs
    category_map = {category.category: category.id for category in categories}

    # Sample income data for all users
    sample_incomes = [
        # User 1
        {"user_id": 1, "amount": 120.0, "category_name": "Salary", "date": datetime(2025, 5, 5), "description": "Monthly salary"},
        {"user_id": 1, "amount": 60.0, "category_name": "Interest", "date": datetime(2025, 5, 8), "description": "Savings interest"},
        {"user_id": 1, "amount": 150.0, "category_name": "Salary", "date": datetime(2025, 5, 10), "description": "Performance bonus"},
        {"user_id": 1, "amount": 35.0, "category_name": "Cashback", "date": datetime(2025, 5, 12), "description": "Shopping cashback"},
        {"user_id": 1, "amount": 80.0, "category_name": "Interest", "date": datetime(2025, 5, 14), "description": "Fixed deposit interest"},

        # User 2
        {"user_id": 2, "amount": 300.0, "category_name": "Salary", "date": datetime(2025, 5, 3), "description": "April salary"},
        {"user_id": 2, "amount": 25.0, "category_name": "Cashback", "date": datetime(2025, 5, 5), "description": "Online cashback"},
        {"user_id": 2, "amount": 70.0, "category_name": "Interest", "date": datetime(2025, 5, 8), "description": "Dividend interest"},
        {"user_id": 2, "amount": 320.0, "category_name": "Salary", "date": datetime(2025, 5, 11), "description": "May salary"},
        {"user_id": 2, "amount": 100.0, "category_name": "Interest", "date": datetime(2025, 5, 13), "description": "Bond interest"},

        # User 3
        {"user_id": 3, "amount": 400.0, "category_name": "Salary", "date": datetime(2025, 5, 2), "description": "Monthly salary"},
        {"user_id": 3, "amount": 50.0, "category_name": "Interest", "date": datetime(2025, 5, 6), "description": "Savings account interest"},
        {"user_id": 3, "amount": 200.0, "category_name": "Salary", "date": datetime(2025, 5, 9), "description": "Performance bonus"},
        {"user_id": 3, "amount": 30.0, "category_name": "Cashback", "date": datetime(2025, 5, 11), "description": "Credit card cashback"},
        {"user_id": 3, "amount": 90.0, "category_name": "Interest", "date": datetime(2025, 5, 14), "description": "Fixed deposit interest"},

        # User 4
        {"user_id": 4, "amount": 450.0, "category_name": "Salary", "date": datetime(2025, 5, 1), "description": "Monthly salary"},
        {"user_id": 4, "amount": 40.0, "category_name": "Cashback", "date": datetime(2025, 5, 4), "description": "Shopping cashback"},
        {"user_id": 4, "amount": 80.0, "category_name": "Interest", "date": datetime(2025, 5, 7), "description": "Savings interest"},
        {"user_id": 4, "amount": 100.0, "category_name": "Interest", "date": datetime(2025, 5, 10), "description": "Bond interest"},
        {"user_id": 4, "amount": 350.0, "category_name": "Salary", "date": datetime(2025, 5, 12), "description": "Bonus salary"},
    ]

    # Add sample data to the database
    for income_data in sample_incomes:
        category_id = category_map.get(income_data["category_name"])
        if not category_id:
            print(f"⚠️ Category '{income_data['category_name']}' not found. Skipping this income.")
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