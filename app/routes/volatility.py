# app/routes/stocks.py
from flask import Blueprint, render_template

bp = Blueprint("stocks", __name__)

@bp.route("/")
def index():
    return render_template("stocks.html")