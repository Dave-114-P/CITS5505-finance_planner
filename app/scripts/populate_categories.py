from app import create_app, db
from app.models.category import Category

def populate_categories():
    """Populate the categories table if it is empty."""

    # Predefined categories
    predefined_categories = [
        ("Food", "food"),
        ("Transportation", "transportation"),
        ("Entertainment", "entertainment"),
        ("Tuition fees", "tuition_fees"),
        ("Clothing", "clothing"),
        ("Personal", "personal"),
        ("Accomodation", "accomodation"),
    ]

    lifestyles = ["simple", "quality", "luxury"]

    for lifestyle in lifestyles:
        for category_name,key in predefined_categories:
            try:
                # Check if the category already exists
                existing_category = Category.query.filter_by(category=category_name, lifestyle=lifestyle).first()
                if not existing_category:
                    # Add new category with default budget (e.g. 0.0)
                    key = category_name.lower().replace(" ", "_") + "_" + lifestyle.lower()
                    new_category = Category(category=category_name, budget=0.0, lifestyle=lifestyle, key=key)
                    db.session.add(new_category)
                    db.session.commit()
                    print(f"✅ Added category: {category_name} - {lifestyle}")
                else:
                    print(f"⚡ Category already exists: {category_name} - {lifestyle}")

            except Exception as e:
                print(f"❌ Error adding category {category_name} - {lifestyle}: {e}")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_categories()
