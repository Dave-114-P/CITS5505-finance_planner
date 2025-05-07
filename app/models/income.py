from app import db

class Income(db.Model):
    # Table name in the database
    __tablename__ = "incomes"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.String(30), db.ForeignKey("categoriesin.id"), nullable=False)

    # Relationship with Categoryin
    category = db.relationship("Categoryin", back_populates="incomes", lazy="select")
    
    def __repr__(self):
        return f"<Income {self.id}: {self.amount}>"
    
    def __init__(self, user_id, amount, category_id, date, description=None):
        self.user_id = user_id
        self.amount = amount
        self.category_id = category_id
        self.date = date
        self.description = description