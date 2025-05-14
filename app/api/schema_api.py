# app/api/schema_api.py

from flask import Blueprint, jsonify
from sqlalchemy import text
from .. import engine  # Assumes engine is exposed in app/__init__.py

bp = Blueprint("schema_api", __name__)

@bp.route("/api/schema")
def get_schema():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(stock_data);"))
            schema = [
                {
                    "cid": row[0],
                    "name": row[1],
                    "type": row[2],
                    "notnull": row[3],
                    "default": row[4],
                    "pk": row[5]
                }
                for row in result
            ]
        return jsonify(schema)

    except Exception as e:
        print(f"❌ Error in get_schema: {e}")
        return jsonify({"error": str(e)}), 500