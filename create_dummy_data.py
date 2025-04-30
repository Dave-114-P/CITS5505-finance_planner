from app import create_app, db
from app.models.spending import Spending
from datetime import datetime, timedelta
import random
#this file is used to create dummy data for the database - finance.db
# and is not part of the main application logic
# This script is used to create dummy data for the database
# It generates random spending records for a user over the last 30 days
# and adds them to the database
# The script should be run in the context of the Flask application
# to ensure that the database connection is properly established
# It only runs if we explicitly call it in the terminal
app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user_id = 1  # Dummy user
    today = datetime.today().date()

    for i in range(30):
        day = today - timedelta(days=i)
        spending = Spending(
            user_id=user_id,
            amount=round(random.uniform(10, 200), 2),
            category=random.choice(["Food", "Transport", "Shopping"]),
            date=day,
            description="Auto-generated"
        )
        db.session.add(spending)

    db.session.commit()
    print("✅ Dummy data added.")