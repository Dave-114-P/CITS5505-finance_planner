from app import db

class Category(db.Model):
    # Table name in the database
    __tablename__ = "categories"

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    lifestyle = db.Column(db.String(20), nullable=False)

    # Relationship with Spendings
    spendings = db.relationship("Spending", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category ID {self.id}: {self.category}>"
    
    def __init__(self, category, budget, lifestyle, id=None):
        self.id = id
        self.category = category
        self.budget = budget
        self.lifestyle = lifestyle
