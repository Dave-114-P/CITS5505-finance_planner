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
    form = UploadSpendingForm()
    if form.validate_on_submit():  # Handles POST and validation
        amount = form.amount.data
        category_name = form.category.data
        date = form.date.data
        description = form.description.data

        # Fetch the category_id based on the category name
        category = Category.query.filter_by(category=category_name).first()

        if not category:
            flash("Invalid category selected", "danger")
            return render_template("upload.html", form=form)

        # Save the spending entry to the database
        new_spending = Spending(
            user_id=current_user.id,
            amount=amount,
            category_id=category.id,
            date=date,
            description=description
        )
        db.session.add(new_spending)
        db.session.commit()
        flash("Spending uploaded successfully", "success")
        return redirect(url_for("upload.upload"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Please correct the errors in the form.", "danger")

    return render_template("upload.html", form=form)