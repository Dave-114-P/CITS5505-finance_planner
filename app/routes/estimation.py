from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
from app.models.spending import Spending
from datetime import datetime
from app import db

bp = Blueprint("est", __name__)

# Define lifestyle plans
LIFESTYLE_PLANS = {
    "simple": {
        "budget": 2000,  
        "categories": {
            "Food": 400,
            "Utilities": 200,
            "Housing": 800,
            "Transportation": 300,
            "Shopping": 200,
            "Other": 100
        }
    },
    "quality": {
        "budget": 4000,
        "categories": {
            "Food": 600,
            "Utilities": 400,
            "Housing": 1500,
            "Transportation": 600,
            "Shopping": 600,
            "Other": 300
        }
    },
    "luxury": {
        "budget": 10000,
        "categories": {
            "Food": 1500,
            "Utilities": 800,
            "Housing": 4000,
            "Transportation": 1500,
            "Shopping": 1500,
            "Other": 700
        }
    },
}


# Define initial categories with budget
BASE_CATEGORIES = [
    {"name": "Food", "budget": 400},
    {"name": "Utilities", "budget": 200},
    {"name": "Housing", "budget": 800},
    {"name": "Transportation", "budget": 300},
    {"name": "Shopping", "budget": 200},
    {"name": "Other", "budget": 100},
]

@bp.route("/change_lifestyle", methods=["POST"])
@login_required
def change_lifestyle():
    # Clear selected lifestyle from session
    session.pop("lifestyle", None)
    return redirect(url_for("est.estimation"))

@bp.route("/estimation", methods=["GET", "POST"])
@login_required
def estimation():
    # Get lifestyle selection
    if request.method == "POST":
        selected_lifestyle = request.form.get("lifestyle")
        session["lifestyle"] = selected_lifestyle
    else:
        selected_lifestyle = session.get("lifestyle")

    # Build categories with spent and percent initialized
    categories_with_data = []
    plan = LIFESTYLE_PLANS.get(selected_lifestyle) if selected_lifestyle else None
    for cat in BASE_CATEGORIES:
        category = cat.copy()
        category["spent"] = 0
        category["percent"] = 0  # Initialize percent to avoid Jinja errors
        if plan and "categories" in plan:
            category["budget"] = plan["categories"].get(category["name"], category["budget"])

        category["percent"] = 0
        categories_with_data.append(category)


    category["percent"] = 0
    categories_with_data.append(category)

    # If lifestyle is selected -> calculate estimations
    if selected_lifestyle:
        plan = LIFESTYLE_PLANS.get(selected_lifestyle)

        # Get spending records from database for current user only
        spending_records = Spending.query.filter_by(user_id=current_user.id).all()

        # Convert to dict list
        spending_data = []
        for record in spending_records:
            spending_data.append({
                "category": record.category,
                "amount": record.amount
            })

        # Update spent values
        for record in spending_data:
            for category in categories_with_data:
                if category["name"] == record["category"]:
                    category["spent"] += record["amount"]

        # Calculate percent for each category
        for category in categories_with_data:
            budget = category["budget"]
            spent = category["spent"]
            category["percent"] = (spent / budget) * 100 if budget > 0 else 0

        # Calculate total spent and remaining budget
        total_spent = sum(c["spent"] for c in categories_with_data)
        remaining_budget = plan["budget"] - total_spent

        # Estimate possible future spending
        est_uber_cost = 20
        est_dining_cost = 30
        est_shopping_cost = 50

        possible_uber = remaining_budget // est_uber_cost
        possible_dining = remaining_budget // est_dining_cost
        possible_shopping = remaining_budget // est_shopping_cost

        # Suggestion message
        suggestion = "You're on track!"
        if remaining_budget < plan["budget"] * 0.2:
            suggestion = "Consider reducing spending to avoid running out of budget."
        if remaining_budget < 0:
            suggestion = "You have overspent. Please control your expenses!"

        return render_template(
            "estimation.html",
            selected_lifestyle=selected_lifestyle,
            recommended_budget=plan["budget"],
            total_spent=total_spent,
            remaining_budget=remaining_budget,
            possible_uber=int(possible_uber),
            possible_dining=int(possible_dining),
            possible_shopping=int(possible_shopping),
            suggestion=suggestion,
            categories=categories_with_data
        )

    # If no lifestyle selected yet, render empty version
    return render_template("estimation.html", categories=categories_with_data)
