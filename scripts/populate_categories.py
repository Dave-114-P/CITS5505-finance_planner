from app import create_app, db
from app.models.categories import Category

def populate_categories():
    """Populate the categories table if it is empty."""
    from app.models.categories import Category

    # Predefined categories
    predefined_categories = {
        "food":"Food",
        "transportation":"Transportation",
        "entertainment":"Entertainment",
        "tuition_fees":"Tuition fees",
        "clothing":"Clothing",
        "personal":"Personal",
        "accommodation":"Accommodation"
    }

    for id, category_name in predefined_categories.items():
        try:
                # Check if the category already exists
                existing_category = Category.query.filter_by(id=id).first()
                if not existing_category:
                    new_category = Category(id=id, category=category_name)
                    db.session.add(new_category)
                    db.session.commit()
                    print(f"✅ Added category: ID={id}, Name={category_name}")
                else:
                    print(f"⚠️ Category already exists: ID={id}, Name={category_name}")
        except Exception as e:
            print(f"❌ Error adding category ID={id}, Name={category_name}: {e}")

    print("Database URI being used:", db.engine.url)
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_categories()
#python -m scripts.populate_categories run this command in terminal to populate the categories table in the database