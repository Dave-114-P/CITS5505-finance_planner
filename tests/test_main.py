import unittest
from datetime import datetime
from flask import url_for
from app import create_app, db
from app.models import User, Spending, Income, Goal
from app.config import TestingConfig

class ResetAllRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test app and database
        self.app = create_app(TestingConfig)  # Use the testing configuration
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test client
        self.client = self.app.test_client()

        # Create a test user
        self.test_user = User(username='testuser', email='testuser@example.com', gender="male")
        self.test_user.set_password("password")
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        # Tear down the database and app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        # Log in as the test user
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })

    def test_reset_all_success(self):
        # Test successful reset of all data
        self.login()

        # Add sample spending and income data
        spending = Spending(user_id=self.test_user.id, amount=100, date=datetime(2025, 5, 1), category_id=1)
        income = Income(user_id=self.test_user.id, amount=500, date=datetime(2025, 5, 1), category_id=1)
        db.session.add(spending)
        db.session.add(income)
        db.session.commit()

        response = self.client.post('/reset_all', data={'confirm': True}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All data has been reset successfully.', response.data)

        # Ensure all data is deleted
        self.assertEqual(Spending.query.filter_by(user_id=self.test_user.id).count(), 0)
        self.assertEqual(Income.query.filter_by(user_id=self.test_user.id).count(), 0)

    def test_reset_all_no_data(self):
        # Test resetting when there's no data to reset
        self.login()

        response = self.client.post('/reset_all', data={'confirm': True}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No data to reset.', response.data)

    def test_reset_all_not_logged_in(self):
        # Test accessing the reset_all route without being logged in
        response = self.client.get('/reset_all', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_reset_all_form_validation_failure(self):
        # Test form submission with validation failure
        self.login()

        response = self.client.post('/reset_all', data={})  # Missing 'confirm' field
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'An error occurred. Please try again.', response.data)