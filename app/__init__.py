# app/__init__.py
import os
from flask import Flask
from .api.volatility_api import bp as vol_bp
from .routes.stocks      import bp as stocks_bp

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join("app", "static"),
        template_folder=os.path.join("app", "templates"),
    )
    # JSON endpoints
    app.register_blueprint(vol_bp)
    # HTML route
    app.register_blueprint(stocks_bp)
    return app
