# Routes for returning analytics charts via AJAX

from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from app.models.spending import Spending

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
    # Fetch spending data for the current user
    spendings = Spending.query.filter_by(user_id=current_user.id).all()
    data = [{"category": s.category, "amount": s.amount} for s in spendings]
    return jsonify(data)