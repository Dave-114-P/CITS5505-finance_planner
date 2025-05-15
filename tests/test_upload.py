import unittest
from datetime import date, timedelta
from app import create_app, db
from app.models import User, Spending, Category
from app.config import TestingConfig

class TestUploadRoute(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application and the test client
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()  # Drop all tables to start fresh
        db.create_all()

        # Create a test user and login
        self.user = User(username='testuser', email='test@example.com',gender="prefer not to say")
        self.user.set_password('password')
        db.session.add(self.user)

        # Add test categories
        self.category_accommodation = Category(category="Accommodation",budget_simple=100, budget_quality=200, budget_luxury=300)
        self.category_food = Category(category="Food",budget_simple=100, budget_quality=200, budget_luxury=300)
        db.session.add_all([self.category_accommodation, self.category_food])
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

    def test_valid_form_submission(self):
        self.login()
        # Test valid form submission
        response = self.client.post('/upload', data={
            'amount': 50.00,
            'category': 'Food',
            'date': date.today(),
            'description': 'Test description'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Spending uploaded successfully', response.data)

        # Check that the spending was added to the database
        spending = Spending.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(spending)
        self.assertEqual(spending.amount, 50.00)
        self.assertEqual(spending.category_id, self.category_food.id)
        self.assertEqual(spending.description, 'Test description')

    def test_invalid_category(self):
        self.login()
        # Test form submission with an invalid category
        response = self.client.post('/upload', data={
            'amount': 30.00,
            'category': 'InvalidCategory',
            'date': date.today(),
            'description': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Not a valid choice.', response.data)

        # Ensure no spending was added to the database
        spending = Spending.query.filter_by(user_id=self.user.id).first()
        self.assertIsNone(spending)

    def test_missing_required_fields(self):
        self.login()
        # Test form submission with missing required fields (amount and category)
        response = self.client.post('/upload', data={
            'amount': '',
            'category': '',
            'date': date.today(),
            'description': 'Test description'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Amount is required.', response.data)
        self.assertIn(b'Please select a category.', response.data)

        # Ensure no spending was added to the database
        spending = Spending.query.filter_by(user_id=self.user.id).first()
        self.assertIsNone(spending)

    def test_future_date_validation(self):
        self.login()
        # Test form submission with a future date
        future_date = date.today() + timedelta(days=1)
        response = self.client.post('/upload', data={
            'amount': 20.00,
            'category': 'Accommodation',
            'date': future_date,
            'description': 'Test future date'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The date cannot be in the future.', response.data)

        # Ensure no spending was added to the database
        spending = Spending.query.filter_by(user_id=self.user.id).first()
        self.assertIsNone(spending)