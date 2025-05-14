# app/api/weights_api.py
import os
from flask import Blueprint, send_file

bp = Blueprint("weights_api", __name__)

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

@bp.route("/weights/<date>")
def get_weights(date: str):
    fname = f"weights_{date}.json"
    path = os.path.join(DATA_DIR, fname)
    return send_file(path, mimetype="application/json",
                     download_name=fname, as_attachment=False)