# app/services/combine_all_tickers.py

import pandas as pd
import os

BASE_DIR = "/Users/vikobal/Documents/RiskRadar"
DATA_DIR = os.path.join(BASE_DIR, "data")

# All your ticker files
ticker_files = [
    "sp500_tickers.csv",
    "nasdaq100_tickers.csv",
    "dow30_tickers.csv",
    "russell2000_tickers.csv",
    "itot_tickers.csv"  # NEW!
]

MASTER_OUTPUT = os.path.join(DATA_DIR, "master_tickers.csv")

def combine_all_tickers():
    print("🚀 Combining all ticker files...")

    tickers = []

    for file in ticker_files:
        path = os.path.join(DATA_DIR, file)
        if os.path.exists(path):
            df = pd.read_csv(path)
            if 'ticker' in df.columns:
                tickers.extend(df['ticker'].dropna().tolist())
                print(f"✅ Loaded {len(df)} tickers from {file}.")
            else:
                print(f"⚠️ Warning: No 'ticker' column in {file}. Skipping.")
        else:
            print(f"⚠️ Warning: {file} does not exist.")

    # Deduplicate tickers
    unique_tickers = sorted(set(tickers))

    # Save final master
    master_df = pd.DataFrame({"ticker": unique_tickers})
    master_df.to_csv(MASTER_OUTPUT, index=False)

    print(f"\n🏁 ✅ Master ticker list created successfully with {len(unique_tickers)} unique tickers.")
    print(f"📄 Saved to {MASTER_OUTPUT}")

if __name__ == "__main__":
    combine_all_tickers()