# Model for user expense records (daily/monthly)

from app import db

class Spending(db.Model):
    # Table name in the database
    __tablename__ = "spendings"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Spending {self.category}: {self.amount}>"