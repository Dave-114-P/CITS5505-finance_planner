import unittest
from app import create_app, db
from app.config import TestingConfig
from app.models.user import User


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

    def get_csrf_token(self, endpoint="/register"):
        response = self.client.get(endpoint)
        response_text = response.data.decode()

        if 'name="csrf_token" value="' not in response_text:
            raise ValueError(f"CSRF token not found in the response for endpoint {endpoint}!")

        csrf_token = response_text.split('name="csrf_token" value="')[1].split('"')[0]
        return csrf_token

    def test_register(self):
        csrf_token = self.get_csrf_token("/register")
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "csrf_token": csrf_token
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful", response.data)

    def test_login(self):
        # Register a user
        csrf_token = self.get_csrf_token("/register")
        self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "csrf_token": csrf_token
        })

        # Fetch CSRF token for login
        csrf_token = self.get_csrf_token("/login")
        response = self.client.post("/login", data={
            "username": "testuser",
            "password": "password123",
            "csrf_token": csrf_token
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Finance Planner", response.data)


if __name__ == "__main__":
    unittest.main()