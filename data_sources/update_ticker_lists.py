# app/services/update_ticker_lists.py

import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from io import StringIO  # For future-proofing warning

# === CONFIGURATION ===

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

SOURCES = {
    "nasdaq100": {
        "url": "https://en.wikipedia.org/wiki/NASDAQ-100",
        "csv_path": os.path.join(DATA_DIR, "nasdaq100_tickers.csv")
    },
    "dow30": {
        "url": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
        "csv_path": os.path.join(DATA_DIR, "dow30_tickers.csv")
    },
    "russell2000": {
        "url": "https://en.wikipedia.org/wiki/Russell_2000_Index",
        "csv_path": os.path.join(DATA_DIR, "russell2000_tickers.csv")
    }
}

# === FUNCTIONS ===

def fetch_nasdaq100_tickers(url: str) -> list:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    df = pd.read_html(StringIO(str(table)))[0]
    tickers = df['Ticker'].dropna().tolist()
    print(f"✅ Found {len(tickers)} NASDAQ-100 tickers.")
    return tickers

def fetch_dow30_tickers(url: str) -> list:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    df = pd.read_html(StringIO(str(table)))[0]
    tickers = df['Symbol'].dropna().tolist()
    print(f"✅ Found {len(tickers)} Dow 30 tickers.")
    return tickers

def fetch_russell2000_tickers(url: str) -> list:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    df = pd.read_html(StringIO(str(tables[0])))[0]  # Take first big table
    tickers = df['Ticker'].dropna().tolist()
    print(f"✅ Found {len(tickers)} Russell 2000 tickers.")
    return tickers

def save_tickers(tickers: list, path: str):
    df = pd.DataFrame({"ticker": tickers})
    df.to_csv(path, index=False)
    print(f"📄 Saved {len(tickers)} tickers to {os.path.basename(path)}.")

def update_all_indices():
    print("🚀 Updating ticker lists...")

    # NASDAQ-100
    nasdaq100_tickers = fetch_nasdaq100_tickers(SOURCES['nasdaq100']['url'])
    save_tickers(nasdaq100_tickers, SOURCES['nasdaq100']['csv_path'])

    # Dow 30
    dow30_tickers = fetch_dow30_tickers(SOURCES['dow30']['url'])
    save_tickers(dow30_tickers, SOURCES['dow30']['csv_path'])

    # Russell 2000
    russell2000_tickers = fetch_russell2000_tickers(SOURCES['russell2000']['url'])
    save_tickers(russell2000_tickers, SOURCES['russell2000']['csv_path'])

    print("\n🏁 ✅ Ticker lists updated successfully.")

# === MAIN EXECUTION ===

if __name__ == "__main__":
    update_all_indices()