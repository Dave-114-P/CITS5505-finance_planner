from flask import Blueprint, render_template, send_file, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models.spending import Spending
import matplotlib.pyplot as plt
import io

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    top_spendings = []
    recent_transactions = []
    username = None
    total = 0  # Initialize total to ensure it's always defined

    if current_user.is_authenticated:
        username = current_user.username

        # Fetch the top 3 largest spendings
        top_spendings = Spending.get_3_largest_spendings(current_user.id)

        # Fetch the 3 most recent transactions
        recent_transactions = Spending.get_3_most_recent_transactions(current_user.id)

        # Calculate the total amount from the top spendings if available
        if isinstance(top_spendings, list) and len(top_spendings) > 0:
            total = sum(spend.amount for spend in top_spendings)
        elif isinstance(top_spendings, dict) and "message" in top_spendings:
            # Handle case where fewer than 1 spending exists
            return render_template(
                "index.html",
                username=username,
                message=top_spendings["message"],
                top_spendings=top_spendings.get("spendings", []),
                recent_transactions=recent_transactions,
                total=total
            )

    return render_template(
        "index.html",
        username=username,
        top_spendings=top_spendings,
        recent_transactions=recent_transactions,
        total=total
    )

#Plotting line graph from server-side and send it as png file
@bp.route("/plot.png")
@login_required
def plot_png():
    today = datetime.today().date()
    last_30 = today - timedelta(days=29)

    # Fetch current user's spending data for the last 30 days
    results = (
        db.session.query(Spending.date, db.func.sum(Spending.amount))
        .filter(Spending.user_id == current_user.id)
        .filter(Spending.date >= last_30)
        .group_by(Spending.date)
        .order_by(Spending.date)
        .all()
    )

    dates = [r[0] for r in results]
    totals = [r[1] for r in results]

    # Plot the data using matplotlib
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(dates, totals, marker="o", color="#76c87d")
    ax.set_title("Your Spending in the Last 30 Days")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    fig.autofmt_xdate()

    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return send_file(img, mimetype="image/png")