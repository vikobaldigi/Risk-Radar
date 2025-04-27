# app/__init__.py
import os
from flask import Flask, redirect, url_for
from .api.volatility_api import bp as vol_bp
from .routes.stocks      import bp as stocks_bp

def create_app():
    # root_path is automatically set to the folder containing this file (app/)
    app = Flask(
        __name__,
        static_folder="static",     # ← looks in app/static/
        template_folder="templates" # ← looks in app/templates/
    )

    # Register your blueprints
    app.register_blueprint(vol_bp)      # serves /api/…
    app.register_blueprint(stocks_bp)   # serves /stocks

    # Optional: redirect “/” to “/stocks/”
    @app.route("/")
    def home():
        return redirect(url_for("stocks.index"))

    return app
