from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="static/frontend", template_folder="templates")
    CORS(app)  # enable if you serve frontend separately

    # import and register your API blueprint
    from .api.volatility_api import bp as vol_bp
    app.register_blueprint(vol_bp, url_prefix="/api")

    @app.route("/")
    def home():
        # serves static/frontend/index.html
        return app.send_static_file("index.html")

    return app