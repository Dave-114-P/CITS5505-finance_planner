from app import create_app, db
from app.models.incategory import Categoryin

def populate_categoriesin():
    """Populate the categories table if it is empty."""

    # Predefined categories with their corresponding icons
    predefined_categories = {
        1: {"category": "Salary", "icon": "salary.png"},
        2: {"category": "Interest", "icon": "interest.png"},
        3: {"category": "Cashback", "icon": "cashback.png"},
    }

    for id, details in predefined_categories.items():
        category_name = details["category"]
        icon_name = details["icon"]
        
        try:
            # Check if the category already exists
            existing_category = Categoryin.query.filter_by(id=id).first()
            if not existing_category:
                new_category = Categoryin(id=id, category=category_name, icon=icon_name)
                db.session.add(new_category)
                db.session.commit()
                print(f"✅ Added category: ID={id}, Name={category_name}, Icon={icon_name}")
            else:
                print(f"⚠️ Category already exists: ID={id}, Name={category_name}, Icon={icon_name}")
        except Exception as e:
            print(f"❌ Error adding category ID={id}, Name={category_name}, Icon={icon_name}: {str(e)}")

    print("Database URI being used:", db.engine.url)