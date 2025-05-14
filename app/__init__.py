# app/__init__.py

from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="static/frontend", template_folder="templates")
    CORS(app)

    # import and register blueprints
    from .api.volatility_api import bp as vol_bp
    from .api.schema_api import bp as schema_bp

    app.register_blueprint(vol_bp, url_prefix="/api")
    app.register_blueprint(schema_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return app.send_static_file("index.html")

    return app