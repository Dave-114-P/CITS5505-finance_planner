# Routes for returning analytics charts via AJAX

from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from app.models.spending import Spending
from app.models.category import Category
from app import db

# Define blueprint for visualise routes
bp = Blueprint("visualise", __name__)

@bp.route("/visualise", methods=["GET"])
@login_required
def visualise():
    # Render the visualisation page
    return render_template("visualise.html")

@bp.route("/api/spending_data", methods=["GET"])
@login_required
def spending_data():
    from datetime import datetime, timedelta

    # Calculate the date range for the last 30 days
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)

    # Fetch spending data for the current user within the last 30 days
    spendings = (
        db.session.query(Spending, Category.category)
        .join(Category, Spending.category_id == Category.id)
        .filter(Spending.user_id == current_user.id)
        .filter(Spending.date >= thirty_days_ago)  # Filter for the last 30 days
        .all()
    )

    # Prepare the data for JSON response
    data = [{"category": category_name, "amount": spending.amount} for spending, category_name in spendings]

    return jsonify(data)