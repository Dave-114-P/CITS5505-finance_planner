from flask import Blueprint, render_template

bp = Blueprint("est", __name__)

@bp.route("/estimation")
def estimation():
    return render_template("estimation.html")