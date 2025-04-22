# Global configuration settings for the Finance Planner app

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv("SECRET_KEY", "123")

    # SQLite database URI
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///finance.db")

    # Disable SQLAlchemy modification tracking for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False