# app/routes/stocks.py
from flask import Blueprint, render_template

bp = Blueprint("stocks", __name__, url_prefix="/stocks")

@bp.route("/")
def index():
    # Renders app/templates/stocks.html
    return render_template("stocks.html")