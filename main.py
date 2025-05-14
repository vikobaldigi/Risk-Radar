from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import os
import urllib.request
import pandas as pd

# === Dropbox Config ===
DB_FOLDER = "app/database"
DB_FILE = "riskradar.db"
DB_PATH = os.path.join(DB_FOLDER, DB_FILE)
DROPBOX_URL = "https://www.dropbox.com/scl/fi/x2bgjbm1804rkj5d2izxy/riskradar.db?rlkey=ee0vfjkaf6i0c9dczqurdzfuv&st=boccvoqy&dl=1"

# === Ensure database is downloaded ===
if not os.path.exists(DB_PATH):
    print("⬇️ Downloading riskradar.db from Dropbox...")
    os.makedirs(DB_FOLDER, exist_ok=True)
    urllib.request.urlretrieve(DROPBOX_URL, DB_PATH)
    print("✅ Database downloaded.")

# === Initialize Flask App and SQLite Engine ===
app = Flask(__name__)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

@app.route("/")
def home():
    return jsonify({"message": "✅ RiskRadar API is running."})

@app.route("/api/tickers")
def get_tickers():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT ticker FROM stock_data"))
        tickers = [row[0] for row in result]
    return jsonify(tickers)

@app.route("/api/history/<ticker>")
def get_history(ticker):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT date, close
                FROM stock_data
                WHERE ticker = :ticker
                ORDER BY date DESC
                LIMIT 100
            """), {"ticker": ticker})

            rows = result.fetchall()

            if not rows:
                return jsonify({"error": f"No data found for ticker '{ticker}'"}), 404

            # ✅ Use keys() from ResultMetadata
            keys = result.keys()
            history = [dict(zip(keys, row)) for row in rows]

        return jsonify(history)
    
    except Exception as e:
        # Debug output to logs
        print(f"❌ ERROR in /api/history/{ticker}: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/api/volatility/<ticker>")
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

if __name__ == "__main__":
    app.run(debug=True)