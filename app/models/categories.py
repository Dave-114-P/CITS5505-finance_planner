from app import db

class Category(db.Model):
    # Table name in the database
    __tablename__ = "categories"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=False) 
    budget = db.Column(db.Float, nullable=False)
    lifestyle = db.Column(db.String(20), nullable=False)
    icon = db.Column(db.String(100), nullable=True)  # Optional image URL

    # Relationship with Spendings
    spendings = db.relationship("Spending", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category ID {self.id}: {self.category}>"
    
    def __init__(self, id, category, budget, lifestyle, icon=None):
        self.id = id
        self.category = category
        self.budget = budget
        self.lifestyle = lifestyle
        self.icon = icon
