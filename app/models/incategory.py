from app import db

class Categoryin(db.Model):
    # Table name in the database
    __tablename__ = "categoriesin"

    # Columns
    id = db.Column(db.String(30), primary_key=True) #salary, bonus, etc.
    category = db.Column(db.String(50), nullable=False, unique=True) #Food, Transportation, etc.

    # Relationship with Spendings
    incomes = db.relationship("Income", back_populates="category", lazy="select")

    def __repr__(self):
        return f"<Category ID {self.id}: {self.category}>"
    
    def __init__(self, category, id):
        self.id = id
        self.category = category