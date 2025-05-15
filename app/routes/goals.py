from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.goals import Goal
from app.forms.goalsform import GoalForm

# Blueprint setup
bp = Blueprint("goals", __name__)

@bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    form = GoalForm()

    if form.validate_on_submit():
        target_amount = form.target_amount.data
        years = form.years.data
        monthly_plan = target_amount / (years * 12)

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

    # Load all goals created by the current user
    user_goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template("goals.html", form=form, goals=user_goals)

@bp.route("/reset_goals", methods=["POST"])
@login_required
def reset_goals():
    # Delete all goals for the current user
    Goal.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("All your savings goals have been reset.", "success")
    return redirect(url_for("goals.goals"))
