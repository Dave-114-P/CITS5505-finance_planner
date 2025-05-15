import unittest
from flask import session
from app import create_app, db
from app.models import User, Category, Spending
from app.config import TestingConfig
from datetime import datetime

class EstimationRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test app and database
        self.app = create_app(TestingConfig)  # Ensure 'testing' config is set for isolated db
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test client for sending requests
        self.client = self.app.test_client()

        # Create a test user
        self.test_user = User(username="testuser", email='test@example.com',gender="prefer not to say")
        self.test_user.set_password('password')  # Hash the password
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        # Tear down database and app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        # Helper method to log in as the test user
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })

    def test_lifestyle_selection_success(self):
        # Test successful lifestyle selection
        self.login()
        response = self.client.post('/estimation', data={'lifestyle': 'simple'})
        self.assertEqual(response.status_code, 302)  # Expect redirect
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['lifestyle'], 'simple')
    
    def test_lifestyle_selection_failure(self):
        # Test invalid lifestyle selection (e.g., no selection made)
        self.login()
        response = self.client.post('/estimation', data={})
        self.assertEqual(response.status_code, 200)  # Form errors render the same template
        self.assertIn(b'Invalid lifestyle selection. Please try again.', response.data)

    def test_change_lifestyle(self):
        # Test resetting the lifestyle selection
        self.login()
        with self.client.session_transaction() as sess:
            sess['lifestyle'] = 'quality'

        response = self.client.post('/estimation/change_lifestyle')
        self.assertEqual(response.status_code, 302)  # Expect redirect
        with self.client.session_transaction() as sess:
            self.assertNotIn('lifestyle', sess)

    def test_category_budget_calculation(self):
        # Test category budget and percentage calculation
        self.login()

        # Add test categories and spendings to the database
        category = Category(category='Food', budget_simple=100, budget_quality=200, budget_luxury=300)
        db.session.add(category)
        db.session.commit()
        spending = Spending(user_id=self.test_user.id, category_id=1, amount=50, date=datetime(2025,5,1))
        db.session.add(spending)
        db.session.commit()

        # Set the selected lifestyle in the session
        with self.client.session_transaction() as sess:
            sess['lifestyle'] = 'simple'

        response = self.client.get('/estimation')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'50.0%', response.data)  # Check if the percentage is correctly calculated and displayed