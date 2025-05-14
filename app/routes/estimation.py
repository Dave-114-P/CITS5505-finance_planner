from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app.forms.estimationform import LifestyleForm, ChangeLifestyleForm
from app import db
from app.models.spending import Spending
from app.models.categories import Category
from sqlalchemy import extract
from datetime import datetime

# Create Blueprint for estimation routes
bp = Blueprint('est', __name__)

# Main estimation route
@bp.route('/estimation', methods=['GET', 'POST'])
@login_required
def estimation():
    # Create instances of both forms
    form = LifestyleForm()
    change_form = ChangeLifestyleForm()  # Add the ChangeLifestyleForm

    # Get the selected lifestyle from session (if exists)
    selected_lifestyle = session.get('lifestyle', None)

    # Handle form submission for selecting a lifestyle
    if form.validate_on_submit():
        lifestyle = form.lifestyle.data
        session['lifestyle'] = lifestyle
        flash('Lifestyle selected successfully!', 'success')
        return redirect(url_for('est.estimation'))
    elif request.method == 'POST' and not form.validate():
        # If the form is invalid, flash the error messages
        flash('Invalid lifestyle selection. Please try again.', 'danger')

    # Fetch all spending categories
    categories = Category.query.filter(Category.category != "Tuition fees").all()

    # Prepare data for rendering: calculate spent amount and percentage
    category_data = []
    current_month = datetime.now().month
    current_year = datetime.now().year
    for category in categories:
        # Filter spendings for the current month and year
        spendings = Spending.query.filter_by(user_id=current_user.id, category_id=category.id)\
                              .filter(extract('month', Spending.date) == current_month)\
                              .filter(extract('year', Spending.date) == current_year)\
                              .all()
        total_spent = sum(s.amount for s in spendings)

        if selected_lifestyle == "simple":
            budget = category.budget_simple
        elif selected_lifestyle == "quality":
            budget = category.budget_quality
        elif selected_lifestyle == "luxury":
            budget = category.budget_luxury
        else:
            budget = 0

        percent = (total_spent / budget) * 100 if budget > 0 else 0

        category_data.append({
            'id': category.id,
            'name': category.category,
            'budget': budget,
            'spent': total_spent,
            'percent': percent
        })

    # Render the template with lifestyle and category data
    return render_template(
        "estimation.html", 
        selected_lifestyle=selected_lifestyle, 
        categories=category_data, 
        form=form,
        change_form=change_form  # Pass the change_form to the template
    )

# Route to reset the selected lifestyle
@bp.route('/estimation/change_lifestyle', methods=['POST'])
@login_required
def change_lifestyle():
    change_form = ChangeLifestyleForm()

    if change_form.validate_on_submit():
        session.pop('lifestyle', None)
        flash('Lifestyle has been reset. Please select again.', 'info')
    return redirect(url_for('est.estimation'))