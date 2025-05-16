# Tests for the delete share route
import unittest
from app import create_app, db
from app.models.user import User
from app.models.share import Share
from app.config import TestingConfig

class TestDeleteShareRoute(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user and share
        self.user = User(username="testuser", email="testuser@gmail.com",gender="female")
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

    def test_delete_share_success(self):
        self.login()
        response = self.client.post(f"/share/delete/{self.share.id}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Share deleted.", response.data)

    def test_delete_nonexistent_share(self):
        self.login()
        response = self.client.post("/share/delete/999", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_delete_share_unauthorized(self):
        self.login()
        other_user = User(username="otheruser", email="otheruser@example.com", gender="prefer not to say")
        other_user.set_password("password")
        db.session.add(other_user)
        db.session.commit()

        other_share = Share(
            sender_id=other_user.id,
            category="Other Category",
            title="Other Title",
            content="Other Content",
            is_public=True,
        )
        db.session.add(other_share)
        db.session.commit()

        response = self.client.post(f"/share/delete/{other_share.id}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You cannot delete someone else&#39;s post.", response.data)