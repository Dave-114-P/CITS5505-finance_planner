# Routes for suggesting savings plans to reach goals

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.goals import Goal

# Define blueprint for goals routes
bp = Blueprint("goals", __name__)

@bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    # Handle setting and suggesting savings goals
    if request.method == "POST":
        target_amount = float(request.form.get("target_amount"))
        years = int(request.form.get("years"))
        monthly_plan = target_amount / (years * 12)  # Simple calculation
        new_goal = Goal(
            user_id=current_user.id,
            target_amount=target_amount,
            years=years,
            monthly_plan=monthly_plan
        )
        db.session.add(new_goal)
        db.session.commit()
        flash(f"Goal set! Save ${monthly_plan:.2f} per month to reach your target.", "success")
        return redirect(url_for("goals.goals"))
    return render_template("goals.html")