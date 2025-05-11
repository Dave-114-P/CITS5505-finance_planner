import unittest
from app import create_app, db
from app.config import TestingConfig


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_with_valid_data(self):
        # Test registration with all valid fields
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "gender": "male",  # Optional field provided
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)

        # Assert that the registration is successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful", response.data)

    def test_register_with_missing_required_fields(self):
        # Test registration with missing required fields (e.g., missing email)
        response = self.client.post("/register", data={
            "username": "testuser",
            "gender": "male",  # Optional field provided
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)

        # Assert that the server responds with a 400 due to validation errors
        self.assertEqual(response.status_code, 400)  # Validation should fail
        self.assertIn(b"This field is required", response.data)

    def test_register_with_password_mismatch(self):
        # Test registration with mismatched passwords
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "gender": "male",  # Optional field provided
            "password": "password123",
            "confirm_password": "differentpassword"
        }, follow_redirects=True)

        # Assert that the server responds with a 400 due to password mismatch
        self.assertEqual(response.status_code, 400)  # Validation should fail
        self.assertIn(b"Passwords must match", response.data)

    def test_register_with_optional_gender_field(self):
        # Test registration with the optional gender field omitted
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)

        # Assert that the registration is successful even without the gender field
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful", response.data)


if __name__ == "__main__":
    unittest.main()