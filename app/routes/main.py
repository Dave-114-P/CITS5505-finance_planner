from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_login import current_user, login_required
from datetime import datetime
from wtforms import SubmitField
from app.models.spending import Spending
from app.models.goals import Goal
from app.models.income import Income
from sqlalchemy import func
from app import db


bp = Blueprint("main", __name__)

# Confirmation Form for Resetting All Data
class ResetForm(FlaskForm):
    confirm = SubmitField("Confirm Reset")

@bp.route("/")
def index():
    form = ResetForm()
    top_spendings = []
    recent_transactions = []
    username = None
    total = 0  # Initialize total to ensure it's always defined
    # Default fallback values for chart data
    labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
    weekly_totals = [0, 0, 0, 0]
    total_expense = 0
    savings_percent = 0

    goals_created = 0

    if current_user.is_authenticated:
        username = current_user.username

        # Fetch the top 3 largest spendings
        top_spendings = Spending.get_3_largest_spendings(current_user.id)

        # Fetch the 3 most recent transactions
        recent_transactions = Spending.get_3_most_recent_transactions(current_user.id)

        # Calculate the total amount of the top spendings
        total = sum(spend.amount for spend in top_spendings)

        # Sum up total expense
        total_expense = (
            Spending.query.with_entities(func.sum(Spending.amount))
            .filter_by(user_id=current_user.id)
            .scalar()
        ) or 0.0

        # Count user's goals
        goals_created = Goal.query.filter_by(user_id=current_user.id).count()

        # Get weekly spending in current month
        now = datetime.now()
        all_spending = Spending.query.filter_by(user_id=current_user.id).all()
        for record in all_spending:
            if record.date and record.date.month == now.month and record.date.year == now.year:
                week_index = (record.date.day - 1) // 7
                if 0 <= week_index < 4:
                    weekly_totals[week_index] += record.amount
        
    return render_template(
        "index.html",
        username=username,
        top_spendings=top_spendings,
        recent_transactions=recent_transactions,
        total=total,
        labels=labels,
        expense_data=weekly_totals,
        total_expense=round(total_expense, 2),
        savings_percent=savings_percent,
        goals_created=goals_created,
        form=form
    )

@bp.route("/reset_all", methods=["GET", "POST"])
@login_required
def reset_all():
    form = ResetForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        try:
            # Check if there is any data to reset
            spendings = Spending.query.filter_by(user_id=current_user.id).all()
            incomes = Income.query.filter_by(user_id=current_user.id).all()

            if not spendings and not incomes:
                flash("No data to reset.", "info")
                return redirect(url_for("main.index"))

            # Delete all spending and income data for the user
            Spending.query.filter_by(user_id=current_user.id).delete()
            Income.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()

            flash("All data has been reset successfully.", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of errors
            flash("An error occurred while resetting data. Please try again.", "danger")
    elif request.method == "POST" and not form.validate_on_submit():
        flash("An error occurred. Please try again.", "danger")
    
    return render_template("reset_all.html", form=form)