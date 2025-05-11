import unittest
from app import create_app, db
from app.config import TestingConfig
from app.models.user import User  # Import the User model (and others if needed)

class BasicTest(unittest.TestCase):
    def setUp(self):
        """
        Set up a test app and database before each test.
        """
        # Create the Flask app with a testing configuration
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()  # Test client for simulating requests
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push the application context for database operations

        # Create the database and populate with dummy data
        db.create_all()

        # Example: Add a dummy user to the database
        dummy_user = User(username="testuser", email="test@example.com", password="password123")
        db.session.add(dummy_user)
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test.
        """
        db.session.remove()  # Remove the database session
        db.drop_all()  # Drop all tables
        self.app_context.pop()  # Pop the application context

    def test_user_creation(self):
        """
        Test that a user can be created successfully.
        """
        user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(user)  # Check if the user exists
        self.assertEqual(user.email, "test@example.com")  # Verify user details

    def test_login(self):
        """
        Test the login functionality.
        """
        response = self.client.post("/login", data={
            "username": "testuser",
            "password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Finance Planner", response.data)  # Check for expected content in response

if __name__ == "__main__":
    unittest.main()