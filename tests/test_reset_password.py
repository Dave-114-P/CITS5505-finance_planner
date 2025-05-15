import unittest
from unittest.mock import patch, MagicMock
from flask import url_for
from app import create_app, db
from app.models import User
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.config import TestingConfig


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """
        Sets up the test environment.
        """
        self.app = create_app(TestingConfig)
        self.app.config['TESTING'] = True
        self.app.config['SERVER_NAME'] = 'localhost'
        self.client = self.app.test_client()
        
        # Push the application context
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Create the database schema
        db.create_all()

        # Example user for tests
        self.user = User(username="testuser", email="test@example.com",gender="prefer not to say")
        self.user.set_password("password123")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """
        Tears down the test environment.
        """
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    @patch('app.routes.auth.flash')
    @patch('app.routes.auth.URLSafeTimedSerializer')  # Mock the serializer
    def test_forgot_password_success(self, mock_serializer, mock_flash):
        """
        Test the forgot_password route when the user exists.
        """
        # Mock the dumps method to return a test token
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.dumps.return_value = "test-token"

        response = self.client.post(
            url_for('auth.forgot_password'),
            data=dict(username="testuser", email="test@example.com"),
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        mock_flash.assert_called_with(
            '<a href="http://localhost/reset-password/test-token" class="alert-link">Click here to reset your password</a>',
            "info"
        )

    @patch('app.routes.auth.flash')
    @patch('app.routes.auth.URLSafeTimedSerializer')  # Mock the serializer
    def test_forgot_password_success(self, mock_serializer, mock_flash):
        """
        Test the forgot_password route when the user exists.
        """
        # Mock the dumps method to return a test token
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.dumps.return_value = "test-token"

        response = self.client.post(
            url_for('auth.forgot_password'),
            data=dict(username="testuser", email="test@example.com"),
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        mock_flash.assert_called_with(
            '<a href="http://localhost/reset-password/test-token?url_scheme=https" class="alert-link">Click here to reset your password</a>',
            "info"
        )

    @patch('app.routes.auth.flash')
    def test_reset_password_form_valid_token(self, mock_flash):
        """
        Test the reset_password_form route with a valid token.
        """
        serializer = URLSafeTimedSerializer(self.app.config['SECRET_KEY'])
        token = serializer.dumps(self.user.id)

        response = self.client.post(
            url_for('auth.reset_password_form', token=token),
            data=dict(password="newpassword123", confirm_password="newpassword123"),
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.user = db.session.get(User, self.user.id)
        self.assertTrue(self.user.check_password("newpassword123"))
        mock_flash.assert_called_with("Your password has been updated!", "success")

    @patch("app.routes.auth.URLSafeTimedSerializer", autospec=True)
    def test_reset_password_form_invalid_token(self, MockSerializer):
        """
        Test the reset_password_form route with an invalid token.
        """
        # Mock the loads method to raise BadSignature
        mock_instance = MockSerializer.return_value
        mock_instance.loads.side_effect = BadSignature("Invalid token")

        # Simulate a GET request with an invalid token
        response = self.client.get(
            url_for("auth.reset_password_form", token="invalid-token"),
            follow_redirects=True  # Follow the redirect to the "Forgot Password" page
        )

        # Verify the status code
        self.assertEqual(response.status_code, 200)

        # Check that the flash message is rendered in the response HTML
        self.assertIn(
            b"Invalid password reset link.",
            response.data
        )

    @patch("app.routes.auth.URLSafeTimedSerializer", autospec=True)
    def test_reset_password_form_expired_token(self, MockSerializer):
        # Mock the loads method to raise SignatureExpired
        mock_instance = MockSerializer.return_value
        mock_instance.loads.side_effect = SignatureExpired("Token expired")

        # Simulate a GET request with an expired token
        response = self.client.get(
            url_for("auth.reset_password_form", token="dummy-token"),
            follow_redirects=False
        )

        # Ensure redirection occurs
        self.assertEqual(response.status_code, 302)

        # Check flash messages
        with self.client.session_transaction() as session:
            flashes = session.get('_flashes')
            self.assertIsNotNone(flashes)
            self.assertIn(('danger', 'The password reset link has expired. Please request a new one.'), flashes)


if __name__ == "__main__":
    unittest.main()