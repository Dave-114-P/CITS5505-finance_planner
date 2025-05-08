from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.incategory import Categoryin
from app.models.income import Income
from app.forms.incomeform import IncomeForm

# Define blueprint for income routes
bp = Blueprint("income", __name__)

@bp.route("/income", methods=["GET", "POST"])
@login_required
def income():
    # Fetch all categories to populate the category dropdown
    categories = Categoryin.query.all()
    category_choices = [(c.category, c.category) for c in categories]

    # Create an instance of the form and populate the category choices dynamically
    form = IncomeForm(request.form)
    form.category.choices = category_choices

    # Handle form submission
    if request.method == "POST" and form.validate():
        amount = form.amount.data
        category_name = form.category.data
        date = form.date.data
        description = form.description.data

        # Fetch the category based on the selected name
        category = Categoryin.query.filter_by(category=category_name).first()
        if not category:
            flash("Invalid category selected", "danger")
            return render_template("income.html", form=form)

        # Save the income entry to the database
        new_income = Income(
            user_id=current_user.id,
            amount=amount,
            category_id=category.id,  # Use the category ID here
            date=date,
            description=description,
        )
        db.session.add(new_income)
        db.session.commit()
        flash("Income uploaded successfully", "success")
        return redirect(url_for("income.income"))

    elif request.method == "POST" and not form.validate():
        # If the form is invalid, flash the errors
        flash("Please correct the errors in the form.", "danger")

    return render_template("income.html", form=form)