from app import db
from datetime import datetime

class Share(db.Model):
    __tablename__ = "shares"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Sender user ID
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # Receiver user ID (nullable)
    category = db.Column(db.String(50), nullable=True)  # Category (nullable)
    title = db.Column(db.String(100), nullable=True)  # Title
    content = db.Column(db.Text, nullable=True)  # Content
    link = db.Column(db.String(255), nullable=True)  # Optional link
    image = db.Column(db.String(255), nullable=True)  # Uploaded image filename
    is_public = db.Column(db.Boolean, default=False)  # Public or private
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Share timestamp

    sender = db.relationship("User", foreign_keys=[sender_id], backref="shares_sent")
    receiver = db.relationship("User", foreign_keys=[receiver_id], backref="shares_received")

    def __repr__(self):
        return f"<Share id={self.id} sender={self.sender_id} receiver={self.receiver_id} public={self.is_public}>"
