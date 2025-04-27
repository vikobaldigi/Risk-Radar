# app/services/extract_russell2000_from_iShares.py

import pandas as pd
import os

# === CONFIGURATION ===

BASE_DIR = "/Users/vikobal/Documents/RiskRadar"
DATA_DIR = os.path.join(BASE_DIR, "data")

IWM_FILE = os.path.join(DATA_DIR, "iShares_Russell2000_holdings.csv")
RUSSELL2000_OUTPUT = os.path.join(DATA_DIR, "russell2000_tickers.csv")

# === PROCESSING ===

def extract_russell2000_tickers():
    print(f"🚀 Loading Russell 2000 holdings from {IWM_FILE}...")

    # Open manually
    with open(IWM_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find start of real table
    data_lines = []
    start_collecting = False

    for line in lines:
        if "Ticker" in line and "Name" in line:
            start_collecting = True
            continue  # skip the header line itself
        if start_collecting:
            if line.strip() == "":
                break  # stop collecting at empty line (end of table)
            data_lines.append(line.strip())

    if not data_lines:
        print("❌ Could not find any ticker data!")
        return

    # Now manually parse
    tickers = []
    for line in data_lines:
        fields = line.split(",")
        if fields and len(fields) > 0:
            ticker = fields[0].strip()
            if ticker and ticker != "-":
                tickers.append(ticker)

    tickers = sorted(set(tickers))  # remove duplicates

    print(f"✅ Found {len(tickers)} unique Russell 2000 tickers.")

    # Save cleaned tickers
    df_out = pd.DataFrame({"ticker": tickers})
    df_out.to_csv(RUSSELL2000_OUTPUT, index=False)

    print(f"📄 Saved Russell 2000 tickers to {RUSSELL2000_OUTPUT}.")

if __name__ == "__main__":
    extract_russell2000_tickers()