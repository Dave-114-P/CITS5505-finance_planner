# Tests for the main share route
import unittest
from app import create_app, db
from app.models.user import User
from app.models.categories import Category
from flask import url_for
from app.config import TestingConfig

class TestShareRoute(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user and category
        self.user = User(username="testuser", email="testuser@gmail.com",gender="male")
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

        self.category = Category(category="Test Category",budget_simple=100, budget_quality=200, budget_luxury=300)
        db.session.add(self.category)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        self.client.post("/login", data={"username": "testuser", "password": "password"})

    def test_share_success(self):
        self.login()
        response = self.client.post(
            "/share/",
            data={
                "category": "Test Category",
                "title": "Test Title",
                "content": "Test Content",
                "is_public": "on",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Share successful.", response.data)

    def test_share_invalid_category(self):
        self.login()
        response = self.client.post(
            "/share/",
            data={
                "category": "Nonexistent Category",  # Invalid category
                "title": "Test Title",
                "content": "Test Content",
                "is_public": "on",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Not a valid choice.", response.data)

    def test_share_with_image(self):
        self.login()
        with open("test_image.jpg", "wb") as f:
            f.write(b"test image content")
        with open("test_image.jpg", "rb") as img:
            response = self.client.post(
                "/share/",
                data={
                    "category": "Test Category",
                    "title": "Test Title",
                    "content": "Test Content",
                    "is_public": "on",
                    "image": img,
                },
                follow_redirects=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Share successful.", response.data)

    def test_share_invalid_user(self):
        self.login()
        response = self.client.post(
            "/share/",
            data={
                "receiver": "nonexistentuser",
                "category": "Test Category",
                "title": "Test Title",
                "content": "Test Content",
                "is_public": "off",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User not found.", response.data)