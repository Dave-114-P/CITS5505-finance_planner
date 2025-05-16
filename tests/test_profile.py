import unittest
from app import create_app, db
from app.models import User
from flask import url_for
from app.config import TestingConfig

class ProfileRouteTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the testing environment
        self.app = create_app(TestingConfig)  # Use testing configuration
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test client
        self.client = self.app.test_client()

        # Add a test user
        self.test_user = User(username='testuser', email='testuser@example.com', gender='male')
        self.test_user.set_password('password')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        # Clean up by removing the database and app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        # Log in as the test user
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })

    def test_profile_update_success(self):
        # Test successful profile update
        self.login()
        response = self.client.post('/profile', data={
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'gender': 'female',
            'password': ''  # Leaving password empty
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated successfully!', response.data)

        # Verify the database has been updated
        db.session.refresh(self.test_user)
        self.assertEqual(self.test_user.username, 'updateduser')
        self.assertEqual(self.test_user.email, 'updateduser@example.com')
        self.assertEqual(self.test_user.gender, 'female')

    def test_profile_update_with_password(self):
        # Test updating the profile with a new password
        self.login()
        response = self.client.post('/profile', data={
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'gender': 'female',
            'password': 'newpassword'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated successfully!', response.data)

        # Verify the password has been updated
        db.session.refresh(self.test_user)
        self.assertTrue(self.test_user.check_password('newpassword'))

    def test_profile_update_validation_failure(self):
        # Log in as the test user
        self.login()

        # Simulate a POST request with an invalid email
        response = self.client.post('/profile', data={
            'username': 'updateduser',
            'email': 'invalid-email',  # Invalid email format
            'gender': 'female',
            'password': ''
        }, follow_redirects=True)

        # Ensure form re-renders with validation error
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address.', response.data)  # Check for validation error message

    def test_profile_access_without_login(self):
        # Test accessing the profile page without logging in
        response = self.client.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)