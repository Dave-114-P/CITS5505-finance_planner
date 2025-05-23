from app import create_app, db
from app.models.categories import Category

def populate_categories():
    """Populate the categories table with predefined data."""
    # Predefined categories with budgets for different lifestyles
    predefined_categories = [
        {
           "category": "Food", "budget_simple": 400, "budget_quality": 600, "budget_luxury": 1000, "icon": "food.png"
        },
        {
            "category": "Transportation", "budget_simple": 150, "budget_quality": 200, "budget_luxury": 400, "icon": "transportation.png"
        },
        {
            "category": "Entertainment", "budget_simple": 100, "budget_quality": 200, "budget_luxury": 600, "icon": "entertainment.png"
        },
        {
            "category": "Tuition fees", "budget_simple": 0, "budget_quality": 0, "budget_luxury": 0, "icon": "tuition_fees.png"
        },
        {
            "category": "Clothing", "budget_simple": 50, "budget_quality": 100, "budget_luxury": 400, "icon": "clothing.png"
        },
        {
           "category": "Personal", "budget_simple": 50, "budget_quality": 100, "budget_luxury": 500, "icon": "personal.png"
        },
        {
            "category": "Accommodation", "budget_simple": 700, "budget_quality": 1000, "budget_luxury": 2000, "icon": "accommodation.png"
        }
    ]

    for entry in predefined_categories:
        try:
            # Check if the category already exists
            existing_category = Category.query.filter_by(category=entry["category"]).first()
            if not existing_category:
                new_category = Category(
                    category=entry["category"],
                    budget_simple=entry["budget_simple"],
                    budget_quality=entry["budget_quality"],
                    budget_luxury=entry["budget_luxury"],
                    icon=entry["icon"]
                )
                db.session.add(new_category)
                db.session.commit()
                print(f"✅ Added category: Name={entry['category']}")
            else:
                print(f"⚠️ Category already exists: ID={existing_category.id}, Name={existing_category.category}")
        except Exception as e:
            print(f"❌ Error adding category Name={entry['category']}: {e}")

    print("Database URI being used:", db.engine.url)
#python -m scripts.populate_categories run this command in terminal to populate the categories table in the database