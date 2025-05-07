from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from sqlalchemy import func

# Import your database models
from app.models.spending import Spending  # Using the Spending class
from app.models.categories import Category  # Category model
from app.models.income import Income  # Income model

# Define the blueprint
bp = Blueprint("api", __name__, url_prefix="/api")

# API: Monthly Spending Breakdown
@bp.route("/monthly_spending_breakdown", methods=["GET"])
@login_required  # Ensure the user is logged in
def monthly_spending_breakdown():
    # Get current month
    current_month = datetime.now().strftime("%Y-%m")
    
    # Query database for the current user's spending in the current month
    results = (
        db.session.query(Category.category, func.sum(Spending.amount).label("total"))
        .join(Category, Spending.category_id == Category.id)  # Join with Category table
        .filter(Spending.user_id == current_user.id)  # Filter by logged-in user
        .filter(func.date(Spending.date).like(f"{current_month}%"))  # Filter by current month
        .group_by(Category.category)  # Group by category name
        .all()
    )
    # Convert results to a list of dictionaries
    spending_data = [{"category": row[0], "amount": row[1]} for row in results]
    return jsonify(spending_data)

# API: Spending Over the Last 30 Days
@bp.route("/data_last_30_days", methods=["GET"])
@login_required  # Ensure the user is logged in
def data_last_30_days():
    # Get the date range for the last 30 days
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    
    # Query database for the current user's spending in the last 30 days
    results_spend = (
        db.session.query(func.date(Spending.date).label("date"), func.sum(Spending.amount).label("total"))
        .filter(Spending.user_id == current_user.id)  # Filter by logged-in user
        .filter(Spending.date.between(thirty_days_ago, today))  # Filter by date range
        .group_by(func.date(Spending.date))  # Group by date
        .order_by(func.date(Spending.date))  # Order by date
        .all()
    )

    results_income = (
        db.session.query(func.date(Income.date).label("date"), func.sum(Income.amount).label("total"))
        .filter(Income.user_id == current_user.id)  # Filter by logged-in user
        .filter(Income.date.between(thirty_days_ago, today))  # Filter by date range
        .group_by(func.date(Income.date))  # Group by date
        .order_by(func.date(Income.date))  # Order by date
        .all()
    )
    
    # Convert results to a list of dictionaries
    data = [{"date": row[0], "amount": row[1], "type": "spending"} for row in results_spend]
    data += [{"date": row[0], "amount": row[1], "type": "income"} for row in results_income]
    return jsonify(data)