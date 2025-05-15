import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models import User
from datetime import datetime, timedelta
from app.config import TestingConfig

class TestSpendingRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the test client and application context."""
        self.app = create_app(TestingConfig)  # Create the Flask app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Populate the test database with a user
        with self.app.app_context():
            db.create_all()
            user = User(id=1, username="testuser", email="test@example.com", gender="male")
            user.set_password("password123")  # Hash the password
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """Tear down the application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        response=self.client.post("/login", data={
            "username": "testuser",
            "password": "password123"
        }, follow_redirects=True)
        print(response.status_code)  # Should be 200 if login is successful
        self.assertEqual(response.status_code, 200)

    def test_protected_route(self):
        self.login()  # Log in the client
        response = self.client.get("/visualise")
        self.assertEqual(response.status_code, 200)

    @patch("app.db.session.query")
    def test_monthly_spending_breakdown(self, mock_query):
        """Test the /monthly_spending_breakdown route with valid data."""
        # Mock the query results
        mock_results = [("Food", 150.0), ("Transportation", 50.0)]
        mock_query.return_value.join.return_value.filter.return_value.filter.return_value.group_by.return_value.all.return_value = mock_results

        #Log in the client
        response = self.client.post("/login", data={
            "username": "testuser",
            "password": "password123"
        }, follow_redirects=True)
        
        # Perform a GET request
        response = self.client.get("/api/monthly_spending_breakdown")
        print(response.status_code, response.headers.get("Location"))
        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"category": "Food", "amount": 150.0},
            {"category": "Transportation", "amount": 50.0},
        ])
        

    @patch("app.db.session.query")
    def test_data_last_30_days(self, mock_query):
        """Test the /data_last_30_days route with valid data."""
        # Mock the spending query results
        mock_spending_results = [
            ( "2025-04-02", 150.0),
            ( "2025-03-01", 50.0),
            ( "2024-07-25", 75.0),
        ]

        # Configure the mock query behavior
        mock_query.return_value.filter.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_spending_results

        #Log in the client
        response = self.client.post("/login", data={
            "username": "testuser",
            "password": "password123"
        }, follow_redirects=True)

        # Perform a GET request
        response = self.client.get("/api/data_last_30_days")
        self.assertEqual(response.status_code, 200)

        # Expected response
        expected_response = [
            {"amount": 150.0, "date": "2025-04-02", "type": "spending"},
            {"amount": 50.0, "date": "2025-03-01", "type": "spending"},
            {"amount": 75.0, "date": "2024-07-25", "type": "spending"},
            {"amount": 150.0, "date": "2025-04-02", "type": "income"},
            {"amount": 50.0, "date": "2025-03-01", "type": "income"},
            {"amount": 75.0, "date": "2024-07-25", "type": "income"},
        ]

        # Verify the response
        self.assertEqual(response.json, expected_response)

    @patch("app.db.session.query")
    def test_monthly_spending_breakdown_with_unauthorised_login(self, mock_query):
        """Test the /monthly_spending_breakdown route with valid data."""
        # Mock the query results
        mock_results = [("Food", 150.0), ("Transportation", 50.0)]
        mock_query.return_value.join.return_value.filter.return_value.filter.return_value.group_by.return_value.all.return_value = mock_results

        # Perform a GET request
        response = self.client.get("/api/monthly_spending_breakdown")
        print(response.status_code, response.headers.get("Location"))
        # Verify the response
        self.assertEqual(response.status_code, 302)

    @patch("app.db.session.query")
    def test_data_last_30_days_with_unauthorised_login(self, mock_query):
        """Test the /data_last_30_days route with valid data."""
        # Mock the spending query results
        mock_spending_results = [
            ( "2025-04-02", 150.0),
            ( "2025-03-01", 50.0),
            ( "2024-07-25", 75.0),
        ]

        # Configure the mock query behavior
        mock_query.return_value.filter.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = mock_spending_results

        # Perform a GET request
        response = self.client.get("/api/data_last_30_days")
        self.assertEqual(response.status_code, 302)

if __name__ == "__main__":
    unittest.main()