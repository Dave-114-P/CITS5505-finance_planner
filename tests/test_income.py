import unittest
from flask import session
from app import create_app, db
from app.models import User, Categoryin, Income
from datetime import date, timedelta
from app.config import TestingConfig

class IncomeRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test app and database
        self.app = create_app(TestingConfig)  # Ensure 'testing' config is set for isolated db
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test client for sending requests
        self.client = self.app.test_client()

        # Create a test user and category
        self.test_user = User(email='test@example.com', gender="prefer not to say", username="testuser")
        self.test_user.set_password('password')
        self.test_category = Categoryin(category="Salary")
        db.session.add(self.test_user)
        db.session.add(self.test_category)
        db.session.commit()

    def tearDown(self):
        # Tear down the database and app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        # Helper method to log in as the test user
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })

    def test_income_creation_success(self):
        # Test successful income creation
        self.login()
        response = self.client.post('/income', data={
            'amount': 1000.50,
            'category': 'Salary',
            'date': date.today().strftime('%Y-%m-%d'),  # Use the current date
            'description': 'Monthly salary'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Expect a successful response
        self.assertIn(b'Income uploaded successfully', response.data)  # Flash message should appear

        # Check if the income entry was added to the database
        income = Income.query.filter_by(user_id=self.test_user.id).first()
        self.assertIsNotNone(income)
        self.assertEqual(income.amount, 1000.50)
        self.assertEqual(income.category_id, self.test_category.id)
        self.assertEqual(income.description, 'Monthly salary')

    def test_income_creation_invalid_category(self):
        # Test income creation with an invalid category
        self.login()
        response = self.client.post('/income', data={
            'amount': 1000.50,
            'category': 'InvalidCategory',  # Invalid category
            'date': date.today().strftime('%Y-%m-%d'),
            'description': 'Test description'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Form re-renders on failure
        self.assertIn(b'Not a valid choice.', response.data)  # Flash message for invalid category

        # Ensure no income entry was created
        income_count = Income.query.filter_by(user_id=self.test_user.id).count()
        self.assertEqual(income_count, 0)

    def test_income_creation_invalid_amount(self):
        # Test income creation with an invalid amount (e.g., negative or zero)
        self.login()
        response = self.client.post('/income', data={
            'amount': -50,  # Invalid amount
            'category': 'Salary',
            'date': date.today().strftime('%Y-%m-%d'),
            'description': 'Test description'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Form re-renders on failure
        self.assertIn(b'Amount must be greater than zero.', response.data)  # Flash message for invalid amount

        # Ensure no income entry was created
        income_count = Income.query.filter_by(user_id=self.test_user.id).count()
        self.assertEqual(income_count, 0)

    def test_income_creation_future_date(self):
        # Test income creation with a date in the future
        self.login()
        future_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')  # Tomorrow's date
        response = self.client.post('/income', data={
            'amount': 500,
            'category': 'Salary',
            'date': future_date,  # Invalid future date
            'description': 'Future income test'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Form re-renders on failure
        self.assertIn(b'The date cannot be in the future.', response.data)  # Flash message for future date

        # Ensure no income entry was created
        income_count = Income.query.filter_by(user_id=self.test_user.id).count()
        self.assertEqual(income_count, 0)