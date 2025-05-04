from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app import db
from app.models.spending import Spending  # import Spending model
from app.models.category import Category

# Create Blueprint for estimation routes
bp = Blueprint('est', __name__)


@bp.route('/estimation', methods=['GET', 'POST'])
@login_required
def estimation():
    
    # Get the selected lifestyle from session (if exists)
    selected_lifestyle = session.get('lifestyle', None)

    # Handle lifestyle selection from form submission
    if request.method == 'POST':
        lifestyle = request.form.get('lifestyle')
        if lifestyle in ['simple', 'quality', 'luxury']:
            session['lifestyle'] = lifestyle
            flash('Lifestyle selected successfully!', 'success')
        else:
            flash('Invalid lifestyle selection.', 'danger')
        return redirect(url_for('est.estimation'))

    # Fetch all spending categories
    categories = Category.query.filter_by(lifestyle=selected_lifestyle).all()

    # Prepare data for rendering: calculate spent amount and percentage
    category_data = []
    for category in categories:
        # Get all spending records for this user and category
        spendings = Spending.query.filter_by(user_id=current_user.id, category_id=category.id).all()
        total_spent = sum(s.amount for s in spendings)

        # Calculate spending percentage (spent/budget * 100)
        if category.budget and category.budget > 0:
            percent = (total_spent / category.budget) * 100
        else:
            percent = 0

        # Append data to be passed to the template
        category_data.append({
            'id': category.id,
            'name': category.category,
            'budget': category.budget,
            'spent': total_spent,
            'percent': percent
        })

    # Render the template with lifestyle and category data
    return render_template("estimation.html", 
                           selected_lifestyle=selected_lifestyle, 
                           categories=category_data)

@bp.route('/estimation/change_lifestyle', methods=['POST'])
@login_required
def change_lifestyle():
    """
    Reset the selected lifestyle. 
    Allows user to choose a new lifestyle again.
    """
    session.pop('lifestyle', None)
    flash('Lifestyle has been reset. Please select again.', 'info')
    return redirect(url_for('est.estimation'))
