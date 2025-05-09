from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    share_id = db.Column(db.Integer, db.ForeignKey("shares.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parent_id = db.Column(db.Integer, nullable=True)  # Parent comment ID (nullable)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Define foreign key constraint separately
    __table_args__ = (
        db.ForeignKeyConstraint(['parent_id'], ['comments.id'], name='fk_parent_comment'),
    )

    share = db.relationship("Share", backref="comments")
    user = db.relationship("User")
    parent = db.relationship("Comment", remote_side=[id], backref="replies")  # Self-referencing relationship for nested replies
