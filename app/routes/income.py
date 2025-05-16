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

    income_id = request.args.get("income_id", type=int)  # Get income_id from query parameters

    # Create an instance of the form and populate the category choices dynamically
    form = IncomeForm(request.form)

    if income_id:  # If editing an existing income
        income = Income.query.get_or_404(income_id)

        # Ensure that the logged-in user owns this income
        if income.user_id != current_user.id:
            flash("You do not have permission to edit this income.", "danger")
            return redirect(url_for("trans.transaction"))

        if request.method == "GET":  # Populate the form with the existing income data
            form.amount.data = income.amount
            form.category.data = income.category.category  # Use the category name
            form.date.data = income.date
            form.description.data = income.description

    # Handle form submission
    if request.method == "POST" and form.validate_on_submit():
        amount = form.amount.data
        category_name = form.category.data
        date = form.date.data
        description = form.description.data

        # Fetch the category based on the selected name
        category = Categoryin.query.filter_by(category=category_name).first()
        if not category:
            flash("Invalid category selected", "danger")
            return render_template("income.html", form=form)

        if income_id:  # Update the existing income
            income.amount = amount
            income.category_id = category.id  # Use the category ID here
            income.date = date
            income.description = description
            db.session.commit()
            flash("Income updated successfully", "success")
        else:  # Create a new income
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

    elif request.method == "POST" and not form.validate_on_submit():
        # If the form is invalid, flash the errors
        flash("Please correct the errors in the form.", "danger")

    return render_template("income.html", form=form)