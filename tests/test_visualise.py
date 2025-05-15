import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Spending, Category
from app.config import TestingConfig

class TestVisualiseRoutes(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application and the test client
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()  # Drop all tables to start fresh
        db.create_all()

        # Create a test user and log in
        self.user = User(username='testuser', email='test@example.com',gender="prefer not to say")
        self.user.set_password('password')
        db.session.add(self.user)

        # Add test categories and spendings
        self.category_food = Category(category="Food",budget_simple=100, budget_quality=200, budget_luxury=300)
        self.category_transportation = Category(category="Transportation",budget_simple=100, budget_quality=200, budget_luxury=300)
        db.session.add_all([self.category_food, self.category_transportation])
        db.session.commit()

    def login(self):
        # Helper method to log in as the test user
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_spending(self, category, amount, days_ago):
        self.login()  # Log in the client
        # Helper method to add spending data
        spending_date = datetime.now() - timedelta(days=days_ago)
        spending = Spending(
            user_id=self.user.id,
            amount=amount,
            category_id=category.id,
            date=spending_date,
            description=f"Test spending {amount}"
        )
        db.session.add(spending)
        db.session.commit()

    def test_visualise_route(self):
        self.login()  # Log in the client
        # Test the /visualise route
        response = self.client.get('/visualise')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Finance Planner - Visualise Data", response.data)

    def test_spending_data_route(self):
        self.login()  # Log in the client
        # Add sample data for the last 30 days
        self.add_spending(self.category_food, 50.00, 5)  # 5 days ago
        self.add_spending(self.category_transportation, 20.00, 15)  # 15 days ago
        self.add_spending(self.category_food, 30.00, 35)  # 35 days ago (outside the range)

        # Test the /api/spending_data route
        response = self.client.get('/api/spending_data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        # Parse the JSON response
        data = response.get_json()
        self.assertEqual(len(data), 2)  # Only 2 records should be in the last 30 days
        self.assertIn({"category": "Food", "amount": 50.00}, data)
        self.assertIn({"category": "Transportation", "amount": 20.00}, data)

    def test_spending_data_no_spendings(self):
        self.login()  # Log in the client
        # Test the /api/spending_data route with no spendings
        response = self.client.get('/api/spending_data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        # Parse the JSON response
        data = response.get_json()
        self.assertEqual(len(data), 0)  # No spendings should be returned

    def test_spending_data_other_user(self):
        self.login()  # Log in the client
        # Add spending for another user
        other_user = User(username='otheruser', email='other@example.com',gender="prefer not to say")
        other_user.set_password('password')
        db.session.add(other_user)
        db.session.commit()

        other_spending = Spending(
            user_id=other_user.id,
            amount=100.00,
            category_id=self.category_food.id,
            date=datetime.now() - timedelta(days=10),
            description="Other user's spending"
        )
        db.session.add(other_spending)
        db.session.commit()

        # Test that the /api/spending_data route does not include other user's data
        response = self.client.get('/api/spending_data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        # Parse the JSON response
        data = response.get_json()
        self.assertEqual(len(data), 0)  # No spendings for the current user
