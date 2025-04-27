from flask import Blueprint, jsonify, send_file
import os

bp = Blueprint("volt", __name__, url_prefix="/api")

@bp.route("/volatility_30d")
def vol_30d():
    path = os.path.join(os.path.dirname(__file__), "../data/volatility.json")
    return send_file(path, mimetype="application/json")

@bp.route("/weights/<date>")
def weights(date):
    path = os.path.join(os.path.dirname(__file__), f"../data/weights_{date}.json")
    return send_file(path, mimetype="application/json")