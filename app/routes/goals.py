from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.goals import Goal
from app.forms.goalsform import GoalForm
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

# Blueprint Setup
bp = Blueprint("goals", __name__)
class ResetGoals(FlaskForm):
    confirm = SubmitField("Confirm Reset", validators=[DataRequired()])

@bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    # Create an instance of the GoalForm
    form = GoalForm()

    # Handle form submission
    if request.method == "POST" and form.validate_on_submit():
        target_amount = form.target_amount.data
        years = form.years.data
        monthly_plan = target_amount / (years * 12)  # Simple calculation

        # Save the new goal to the database
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
    else:
        # Show error messages if the form is invalid
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, "danger")

    # Load all goals created by the current user
    user_goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template("goals.html", form=form, goals=user_goals)

@bp.route("/reset_goals", methods=["POST", "GET"])
@login_required
def reset_goals():
    form = ResetGoals()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("An error occurred. Please try again.", "danger")
            return render_template("reset_all.html", form=form), 200
        try:
            goals = Goal.query.filter_by(user_id=current_user.id).all()

            if not goals:
                flash("No goals to reset.", "info")
                return redirect(url_for("goals.goals"))

            Goal.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()

            flash("All your savings goals have been reset.", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of errors
            flash("An error occurred while resetting data. Please try again.", "danger")
    return render_template("reset_goals.html", form=form)