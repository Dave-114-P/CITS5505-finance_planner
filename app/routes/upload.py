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
    selected_lifestyle = session.get('lifestyle', None)
    
    categories = Category.query.filter_by(lifestyle=selected_lifestyle).all()

    if request.method == "POST":
        amount = float(request.form.get("amount"))
        category_id = request.form.get("category")
        date_str = request.form.get("date")
        description = request.form.get("description")
        date = datetime.strptime(date_str, "%Y-%m-%d")

        new_spending = Spending(
            user_id=current_user.id,
            amount=amount,
            category_id=category_id,
            date=date,
            description=description
        )
        db.session.add(new_spending)
        db.session.commit()
        flash("Spending data uploaded successfully", "success")
        return redirect(url_for("est.estimation"))

    return render_template("upload.html", categories=categories)
