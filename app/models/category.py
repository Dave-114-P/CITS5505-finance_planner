from app import db

class Category(db.Model):
    # Table name in the database
    __tablename__ = "categories"

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Auto increment integer ID
    category = db.Column(db.String(30), nullable=False, unique=False)
    lifestyle = db.Column(db.String(30), nullable=False)
    budget = db.Column(db.Float, nullable=True)
    key = db.Column(db.String(30), nullable=False, unique=True)  # New key field for images
    # Relationship with Spendings
    spendings = db.relationship('Spending', back_populates='category')

    def __repr__(self):
        return f"<Category ID {self.id}: {self.category}>"
