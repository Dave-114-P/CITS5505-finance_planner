from app import db
from app.models.category import Category

class Spending(db.Model):
    __tablename__ = "spendings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category_key = db.Column(db.String(30))

    
    category = db.relationship('Category', back_populates='spendings', foreign_keys=[category_id])

    def __repr__(self):
        return f"<Spending {self.id}: {self.amount}>"

    @staticmethod
    def get_3_largest_spendings(user_id, limit=3):
        spendings = (
            Spending.query.filter_by(user_id=user_id)
            .order_by(Spending.amount.desc())
            .limit(limit)
            .all()
        )
        if not spendings:
            return None

        if len(spendings) < 1:
            return {"message": "User has less than 1 transactions.", "spendings": spendings}

        return spendings

    @staticmethod
    def get_3_most_recent_transactions(user_id, limit=3):
        transactions = (
            Spending.query.filter_by(user_id=user_id)
            .order_by(Spending.date.desc())
            .limit(limit)
            .all()
        )
        if not transactions:
            return {"message": "No transactions found for the user."}

        return transactions

def __init__(self, user_id, amount, category_id, date, description, category_key=None):
        self.user_id      = user_id
        self.amount       = amount
        self.category_id  = category_id
        self.date         = date
        self.description  = description
        self.category_key = category_key
