import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# === CONFIGURATION ===

# Find the correct database path dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{BASE_DIR}/app/database/riskradar.db"

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# === FUNCTIONS ===

def get_distinct_tickers() -> list:
    """
    Fetch all distinct stock tickers stored in the database.
    """
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT DISTINCT ticker FROM stock_data"))
        tickers = [row[0] for row in result.fetchall()]
        return tickers
    finally:
        session.close()

def get_all_data_for_ticker(ticker: str) -> pd.DataFrame:
    """
    Fetch all historical price data for a given ticker.
    """
    session = SessionLocal()
    try:
        query = text("""
            SELECT date, open, high, low, close, volume
            FROM stock_data
            WHERE ticker = :ticker
            ORDER BY date ASC
        """)
        df = pd.read_sql_query(query, session.bind, params={"ticker": ticker})
        return df
    finally:
        session.close()

def get_data_by_date_range(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch stock data for a ticker between two dates (inclusive).
    Format: 'YYYY-MM-DD'
    """
    session = SessionLocal()
    try:
        query = text("""
            SELECT date, open, high, low, close, volume
            FROM stock_data
            WHERE ticker = :ticker
              AND date BETWEEN :start_date AND :end_date
            ORDER BY date ASC
        """)
        df = pd.read_sql_query(query, session.bind, params={"ticker": ticker, "start_date": start_date, "end_date": end_date})
        return df
    finally:
        session.close()

def get_recent_n_days(ticker: str, n_days: int = 30) -> pd.DataFrame:
    """
    Fetch the most recent N days of stock data for a given ticker.
    """
    session = SessionLocal()
    try:
        query = text(f"""
            SELECT date, open, high, low, close, volume
            FROM stock_data
            WHERE ticker = :ticker
            ORDER BY date DESC
            LIMIT {n_days}
        """)
        df = pd.read_sql_query(query, session.bind, params={"ticker": ticker})
        return df.sort_values("date")
    finally:
        session.close()

# === QUICK TESTING / DEMO ===

if __name__ == "__main__":
    print("✅ Connected to RiskRadar Database!\n")

    # Show available tickers
    tickers = get_distinct_tickers()
    print(f"📈 {len(tickers)} tickers found.")
    print(tickers[:10], "...")  # Print first 10 tickers as a sample

    # Pick a sample ticker to explore
    sample_ticker = "AAPL"
    print(f"\n🔍 Fetching full history for {sample_ticker}...")
    df_full = get_all_data_for_ticker(sample_ticker)
    print(df_full.head())

    # Fetch by date range
    print(f"\n🗓️ Fetching {sample_ticker} data from 2020-01-01 to 2022-12-31...")
    df_range = get_data_by_date_range(sample_ticker, "2020-01-01", "2022-12-31")
    print(df_range.head())

    # Fetch last N days
    print(f"\n⏳ Fetching last 10 days for {sample_ticker}...")
    df_recent = get_recent_n_days(sample_ticker, n_days=10)
    print(df_recent)