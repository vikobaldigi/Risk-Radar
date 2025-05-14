# app/__init__.py

from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .api.schema_api import bp as schema_bp
    from .api.volatility_api import bp as volatility_bp

    app.register_blueprint(schema_bp, url_prefix="/api")
    app.register_blueprint(volatility_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return jsonify({"status": "ok", "message": "✅ RiskRadar API is live"})

    return app