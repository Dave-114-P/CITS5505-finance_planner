# Tests for the view share route
import unittest
from app import create_app, db
from app.models.user import User
from app.models.share import Share
from app.config import TestingConfig

class TestViewShareRoute(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user and share
        self.user = User(username="testuser", email="testuser@gmail.com",gender="male")
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

        self.share = Share(
            sender_id=self.user.id,
            category="Test Category",
            title="Test Title",
            content="Test Content",
            is_public=True,
        )
        db.session.add(self.share)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        self.client.post("/login", data={"username": "testuser", "password": "password"})

    def test_view_share_success(self):
        self.login()
        response = self.client.get(f"/share/view/{self.share.id}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Title", response.data)

    def test_view_nonexistent_share(self):
        self.login()
        response = self.client.get("/share/view/999", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_add_comment_success(self):
        self.login()
        response = self.client.post(
            f"/share/view/{self.share.id}",
            data={"content": "Test Comment"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comment added.", response.data)

    def test_add_comment_empty_content(self):
        self.login()
        # Simulate a POST request with tampered data (bypassing client-side validation)
        response = self.client.post(
            f"/share/view/{self.share.id}",
            data={"content": ""},  # Empty content
            follow_redirects=True,
        )
        # Check that the server responds with the appropriate error message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comment cannot be empty.", response.data)  # Check for validation error message