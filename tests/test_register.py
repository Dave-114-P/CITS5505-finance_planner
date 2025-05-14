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

    def test_register_with_invalid_method(self):
        """
        Test that the /register endpoint does not allow PUT or DELETE requests.
        """
        # Test PUT method
        response_put = self.client.put("/register")
        self.assertEqual(response_put.status_code, 405)
        self.assertIn(b"Method Not Allowed", response_put.data)

        # Test DELETE method
        response_delete = self.client.delete("/register")
        self.assertEqual(response_delete.status_code, 405)
        self.assertIn(b"Method Not Allowed", response_delete.data)

    def test_register_backend_validation(self):
        """
        Test backend validation for various registration scenarios.
        """
        # Missing required fields (e.g., missing email)
        response = self.client.post("/register", data={
            "username": "testuser",
            "gender": "female",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)  # Validation should fail
        self.assertIn(b"This field is required", response.data)

        # Password mismatch
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "gender": "male",
            "password": "password123",
            "confirm_password": "differentpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)  # Validation should fail
        self.assertIn(b"Passwords must match", response.data)

        # Invalid email format
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "123@gmail",
            "gender": "prefer not to say",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid email address.", response.data)

        # Duplicate username
        self.client.post("/register", data={
            "username": "testuser",
            "email": "test1@example.com",
            "gender": "male",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        response_duplicate_username = self.client.post("/register", data={
            "username": "testuser",  # Duplicate username
            "email": "test2@example.com",
            "gender": "female",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response_duplicate_username.status_code, 400)
        self.assertIn(b"Username or Email already exists", response_duplicate_username.data)

        # Duplicate email
        self.client.post("/register", data={
            "username": "user1",
            "email": "test@example.com",
            "gender": "male",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        response_duplicate_email = self.client.post("/register", data={
            "username": "user2",
            "email": "test@example.com",  # Duplicate email
            "gender": "female",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response_duplicate_email.status_code, 400)
        self.assertIn(b"Username or Email already exists", response_duplicate_email.data)

if __name__ == "__main__":
    unittest.main()