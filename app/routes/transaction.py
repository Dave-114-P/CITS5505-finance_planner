from flask import Blueprint, render_template

bp = Blueprint("trans", __name__)

@bp.route("/transaction", methods=["GET", "POST"])
def transaction():
    flow = {'inflow': 555.6, 'outflow': 999.9}
    budget_week = 80  # sample data
    return render_template('transaction.html', flow = flow, budget_week=budget_week)