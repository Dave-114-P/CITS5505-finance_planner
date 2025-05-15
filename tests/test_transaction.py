import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Spending, Income, Category, Categoryin
from flask_login import login_user
from app.config import TestingConfig

class TestTransactionRoute(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application and the test client
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()  # Drop all tables to start fresh
        db.create_all()

        # Create a test user
        self.user = User(username='testuser', email='test@gmail.com',gender="male")
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

        # Add sample spendings and incomes
        self.add_sample_transactions()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        self.client.post("/login", data={"username": "testuser", "password": "password"})

    def add_sample_transactions(self):
        self.login()
        # Add spendings for the current and previous months
        current_date = datetime.utcnow()
        last_month_date = current_date - timedelta(days=30)
        last_3month_date = current_date - timedelta(days=90)
        db.session.add(Category(category="Groceries",budget_simple=100, budget_quality=200, budget_luxury=300,icon="food.png"))
        db.session.add(Category(category="Transport",budget_simple=50, budget_quality=100, budget_luxury=150,icon="transportation.png"))
        db.session.add(Categoryin(category="Salary",icon="salary.png"))
        db.session.add(Categoryin(category="Freelance",icon="interest.png"))
        db.session.add(Spending(user_id=self.user.id, amount=100, date=current_date,category_id=1, description='Groceries'))
        db.session.add(Spending(user_id=self.user.id, amount=50, date=last_month_date,category_id=2, description='Transport'))
        
        # Add incomes for the current and previous months
        db.session.add(Income(user_id=self.user.id, amount=500, date=current_date,category_id=1, description='Salary'))
        db.session.add(Income(user_id=self.user.id, amount=200, date=last_3month_date,category_id=2, description='Freelance'))
        db.session.add(Income(user_id=self.user.id, amount=200, date=last_month_date,category_id=2, description='Freelance'))

        db.session.commit()

    def test_default_view(self):
        self.login()
        # Test the default view (GET request with no filters)
        response = self.client.get('/transaction')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Groceries', response.data)
        self.assertIn(b'Salary', response.data)

    def test_filter_by_month(self):
        self.login()
        # Test filtering by a specific month and year
        current_date = datetime.utcnow()
        response = self.client.get(f'/transaction?month={current_date.month}&year={current_date.year}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Groceries', response.data)
        self.assertIn(b'Salary', response.data)

        # Test filtering for the previous month
        last_month_date = current_date - timedelta(days=30)
        response = self.client.get(f'/transaction?month={last_month_date.month}&year={last_month_date.year}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transport', response.data)
        self.assertIn(b'Freelance', response.data)

    def test_filter_period(self):
        self.login()
        # Test filtering for a specific period using POST
        response = self.client.post('/transaction', data={'period': 'month'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Groceries', response.data)
        self.assertIn(b'Salary', response.data)

    def test_past_months_dropdown(self):
        self.login()
        current_date = datetime.utcnow()
        # Test filtering for the previous month
        last_month_date = current_date - timedelta(days=30)
        # Test that the past months dropdown is generated correctly
        response = self.client.get(f'/transaction?month={last_month_date.month}&year={last_month_date.year}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Past Months', response.data)  # Ensure the dropdown section is rendered
        self.assertIn(b'Transport', response.data)
        self.assertIn(b'Freelance', response.data)

    def test_no_transactions(self):
        self.login()
        # Test behavior when there are no spendings or incomes
        db.session.query(Spending).delete()
        db.session.query(Income).delete()
        db.session.commit()

        response = self.client.get('/transaction')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Groceries', response.data)
        self.assertNotIn(b'Salary', response.data)
        # Remove all HTML comments from the response data
        import re
        response_text = re.sub(b'<!--.*?-->', b'', response.data, flags=re.DOTALL)

        # Perform the assertion after stripping comments
        self.assertNotIn(b'Past Months', response_text)  # Dropdown should not be shown