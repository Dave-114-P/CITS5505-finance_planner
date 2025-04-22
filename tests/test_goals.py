# Unit tests for goal logic computation

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

def test_set_goal(client, user, app):
    # Test setting a savings goal
    with app.test_request_context():
        login_user(user)
        response = client.post("/goals", data={
            "target_amount": 12000,
            "years": 2
        }, follow_redirects=True)
        assert b"Goal set! Save $500.00 per month" in response.data