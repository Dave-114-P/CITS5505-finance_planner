from flask import Blueprint, render_template, send_file
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models.spending import Spending
import matplotlib.pyplot as plt
import io

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

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