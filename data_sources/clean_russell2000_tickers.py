# app/services/clean_russell2000_tickers.py

import pandas as pd
import os

# === CONFIGURATION ===

BASE_DIR = "/Users/vikobal/Documents/RiskRadar"
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_FILE = os.path.join(DATA_DIR, "russell2000_tickers.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "russell2000_tickers_cleaned.csv")

# === PROCESSING ===

def clean_russell_tickers():
    print(f"🧹 Loading {INPUT_FILE}...")

    # Read the file while skipping duplicated header rows
    df = pd.read_csv(INPUT_FILE)

    # Remove rows where ticker equals 'ticker' (sometimes second header sneaks in)
    df = df[df['ticker'].str.lower() != 'ticker']

    # Strip quotation marks, whitespace
    df['ticker'] = df['ticker'].str.replace('"', '', regex=False).str.strip()

    # Drop any empty tickers after cleaning
    df = df[df['ticker'] != ""]

    # Sort alphabetically
    df = df.sort_values(by="ticker").reset_index(drop=True)

    # Save cleaned version
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Cleaned and saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    clean_russell_tickers()