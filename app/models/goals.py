# Model for savings goals: target amount, years, plan

from app import db

class Goal(db.Model):
    # Table name in the database
    __tablename__ = "goals"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    years = db.Column(db.Integer, nullable=False)
    monthly_plan = db.Column(db.Float)

    def __repr__(self):
        return f"<Goal Target: {self.target_amount}>"