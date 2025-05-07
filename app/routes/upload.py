# app/routes/upload.py

from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.spending import Spending
from app.models.category import Category
from datetime import datetime

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        # Retrieve form inputs
        amount = float(request.form["amount"])
        key = request.form["category"]  
        date_str = request.form["date"]
        description = request.form.get("description", "")

        # Look up the Category by combining key with default lifestyle "simple"
        lifestyle = session.get("lifestyle", "simple")
        category = Category.query.filter_by(key=f"{key}_{lifestyle}").first()
        if not category:
            flash("Invalid category selected", "danger")
            return redirect(url_for("upload.upload"))

        # Parse and validate the date
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format", "danger")
            return redirect(url_for("upload.upload"))
        if date.date() > datetime.utcnow().date():
            flash("Date cannot be in the future", "danger")
            return redirect(url_for("upload.upload"))

        # Create a new Spending record linked by category_id
        sp = Spending(
            user_id     = current_user.id,
            amount      = amount,
            category_id = category.id,
            date        = date,
            description = description
        )
        db.session.add(sp)
        db.session.commit()

        flash("Spending uploaded successfully", "success")
        return redirect(url_for("upload.upload"))

    # Prepare category keys for the dropdown (no lifestyle choice here)
    keys = [
        "accomodation",
        "food",
        "transportation",
        "entertainment",
        "clothing",
        "personal",
        "tuition_fees"
    ]
    return render_template("upload.html", keys=keys)
