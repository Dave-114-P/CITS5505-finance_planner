from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from collections import defaultdict
from flask_login import login_required, current_user
from app.models.spending import Spending
from app.models.income import Income
from calendar import monthrange

bp = Blueprint("trans", __name__)

@bp.route("/transaction", methods=["GET", "POST"])
@login_required
def transaction():
    # Fetch spendings and incomes for the current user
    spendings = Spending.query.filter_by(user_id=current_user.id).order_by(Spending.date.desc()).all()
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()

    if request.method == "POST":
        # Handle filtering
        period = request.form.get("period", "month")
        filtered_spendings = filter_transactions(spendings, period)
        filtered_incomes = filter_transactions(incomes, period)
        categorized_spendings = group_transactions_by_month(filtered_spendings)
        categorized_incomes = group_transactions_by_month(filtered_incomes)
    else:
        # Default to showing all transactions grouped by month
        categorized_spendings = group_transactions_by_month(spendings)
        categorized_incomes = group_transactions_by_month(incomes)

    # Get current date and time
    now = datetime.utcnow()
    current_year = now.year
    current_month = now.month

    # Get selected month and year from query parameters
    month = request.args.get('month', type=int, default=current_month)
    year = request.args.get('year', type=int, default=current_year)

    # Define the start and end dates for the selected month
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, monthrange(year, month)[1])

    # Flatten and filter transactions for the selected month
    spendings = [
        transaction for sublist in categorized_spendings.values()
        for transaction in sublist
        if start_date <= transaction.date <= end_date
    ]
    incomes = [
        transaction for sublist in categorized_incomes.values()
        for transaction in sublist
        if start_date <= transaction.date <= end_date
    ]

    # Calculate last month
    if current_month == 1:
        last_month = 12
        last_month_year = current_year - 1
    else:
        last_month = current_month - 1
        last_month_year = current_year

    # Generate past months for dropdown
    unique_months_spendings = set((transaction.date.year, transaction.date.month) for sublist in categorized_spendings.values() for transaction in sublist)
    unique_months_incomes = set((transaction.date.year, transaction.date.month) for sublist in categorized_incomes.values() for transaction in sublist)
    unique_months = unique_months_spendings.union(unique_months_incomes)

    past_months = [{"month": m, "year": y} for y, m in sorted(unique_months, reverse=True)]

    # Exclude "this month" and "last month" from past_months
    past_months = [
        month for month in past_months
        if not (month["year"] == current_year and month["month"] == current_month) and
           not (month["year"] == last_month_year and month["month"] == last_month)
    ]

    # Only show the dropdown if there are valid past months
    show_dropdown = len(past_months) > 0

    return render_template('transaction.html',
                           spendings=spendings,
                           incomes=incomes,
                           past_months=past_months,
                           show_dropdown=show_dropdown,
                           current_month=current_month,
                           current_year=current_year,
                           last_month=last_month,
                           last_month_year=last_month_year)

def group_transactions_by_month(transactions):
    categorized = defaultdict(list)
    today = datetime.today()

    for transaction in transactions:
        transaction_date = transaction.date  # Use attribute access instead of dictionary-like access
        if transaction_date.month == today.month and transaction_date.year == today.year:
            categorized['This Month'].append(transaction)
        elif transaction_date.month == (today - timedelta(days=30)).month and transaction_date.year == (today - timedelta(days=30)).year:
            categorized['Last Month'].append(transaction)
        elif transaction_date > today:
            categorized['Future'].append(transaction)
        else:
            categorized[transaction_date.strftime('%m/%Y')].append(transaction)

    return categorized

def filter_transactions(transactions, period='month'):
    today = datetime.today()
    filtered = []

    if period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'year':
        start_date = today - timedelta(days=365)
    else:  # Default to month
        start_date = today - timedelta(days=30)

    for transaction in transactions:
        transaction_date = transaction.date  # Use attribute access
        if transaction_date >= start_date:
            filtered.append(transaction)

    return filtered