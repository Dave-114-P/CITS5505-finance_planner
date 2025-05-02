from app import db

class Category(db.Model):
    # Table name in the database
    __tablename__ = "categories"

    # Columns
    id = db.Column(db.String(30), primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True)

    # Relationship with Spendings
    spendings = db.relationship("Spending", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category ID {self.id}: {self.category}>"
    
    def __init__(self, category, id):
        self.id = id
        self.category = category