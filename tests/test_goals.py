import unittest
from flask import session
from app import create_app, db
from app.models import User, Goal
from app.config import TestingConfig

class GoalsRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test app and database
        self.app = create_app(TestingConfig)  # Ensure 'testing' config is set for isolated db
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test client for sending requests
        self.client = self.app.test_client()

        # Create a test user
        self.test_user = User(username="testuser",email='test@example.com', gender="female")
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

    def test_goal_creation_success(self):
        # Test successful goal creation with valid data
        self.login()
        response = self.client.post('/goals', data={
            'target_amount': 1200,
            'years': 2
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful submission

        # Check if the goal was added to the database
        goal = Goal.query.filter_by(user_id=self.test_user.id).first()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.target_amount, 1200)
        self.assertEqual(goal.years, 2)
        self.assertEqual(goal.monthly_plan, 50)  # 1200 / (2 * 12)

    def test_goal_creation_invalid_target_amount(self):
        # Test goal creation with an invalid target amount
        self.login()
        response = self.client.post('/goals', data={
            'target_amount': -500,  # Invalid target amount
            'years': 2
        })
        self.assertEqual(response.status_code, 200)  # Form errors render the same template
        self.assertIn(b'Target amount must be greater than 0.', response.data)

        # Ensure no goal was created
        goal_count = Goal.query.filter_by(user_id=self.test_user.id).count()
        self.assertEqual(goal_count, 0)

    def test_goal_creation_invalid_years(self):
        # Test goal creation with invalid years
        self.login()
        response1 = self.client.post('/goals', data={
            'target_amount': 1200,
            'years': 0  # Invalid years input
        })
        self.assertEqual(response1.status_code, 200)  # Form errors render the same template
        self.assertIn(b'Number of years is required', response1.data)

        response2 = self.client.post('/goals', data={
            'target_amount': 1200,
            'years': -2 # Invalid years input
        })
        self.assertEqual(response2.status_code, 200)  # Form errors render the same template
        self.assertIn(b'Years must be between 1 and 50.', response2.data)

        # Ensure no goal was created
        goal_count = Goal.query.filter_by(user_id=self.test_user.id).count()
        self.assertEqual(goal_count, 0)

    def test_goal_creation_missing_fields(self):
        # Test goal creation with missing form fields
        self.login()
        response = self.client.post('/goals', data={
            'target_amount': '',  # Missing target amount
            'years': ''           # Missing years
        })
        self.assertEqual(response.status_code, 200)  # Form errors render the same template
        self.assertIn(b'Target amount is required.', response.data)
        self.assertIn(b'Number of years is required.', response.data)

        # Ensure no goal was created
        goal_count = Goal.query.filter_by(user_id=self.test_user.id).count()
        self.assertEqual(goal_count, 0)