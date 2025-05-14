# app/api/volatility_api.py

import os
import pandas as pd
from flask import Blueprint, request, jsonify, send_file
from sqlalchemy import text
from app.database import engine

bp = Blueprint("volatility_api", __name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@bp.route("/weights/<date>")
def get_weights(date):
    path = os.path.join(DATA_DIR, f"weights_{date}.json")
    return send_file(path, mimetype="application/json")

@bp.route("/tickers")
def get_tickers():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT ticker FROM stock_data"))
        tickers = [row[0] for row in result]
    return jsonify(tickers)

@bp.route("/history/<ticker>")
def get_history(ticker):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT date, open, high, low, close, volume
                FROM stock_data
                WHERE ticker = :ticker
                ORDER BY date DESC
                LIMIT 100
            """), {"ticker": ticker})

            rows = result.fetchall()
            keys = result.keys()
            history = [dict(zip(keys, row)) for row in rows]

        return jsonify(history)

    except Exception as e:
        print(f"❌ Error in get_history: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route("/volatility/<ticker>")
def get_volatility(ticker):
    window = int(request.args.get("window", 30))
    with engine.connect() as conn:
        df = pd.read_sql_query("""
            SELECT date, close
            FROM stock_data
            WHERE ticker = :ticker
            ORDER BY date ASC
        """, conn, params={"ticker": ticker})

    if df.empty or len(df) < window:
        return jsonify({"error": "Not enough data to compute volatility"}), 400

    df['return'] = df['close'].pct_change()
    df['volatility'] = df['return'].rolling(window).std()
    df = df.dropna()

    return jsonify(df[['date', 'volatility']].tail(30).to_dict(orient='records'))