# Unit tests for uploading expense data

import pytest
from app import create_app, db
from app.models.user import User
from flask_login import login_user

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password="password123")
        db.session.add(user)
        db.session.commit()
        return user

def test_upload_spending(client, user, app):
    # Test uploading spending data
    with app.test_request_context():
        login_user(user)
        response = client.post("/upload", data={
            "amount": 100.50,
            "category": "Food",
            "date": "2025-01-01",
            "description": "Groceries"
        }, follow_redirects=True)
        assert b"Spending data uploaded successfully" in response.data