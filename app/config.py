# Global configuration settings for the Finance Planner app

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

    # Disable SQLAlchemy modification tracking for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    # Database URI for development environment
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///finance.db")
    WTF_CSRF_ENABLED = True  # Enable CSRF protection

class TestingConfig(Config):
    # Database URI for testing environment
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI", "sqlite:///test.db")
    TESTING = True  # Enable testing mode
    DEBUG = True  # Enable debug mode for development
    WTF_CSRF_ENABLED = False  # Ensure CSRF is enabled for testing
    SECRET_KEY = os.getenv("SECRET_KEY", "test-secret-key")