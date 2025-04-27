# app/services/clean_master_tickers.py

import pandas as pd
import os
import re

BASE_DIR = "/Users/vikobal/Documents/RiskRadar"
DATA_DIR = os.path.join(BASE_DIR, "data")

MASTER_FILE = os.path.join(DATA_DIR, "master_tickers.csv")
CLEANED_MASTER_FILE = os.path.join(DATA_DIR, "master_tickers_cleaned.csv")

def clean_master_tickers():
    print(f"🧹 Loading {MASTER_FILE}...")

    df = pd.read_csv(MASTER_FILE)

    if 'ticker' not in df.columns:
        raise ValueError("❌ No 'ticker' column found!")

    # Step 1: Drop NA and duplicates
    df = df.dropna()
    df = df.drop_duplicates()

    # Step 2: Strip whitespace and invalid symbols
    df['ticker'] = df['ticker'].str.strip()

    # Step 3: Filter only valid tickers
    # Valid tickers: letters, numbers, dots, dashes
    df = df[df['ticker'].apply(lambda x: bool(re.match(r'^[A-Za-z0-9\.-]+$', str(x))))]

    # Step 4: Remove tickers that are too short or obviously broken
    df = df[df['ticker'].str.len() >= 1]
    df = df[df['ticker'] != '-']

    # Step 5: Save cleaned file
    df = df.sort_values(by='ticker').reset_index(drop=True)
    df.to_csv(CLEANED_MASTER_FILE, index=False)

    print(f"✅ Cleaned tickers saved to {CLEANED_MASTER_FILE}.")
    print(f"✅ {len(df)} tickers remaining after cleaning.")

if __name__ == "__main__":
    clean_master_tickers()