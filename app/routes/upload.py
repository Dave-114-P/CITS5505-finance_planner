# Routes for uploading spending data and budget estimates

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.spending import Spending
from datetime import datetime

# Define blueprint for upload routes
bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    # Handle uploading of spending data
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        date_str = request.form.get("date")
        description = request.form.get("description")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        new_spending = Spending(
            user_id=current_user.id,
            amount=amount,
            category=category,
            date=date,
            description=description
        )
        db.session.add(new_spending)
        db.session.commit()
        flash("Spending data uploaded successfully", "success")
        return redirect(url_for("upload.upload"))
    return render_template("upload.html")