from app import create_app, db
from app.models.spending import Spending
from datetime import datetime

def populate_spendings():
    from app.models.categories import Category
    """Populate the spendings table with sample data."""

    # Check if the categories table is populated
    categories = Category.query.all()
    if not categories:
        print("❌ Categories table is empty. Please populate it first!")
        return

    # Map category names to their IDs
    category_map = {category.category: category.id for category in categories}

    # Sample spending data
    sample_spendings = [
        {"user_id": 1, "amount": 50.0, "category_name": "Food", "date": datetime(2025, 5, 1), "description": "Groceries"},
        {"user_id": 1, "amount": 120.0, "category_name": "Transportation", "date": datetime(2025, 5, 2), "description": "Transportation"},
        {"user_id": 1, "amount": 200.0, "category_name": "Entertainment", "date": datetime(2025, 5, 3), "description": "Entertainment"},
        {"user_id": 2, "amount": 350.0, "category_name": "Food", "date": datetime(2025, 4, 1), "description": "Rent"},
        {"user_id": 2, "amount": 25.0, "category_name": "Tuition fees", "date": datetime(2025, 4, 2), "description": "Snacks"},
    ]

    # Add sample data to the database
    for spending_data in sample_spendings:
        category_id = category_map.get(spending_data["category_name"])
        if not category_id:
            print(f"⚠️ Category '{spending_data['category_name']}' not found. Skipping this spending.")
            continue

        new_spending = Spending(
            user_id=spending_data["user_id"],
            amount=spending_data["amount"],
            category_id=category_id,  # Use category ID from the map
            date=spending_data["date"],
            description=spending_data.get("description")
        )
        db.session.add(new_spending)
    
    # Commit the changes
    db.session.commit()
    print("✅ Sample spendings populated successfully!")

if __name__ == "__main__":
    # Initialize the Flask app
    app = create_app()
    # Set up the application context
    with app.app_context():
        # Populate the spendings table
        populate_spendings()

#python -m scripts.populate_spending run this command in terminal to populate the categories table in the database