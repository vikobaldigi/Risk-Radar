import os
from flask import Blueprint, send_file

bp = Blueprint("volatility_api", __name__, static_folder=None)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@bp.route("/weights/<date>")
def get_weights(date):
    path = os.path.join(DATA_DIR, f"weights_{date}.json")
    return send_file(path, mimetype="application/json")