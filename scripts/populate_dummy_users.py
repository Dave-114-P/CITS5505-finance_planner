from app import create_app, db
from app.models.user import User  # Import the User model

def populate_users():
    """Populate the users table with sample data."""

    # Sample user data
    sample_users = [
        {"username": "zeyu-wang-123", "password": "23320288", "email": "zeyu-wang-123@gmail.com", "gender": "male"},
        {"username": "Karl-Sue", "password": "24595816", "email": "Karl-Sue@gmail.com", "gender": "female"},
        {"username": "Maxwell2048", "password": "24331475", "email": "Maxwell2048@gmail.com", "gender": "prefer not to say"},
        {"username": "Dave-114-P", "password": "23495103", "email": "Dave-114-P@gmail.com", "gender": "male"},
    ]

    # Add sample data to the database
    for user_data in sample_users:
        # Check if the user already exists
        existing_user = User.query.filter_by(username=user_data["username"]).first()
        if existing_user:
            print(f"⚠️ User '{user_data['username']}' already exists. Skipping...")
            continue

        # Create a new User instance
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            gender=user_data["gender"],
        )
        # Set the user's password (hashed)
        new_user.set_password(user_data["password"])
        
        # Add the user to the session
        db.session.add(new_user)
    
    # Commit the changes
    db.session.commit()
    print("✅ Sample users populated successfully!")