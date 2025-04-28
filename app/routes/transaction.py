from flask import Blueprint, render_template

bp = Blueprint("trans", __name__)

@bp.route("/transaction", methods=["GET", "POST"])
def transaction():
    return render_template("transaction.html")