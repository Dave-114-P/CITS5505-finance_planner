# Unit tests for login/register functionality

import pytest
from app import create_app, db

@pytest.fixture
def app():
    # Create a test Flask app
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

def test_register(client):
    # Test user registration
    response = client.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert b"Registration successful" in response.data

def test_login(client):
    # Test user login
    client.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)
    assert b"Welcome to Finance Planner" in response.data