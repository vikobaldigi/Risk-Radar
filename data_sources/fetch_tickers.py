# app/services/fetch_tickers.py

import pandas as pd
import os

# === CONFIGURATION ===

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Paths to your individual index CSV files
SOURCES = {
    "sp500": os.path.join(DATA_DIR, "sp500_tickers.csv"),
    "nasdaq100": os.path.join(DATA_DIR, "nasdaq100_tickers.csv"),
    "dow30": os.path.join(DATA_DIR, "dow30_tickers.csv"),
    "russell2000": os.path.join(DATA_DIR, "russell2000_tickers.csv"),
}

MASTER_FILE = os.path.join(DATA_DIR, "master_tickers.csv")

# === FUNCTIONS ===

def load_ticker_list(path: str) -> list:
    """
    Load ticker list from a given CSV path.
    """
    if not os.path.exists(path):
        print(f"⚠️ Warning: {path} not found.")
        return []
    
    try:
        df = pd.read_csv(path)
        if 'ticker' not in df.columns:
            print(f"⚠️ Warning: {os.path.basename(path)} has no 'ticker' column.")
            return []
        tickers = df['ticker'].dropna().unique().tolist()
        print(f"✅ Loaded {len(tickers)} tickers from {os.path.basename(path)}.")
        return tickers
    except pd.errors.EmptyDataError:
        print(f"⚠️ Warning: {os.path.basename(path)} is empty. Skipping...")
        return []

def combine_tickers_and_remove_duplicates():
    """
    Combine all ticker lists from different sources and remove duplicates.
    """
    all_tickers = []

    for name, path in SOURCES.items():
        tickers = load_ticker_list(path)
        all_tickers.extend(tickers)

    # Remove duplicates
    unique_tickers = sorted(list(set(all_tickers)))

    if unique_tickers:
        # Save to master_tickers.csv
        master_df = pd.DataFrame({"ticker": unique_tickers})
        master_df.to_csv(MASTER_FILE, index=False)
        print(f"\n🏁 ✅ Master ticker list created successfully with {len(unique_tickers)} unique tickers.")
        print(f"📄 Saved to {MASTER_FILE}")
    else:
        print("\n⚠️ No tickers found to save. Master ticker list not created.")

# === MAIN ===

if __name__ == "__main__":
    print("🚀 Combining tickers from all indices...\n")
    combine_tickers_and_remove_duplicates()