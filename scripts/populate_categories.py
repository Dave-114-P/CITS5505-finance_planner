from app import create_app, db
from app.models.incategory import Categoryin

def populate_categoriesin():
    """Populate the categoriesin table if it is empty."""

    # Predefined categories with icons
    predefined_categories = [
        {"id": 1, "category": "Salary", "icon": "salary.png"},
        {"id": 2, "category": "Interest", "icon": "interest.png"},
        {"id": 3, "category": "Cashback", "icon": "cashback.png"}
    ]

    for category_data in predefined_categories:
        try:
            # Check if the category already exists
            existing_category = Categoryin.query.filter_by(id=category_data["id"]).first()
            if not existing_category:
                new_category = Categoryin(
                    id=category_data["id"],
                    category=category_data["category"],
                    icon=category_data["icon"]
                )
                db.session.add(new_category)
                db.session.commit()
                print(f"✅ Added category: {category_data}")
            else:
                print(f"⚠️ Category already exists: {category_data}")
        except Exception as e:
            print(f"❌ Error adding category {category_data}: {str(e)}")

    print("Database URI being used:", db.engine.url)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_categoriesin()
#python -m scripts.populate_categories run this command in terminal to populate the categories table in the database