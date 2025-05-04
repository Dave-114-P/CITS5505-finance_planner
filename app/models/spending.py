from app import db

class Spending(db.Model):
    # Table name in the database
    __tablename__ = "spendings"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.String(30), db.ForeignKey("categories.id"), nullable=False)

    def __repr__(self):
        return f"<Spending {self.id}: {self.amount}>"
    
    @staticmethod
    def get_3_largest_spendings(user_id, limit=3):
        """Get the top N largest spendings for a given user."""
        spendings = (
            Spending.query.filter_by(user_id=user_id)
            .order_by(Spending.amount.desc())
            .limit(limit)
            .all()
        )
        
        if not spendings:
            return None  # No transactions found

        if len(spendings) < 1:
            return {"message": "User has less than 1 transactions.", "spendings": spendings}

        return spendings
    
    @staticmethod
    def get_3_most_recent_transactions(user_id, limit=3):
        """Get the top N most recent transactions for a given user."""
        transactions = (
            Spending.query.filter_by(user_id=user_id)
            .order_by(Spending.date.desc())  # Assuming there's a 'date' column
            .limit(limit)
            .all()
        )
        
        if not transactions:
            return {"message": "No transactions found for the user."}

        return transactions
    
    def __init__(self, user_id, amount, category_id, date, description=None):
        self.user_id = user_id
        self.amount = amount
        self.category_id = category_id
        self.date = date
        self.description = description