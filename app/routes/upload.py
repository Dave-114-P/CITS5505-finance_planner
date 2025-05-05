# Routes for uploading spending data and budget estimates

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.spending import Spending
from app.models.categories import Category
from datetime import datetime

# Define blueprint for upload routes
bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    # Handle uploading of spending data
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        category_name = request.form.get("category")  # Get category name from the form
        date_str = request.form.get("date")
        description = request.form.get("description")
        date = datetime.strptime(date_str, "%Y-%m-%d")

        # Fetch the category_id based on the category name
        category = Category.query.filter_by(category=category_name).first()

        if not category:
            flash("Invalid category selected", "danger")
            return redirect(url_for("upload.upload"))

        new_spending = Spending(
            user_id=current_user.id,
            amount=amount,
            category_id=category.id,  # Use the category ID here
            date=date,
            description=description
        )
        db.session.add(new_spending)
        db.session.commit()
        flash("Spending data uploaded successfully", "success")
        return redirect(url_for("upload.upload"))
    return render_template("upload.html")