from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.spending import Spending
from app.models.categories import Category
from app.models.incategory import Categoryin
from app.models.income import Income
from datetime import datetime

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    selected_lifestyle = session.get('lifestyle', None)
    
    categories = Category.query.filter_by(lifestyle=selected_lifestyle).all()

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
        
        # Check if the amount is a valid number
        try:
            amount = float(amount)
            if amount <= 0:
                flash("Amount must be a positive number", "danger")
                return render_template("income.html", amount=amount, category_name=category_name, date=date_str, description=description)
        except ValueError:
            flash("Invalid amount. Please enter a valid number.", "danger")
            return render_template("income.html", amount=amount, category_name=category_name, date=date_str, description=description)

        # Convert the date string to a datetime object
        try:
            input_date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Ensure the date is in the correct format
        except ValueError:
            # Handle invalid date format
            return "Invalid date format. Please enter a valid date in the format YYYY-MM-DD."

        # Get today's date
        today = datetime.utcnow().date()

        # Check if the input date is not more than today
        if input_date > today:
            flash("The date cannot be in the future. Please select a valid date.")
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
        flash("Spending uploaded successfully", "success")
        return redirect(url_for("upload.upload"))
    return render_template("upload.html")