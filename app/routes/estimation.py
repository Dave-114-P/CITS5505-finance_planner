# app/routes/estimation.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app.models.spending import Spending
from app.models.category import Category

bp = Blueprint("est", __name__)

@bp.route("/estimation", methods=["GET", "POST"])
@login_required
def estimation():
    # When the user submits a lifestyle choice, save it in session
    if request.method == "POST":
        life = request.form.get("lifestyle")
        if life in ("simple", "quality", "luxury"):
            session["lifestyle"] = life
            flash("Lifestyle selected", "success")
        else:
            flash("Invalid selection", "danger")
        return redirect(url_for("est.estimation"))

    # Read selected lifestyle from session
    selected = session.get("lifestyle")
    # Fetch categories for that lifestyle
    categories = Category.query.filter_by(lifestyle=selected).all()

    results = []
    for c in categories:
        # Sum up all spendings for this user + category
        spendings = Spending.query.filter(
            Spending.user_id == current_user.id,
            Spending.category_id == int(c.id)
        ).all()
        total = sum(s.amount for s in spendings)
        percent = (total / c.budget * 100) if c.budget else 0
        results.append({
            "name":    c.category,
            "budget":  c.budget,
            "spent":   total,
            "percent": percent
        })

    return render_template(
        "estimation.html",
        selected_lifestyle=selected,
        categories=results
    )

@bp.route("/estimation/change_lifestyle", methods=["POST"])
@login_required
def change_lifestyle():
    # Allow the user to reset their lifestyle choice
    session.pop("lifestyle", None)
    flash("Lifestyle reset—please choose again", "info")
    return redirect(url_for("est.estimation"))
