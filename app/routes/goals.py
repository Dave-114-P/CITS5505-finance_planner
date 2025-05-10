from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.goals import Goal
from app.forms.goalsform import GoalForm

# Define blueprint for goals routes
bp = Blueprint("goals", __name__)

@bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    # Create an instance of the GoalForm
    form = GoalForm(request.form)

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
            monthly_plan=monthly_plan,
        )
        db.session.add(new_goal)
        db.session.commit()

        flash(f"Goal set! Save ${monthly_plan:.2f} per month to reach your target.", "success")
        return redirect(url_for("goals.goals"))
    elif request.method == "POST" and not form.validate():
        # Show error messages if the form is invalid
        flash("Please correct the errors in the form.", "danger")

    return render_template("goals.html", form=form)