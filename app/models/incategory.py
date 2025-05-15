from app import db

class Categoryin(db.Model):
    # Table name in the database
    __tablename__ = "categoriesin"

    # Columns
    id = db.Column(db.String(50), primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True)
    icon = db.Column(db.String(100), nullable=True)  # Optional image URL

    # Relationship with Spendings
    incomes = db.relationship("Income", back_populates="category", lazy="select")

    def __repr__(self):
        return f"<Category ID {self.id}: {self.category}>"
    
    def __init__(self, category, id, icon=None):
        self.id = id
        self.category = category
        self.icon = icon