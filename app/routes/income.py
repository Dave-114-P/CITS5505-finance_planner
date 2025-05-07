from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.incategory import Categoryin
from app.models.income import Income
from datetime import datetime

bp = Blueprint("income", __name__)

@bp.route("/income", methods=["GET", "POST"])
@login_required
def income():
    categories = Categoryin.query.all()

    if request.method == "POST":
        amount = request.form.get("amount")
        category_name = request.form.get("category")
        date_str = request.form.get("date")
        description = request.form.get("description")

        category = Categoryin.query.filter_by(category=category_name).first()

        if not category:
            flash("Invalid category selected", "danger")
            return render_template("income.html", amount=amount, category_name=category_name, date=date_str, description=description, categories=categories)

        try:
            input_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            flash("Invalid date format. Please enter a valid date in the format YYYY-MM-DD.", "danger")
            return render_template("income.html", amount=amount, category_name=category_name, date=date_str, description=description, categories=categories)

        if input_date.date() > datetime.utcnow().date():
            flash("The date cannot be in the future. Please select a valid date.", "danger")
            return render_template("income.html", amount=amount, category_name=category_name, date=date_str, description=description, categories=categories)

        new_income = Income(
            user_id=current_user.id,
            amount=float(amount),
            category_id=category.id,
            date=input_date,
            description=description
        )
        db.session.add(new_income)
        db.session.commit()
        flash("Income uploaded successfully", "success")
        return redirect(url_for("income.income"))

    return render_template("income.html", categories=categories)
