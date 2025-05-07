from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime
from app.models.spending import Spending
from app.models.goals import Goal
from sqlalchemy import func
from app import db

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    # Default fallback values for chart data
    labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
    weekly_totals = [0, 0, 0, 0]
    total_expense = 0
    savings_percent = 0

    # Count user's goals
    goals_created = Goal.query.filter_by(user_id=current_user.id).count()

    # If user is logged in, calculate real values
    if current_user.is_authenticated:
        # Sum up total expense
        total_expense = (
            Spending.query.with_entities(func.sum(Spending.amount))
            .filter_by(user_id=current_user.id)
            .scalar()
        ) or 0.0

        # Get weekly spending in current month
        now = datetime.now()
        all_spending = Spending.query.filter_by(user_id=current_user.id).all()
        for record in all_spending:
            if record.date and record.date.month == now.month and record.date.year == now.year:
                week_index = (record.date.day - 1) // 7
                if 0 <= week_index < 4:
                    weekly_totals[week_index] += record.amount

    #
    return render_template(
        "index.html",
        labels=labels,
        expense_data=weekly_totals,
        total_expense=round(total_expense, 2),
        savings_percent=savings_percent,
        goals_created=goals_created
    )

@bp.route("/reset_expenses", methods=["POST"])
@login_required
def reset_expenses():
    Spending.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return redirect(url_for("main.index"))
