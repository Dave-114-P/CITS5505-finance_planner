from app import create_app, db
from app.models.categories import Category

def populate_categories():
    """Populate the categories table with predefined data."""
    # Predefined categories with additional fields
    predefined_categories = [
        {"id": 1, "category": "Food", "lifestyle": "simple", "budget": 400, "icon": "food.png"},
        {"id": 2, "category": "Transportation", "lifestyle": "simple", "budget": 150, "icon": "transportation.png"},
        {"id": 3, "category": "Entertainment", "lifestyle": "simple", "budget": 100, "icon": "entertainment.png"},
        {"id": 4, "category": "Tuition fees", "lifestyle": "simple", "budget": 0, "icon": "tuition_fees.png"},
        {"id": 5, "category": "Clothing", "lifestyle": "simple", "budget": 50, "icon": "clothing.png"},
        {"id": 6, "category": "Personal", "lifestyle": "simple", "budget": 50, "icon": "personal.png"},
        {"id": 7, "category": "Accommodation", "lifestyle": "simple", "budget": 700, "icon": "accommodation.png"},
        {"id": 8, "category": "Food", "lifestyle": "quality", "budget": 600, "icon": "food.png"},
        {"id": 9, "category": "Transportation", "lifestyle": "quality", "budget": 200, "icon": "transportation.png"},
        {"id": 10, "category": "Entertainment", "lifestyle": "quality", "budget": 200, "icon": "entertainment.png"},
        {"id": 11, "category": "Tuition fees", "lifestyle": "quality", "budget": 0, "icon": "tuition_fees.png"},
        {"id": 12, "category": "Clothing", "lifestyle": "quality", "budget": 100, "icon": "clothing.png"},
        {"id": 13, "category": "Personal", "lifestyle": "quality", "budget": 100, "icon": "personal.png"},
        {"id": 14, "category": "Accommodation", "lifestyle": "quality", "budget": 1000, "icon": "accommodation.png"},
        {"id": 15, "category": "Food", "lifestyle": "luxury", "budget": 1000, "icon": "food.png"},
        {"id": 16, "category": "Transportation", "lifestyle": "luxury", "budget": 400, "icon": "transportation.png"},
        {"id": 17, "category": "Entertainment", "lifestyle": "luxury", "budget": 600, "icon": "entertainment.png"},
        {"id": 18, "category": "Tuition fees", "lifestyle": "luxury", "budget": 0, "icon": "tuition_fees.png"},
        {"id": 19, "category": "Clothing", "lifestyle": "luxury", "budget": 400, "icon": "clothing.png"},
        {"id": 20, "category": "Personal", "lifestyle": "luxury", "budget": 500, "icon": "personal.png"},
        {"id": 21, "category": "Accommodation", "lifestyle": "luxury", "budget": 2000, "icon": "accommodation.png"}
    ]

    for entry in predefined_categories:
        try:
            # Check if the category already exists
            existing_category = Category.query.filter_by(id=entry["id"]).first()
            if not existing_category:
                new_category = Category(
                    id=entry["id"],
                    category=entry["category"],
                    budget=entry["budget"],
                    lifestyle=entry["lifestyle"],
                    icon=entry["icon"]
                )
                db.session.add(new_category)
                db.session.commit()
                print(f"✅ Added category: ID={entry['id']}, Name={entry['category']}, Lifestyle={entry['lifestyle']}, Budget={entry['budget']}")
            else:
                print(f"⚠️ Category already exists: ID={entry['id']}, Name={entry['category']}, Lifestyle={entry['lifestyle']}")
        except Exception as e:
            print(f"❌ Error adding category ID={entry['id']}, Name={entry['category']}, Lifestyle={entry['lifestyle']}: {e}")

    print("Database URI being used:", db.engine.url)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_categories()
#python -m scripts.populate_categories run this command in terminal to populate the categories table in the database