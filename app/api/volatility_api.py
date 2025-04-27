# app/api/volatility_api.py
from flask import Blueprint, send_file
import os

bp = Blueprint("vol_api", __name__, url_prefix="/api")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@bp.route("/volatility_30d")
def get_volatility():
    return send_file(
        os.path.join(DATA_DIR, "volatility_30d.json"),
        mimetype="application/json"
    )

@bp.route("/weights/<date>")
def get_weights(date):
    return send_file(
        os.path.join(DATA_DIR, f"weights_{date}.json"),
        mimetype="application/json"
    )