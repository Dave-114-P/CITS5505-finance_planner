from app import create_app, db
from app.models.income import Income
from datetime import datetime

def populate_incomes():
    from app.models.incategory import Categoryin
    """Populate the spendings table with sample data."""
    # Check if the categories table is populated
    categories = Categoryin.query.all()
    if not categories:
        print("❌ Categories table is empty. Please populate it first!")
        return

    sample_spendings = [
        {"user_id": 1, "amount": 50.0, "category_id": "interest", "date": datetime(2025, 5, 1), "description": "Interest"},
        {"user_id": 1, "amount": 120.0, "category_id": "salary", "date": datetime(2025, 5, 2), "description": "Salary"},
        {"user_id": 1, "amount": 200.0, "category_id": "salary", "date": datetime(2025, 5, 3), "description": "Salary"},
        {"user_id": 2, "amount": 350.0, "category_id": "salary", "date": datetime(2025, 4, 1), "description": "Salary"},
        {"user_id": 2, "amount": 25.0, "category_id": "cashback", "date": datetime(2025, 4, 2), "description": "Cashback"},
    ]

    # Add sample data to the database
    for spending_data in sample_spendings:
        new_spending = Income(
            user_id=spending_data["user_id"],
            amount=spending_data["amount"],
            category_id=spending_data["category_id"],
            date=spending_data["date"],
            description=spending_data.get("description")
        )
        db.session.add(new_spending)
    
    # Commit the changes
    db.session.commit()
    print("✅ Sample spendings populated successfully!")
if __name__ == "__main__":
    from app.models.income import Income
    # Initialize the Flask app
    app = create_app()
     # Set up the application context
    with app.app_context():
        # Populate the spendings table
        populate_incomes()