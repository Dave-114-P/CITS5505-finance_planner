from app import create_app, db
from app.models.spending import Spending
from datetime import datetime, timedelta

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

    # Sample spending data for each user
    sample_spendings = [
        {"category_name": "Food", "amounts": [50, 70, 100], "description": "Groceries"},
        {"category_name": "Transportation", "amounts": [15, 30, 50], "description": "Transport costs"},
        {"category_name": "Entertainment", "amounts": [30, 40, 60], "description": "Movies and games"},
        {"category_name": "Tuition fees", "amounts": [20, 25, 40], "description": "College expenses"},
        {"category_name": "Clothing", "amounts": [50, 70, 90], "description": "Clothing shopping"},
        {"category_name": "Personal", "amounts": [25, 35, 50], "description": "Personal care"},
        {"category_name": "Accommodation", "amounts": [200, 300, 500], "description": "Rent payment"},
    ]

    # Generate 10 spendings per user
    users = [1, 2, 3, 4]  # User IDs
    start_date = datetime(2025, 5, 1)

    for user_id in users:
        spending_count = 0
        for spending_data in sample_spendings:
            if spending_count >= 10:
                break  # Limit to 10 spendings per user

            category_id = category_map.get(spending_data["category_name"])
            if not category_id:
                print(f"⚠️ Category '{spending_data['category_name']}' not found. Skipping...")
                continue

            for amount in spending_data["amounts"]:
                if spending_count >= 10:
                    break  # Stop when we reach 10 spendings

                new_spending = Spending(
                    user_id=user_id,
                    amount=amount,
                    category_id=category_id,
                    date=start_date + timedelta(days=spending_count),
                    description=f"{spending_data['description']} - User {user_id}"
                )
                db.session.add(new_spending)
                spending_count += 1
    
    # Commit the changes
    db.session.commit()
    print("✅ Sample spendings populated successfully!")