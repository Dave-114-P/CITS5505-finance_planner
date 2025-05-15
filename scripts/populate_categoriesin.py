from app import create_app, db
from app.models.incategory import Categoryin

def populate_categoriesin():
    """Populate the categories table if it is empty."""

    # Predefined categories
    predefined_categories = {
        "salary": ("Salary", "salary.png"),
        "interest": ("Interest", "interest.png"),
        "cashback": ("Cashback", "cashback.png")
    }

    for id, (category_name, icon_name) in predefined_categories.items():
        try:
            existing_category = Categoryin.query.filter_by(id=id).first()
            if not existing_category:
                new_category = Categoryin(id=id, category=category_name, icon=icon_name)
                db.session.add(new_category)
                db.session.commit()
                print(f"✅ Added category: ID={id}, Name={category_name}")
            else:
                print(f"⚠️ Category already exists: ID={id}, Name={category_name}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding category ID={id}, Name={category_name}: {str(e)}")

    print("Database URI being used:", db.engine.url)
if __name__ == "__main__":
    app = create_app()
    
    from app.models.incategory import Categoryin
    with app.app_context():
        populate_categoriesin()
#python -m scripts.populate_categoriesin run this command in terminal to populate the categories table in the database