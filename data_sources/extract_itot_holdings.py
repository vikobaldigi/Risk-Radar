# app/services/extract_itot_holdings.py

import pandas as pd
import os

BASE_DIR = "/Users/vikobal/Documents/RiskRadar"
DATA_DIR = os.path.join(BASE_DIR, "data")

ITOT_FILE = os.path.join(DATA_DIR, "ITOT_holdings.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "itot_tickers.csv")

def extract_itot_tickers():
    print(f"🚀 Loading ITOT holdings from {ITOT_FILE}...")

    # Load the file
    df = pd.read_csv(ITOT_FILE)

    # Show columns
    print("\n🔎 Columns detected in ITOT file:")
    print(df.columns)

    # Detect correct column (either 'Ticker', 'Symbol', etc.)
    possible_columns = ['Ticker', 'ticker', 'Symbol', 'symbol']
    ticker_col = None

    for col in possible_columns:
        if col in df.columns:
            ticker_col = col
            break

    if not ticker_col:
        raise ValueError("❌ Could not find ticker/symbol column!")

    # Extract tickers
    tickers = df[ticker_col].dropna().unique().tolist()

    # Save clean file
    output_df = pd.DataFrame({"ticker": sorted(tickers)})
    output_df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Extracted and saved {len(tickers)} ITOT tickers to {OUTPUT_FILE}.")

if __name__ == "__main__":
    extract_itot_tickers()