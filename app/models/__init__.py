# This file is part of the app.models module.
# It imports all the necessary models for the testing.
from .user import User
from .spending import Spending
from .categories import Category
from .goals import Goal
from .post import Post
from .incategory import Categoryin
from .income import Income

__all__ = ["User", "Spending", "Category", "Goal", "Post", "Categoryin", "Income"]