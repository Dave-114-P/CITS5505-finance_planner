from app import db

class Category(db.Model):
    # Table name in the database
    __tablename__ = "categories"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True) 
    budget_simple = db.Column(db.Float, nullable=False)
    budget_quality = db.Column(db.Float, nullable=False)
    budget_luxury = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(100), nullable=True)  # Optional image URL

    # Relationship with Spendings
    spendings = db.relationship("Spending", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category ID {self.id}: {self.category}>"
    
    def __init__(self, category, budget_simple, budget_quality, budget_luxury, icon=None):
        self.category = category
        self.budget_simple = budget_simple
        self.budget_quality = budget_quality
        self.budget_luxury = budget_luxury
        self.icon = icon
