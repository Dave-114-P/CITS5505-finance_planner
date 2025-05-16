from app.forms.spendform import UploadSpendingForm
from flask import Blueprint, render_template, redirect, url_for, flash,request
from flask_login import login_required, current_user
from app.models.spending import Spending
from app.models.categories import Category
from app import db
from datetime import datetime

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    spending_id = request.args.get("spending_id", type=int)  # Get spending_id from query parameters
    form = UploadSpendingForm()

    if spending_id:  # If editing an existing spending record
        spending = Spending.query.get_or_404(spending_id)

        # Ensure the logged-in user owns this spending record
        if spending.user_id != current_user.id:
            flash("You do not have permission to edit this spending.", "danger")
            return redirect(url_for("trans.transaction"))

        if request.method == "GET":  # Populate the form with the existing spending data
            form.amount.data = spending.amount
            form.category.data = spending.category.category  # Use the category name
            form.date.data = spending.date
            form.description.data = spending.description

    if request.method == "POST" and form.validate_on_submit():
        # Extract form data
        amount = form.amount.data
        category_name = form.category.data
        date = form.date.data
        description = form.description.data

        # Fetch the category based on the selected name
        category = Category.query.filter_by(category=category_name).first()
        if not category:
            flash("Invalid category selected", "danger")
            return render_template("upload.html", form=form)

        if spending_id:  # If editing, update the existing spending record
            spending.amount = amount
            spending.category_id = category.id  # Use the category ID here
            spending.date = date
            spending.description = description
            db.session.commit()
            flash("Spending updated successfully", "success")
        else:  # If creating a new spending record
            new_spending = Spending(
                user_id=current_user.id,
                amount=amount,
                category_id=category.id,
                date=date,
                description=description,
            )
            db.session.add(new_spending)
            db.session.commit()
            flash("Spending uploaded successfully", "success")

        return redirect(url_for("upload.upload"))

    elif request.method == "POST" and not form.validate_on_submit():
        # If the form is invalid, flash the errors
        flash("Please correct the errors in the form.", "danger")

    return render_template("upload.html", form=form)