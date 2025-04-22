# Model for forum posts, feedback, and sharing

from app import db

class Post(db.Model):
    # Table name in the database
    __tablename__ = "posts"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    likes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Post {self.title}>"