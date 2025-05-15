import unittest
from app import create_app, db
from app.config import TestingConfig
from app.models.user import User  # Import the User model (and others if needed)
from werkzeug.security import generate_password_hash


class LoginTestCase(unittest.TestCase):
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

        # Example: Add a dummy user to the database with hashed password
        dummy_user = User(
            username="testuser",
            email="test@example.com",
            gender="prefer not to say"
        )
        dummy_user.set_password("password123")  # Hash the password
        db.session.add(dummy_user)
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test.
        """
        db.session.remove()  # Remove the database session
        db.drop_all()  # Drop all tables
        self.app_context.pop()  # Pop the application context

    def test_valid_login(self):
        """
        Test login with valid credentials.
        """
        response = self.client.post("/login", data={
            "username": "testuser",
            "password": "password123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")  # Decode response.data to a string
        self.assertIn("Login successful!", response_text)  # Check for success message in response

    def test_invalid_password_login(self):
        """
        Test login with invalid credentials (wrong password).
        """
        response = self.client.post("/login", data={
            "username": "testuser",
            "password": "wrongpassword"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")
        self.assertIn("Invalid username or password", response_text)  # Check for error message

    def test_nonexistent_user_login(self):
        """
        Test login with a non-existent username.
        """
        response = self.client.post("/login", data={
            "username": "nonexistentuser",
            "password": "password123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode("utf-8")
        self.assertIn("Invalid username or password", response_text)  # Check for error message


if __name__ == "__main__":
    unittest.main()