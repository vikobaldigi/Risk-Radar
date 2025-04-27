# app/services/database_explorer.py

import os
import json
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# === CONFIGURATION ===
# Dynamically locate the SQLite database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{BASE_DIR}/app/database/riskradar.db"

# Create engine and session factory
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# === FUNCTIONS ===

def get_all_data() -> pd.DataFrame:
    """
    Load the entire stock_data table into a pandas DataFrame.
    """
    with engine.connect() as conn:
        df = pd.read_sql(
            "SELECT ticker, date, close, volume, open, high, low FROM stock_data ORDER BY ticker, date",
            conn,
        )
    df['date'] = pd.to_datetime(df['date'])
    return df


def check_coverage_summary(df: pd.DataFrame) -> None:
    """
    Print overview of distinct tickers and dates and overall date range.
    """
    print("\n🗓️ === Coverage Summary ===")
    num_tickers = df['ticker'].nunique()
    num_dates = df['date'].nunique()
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    print(f"Distinct tickers: {num_tickers}")
    print(f"Distinct dates : {num_dates}")
    print(f"Date range     : {min_date} to {max_date}")


def check_records_per_date(df: pd.DataFrame) -> None:
    """
    Print count of tickers recorded per date and highlight dates with incomplete coverage.
    """
    print("\n🗓️ === Records per Date ===")
    counts = df.groupby('date')['ticker'].nunique()
    print(f"Distinct dates          : {counts.size}")
    print(f"Average tickers per date: {counts.mean():.1f}")
    print(f"Min tickers in a date   : {counts.min()}")
    print(f"Max tickers in a date   : {counts.max()}")
    max_tickers = counts.max()
    missing = counts[counts < max_tickers]
    if not missing.empty:
        print(f"\n⚠️  Dates with fewer than {max_tickers} tickers (sample 10):")
        print(missing.head(10).to_string())
    else:
        print("All dates have full coverage of tickers.")


def get_summary_statistics(df: pd.DataFrame) -> None:
    """
    Print summary statistics for numerical columns.
    """
    print("\n📊 === Summary Statistics ===")
    print(df.describe())


def check_missing_data(df: pd.DataFrame) -> None:
    """
    Check for missing (null) values in any column.
    """
    print("\n🔎 === Missing Data ===")
    missing = df.isnull().sum()
    if missing.any():
        print(missing[missing > 0])
    else:
        print("No missing values found.")


def check_records_per_ticker(df: pd.DataFrame) -> None:
    """
    Print count of records for each ticker.
    """
    print("\n📈 === Records per Ticker ===")
    counts = df['ticker'].value_counts()
    print(counts)
    print(f"\n🔢 Average records per ticker: {counts.mean():.1f}")
    print(f"📉 Minimum records for a ticker: {counts.min()}")
    print(f"📈 Maximum records for a ticker: {counts.max()}")


def compute_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily returns per ticker: r_t = (close_t / close_{t-1}) - 1.
    """
    df = df.copy()
    df['return'] = df.groupby('ticker')['close'].pct_change()
    return df.dropna(subset=['return'])


def compute_rolling_volatility(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """
    Compute rolling volatility (std dev of returns) per ticker over given window.
    Returns DataFrame with columns: ticker, date, volatility.
    """
    vol = (
        df.groupby('ticker')
          .rolling(window=window, on='date', min_periods=window)['return']
          .std()
          .reset_index()
    )
    vol.rename(columns={'return': 'volatility'}, inplace=True)
    return vol[['ticker', 'date', 'volatility']]


def check_volatility_summary(vol_df: pd.DataFrame, latest_date: pd.Timestamp) -> None:
    """
    Print top and bottom tickers by latest volatility.
    """
    latest = vol_df[vol_df['date'] == latest_date]
    if latest.empty:
        print(f"No volatility data for {latest_date.date()}")
        return
    top = latest.nlargest(10, 'volatility')
    bot = latest.nsmallest(10, 'volatility')
    print(f"\n📈 === Volatility on {latest_date.date()} ===")
    print("Top 10 most volatile tickers:")
    print(top[['ticker', 'volatility']].to_string(index=False))
    print("\nBottom 10 least volatile tickers:")
    print(bot[['ticker', 'volatility']].to_string(index=False))


def compute_volatility_weights(vol_df: pd.DataFrame, target_date: pd.Timestamp) -> pd.DataFrame:
    """
    For a given date, normalize each ticker's volatility into weights.
    Returns DataFrame with ticker, volatility, weight.
    """
    date_vol = vol_df[vol_df['date'] == target_date].copy()
    total_vol = date_vol['volatility'].sum()
    date_vol['weight'] = date_vol['volatility'] / total_vol
    return date_vol[['ticker', 'volatility', 'weight']].sort_values('weight', ascending=False)


def export_to_json(df: pd.DataFrame, filepath: str) -> None:
    """
    Export a DataFrame to JSON with ISO date formatting, records orientation.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_json(filepath, orient='records', date_format='iso')
    print(f"✅ Exported data to {filepath}")


def check_reliability_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute reliability score per ticker based on record counts.
    """
    counts = df['ticker'].value_counts()
    max_count = counts.max()
    rel = (counts / max_count).rename('reliability')
    reliability_df = pd.concat([counts.rename('records'), rel], axis=1)
    print("\n⭐ === Reliability Scores (Top/Bottom 5) ===")
    print(reliability_df.sort_values('reliability', ascending=False).head(5).to_string())
    print(reliability_df.sort_values('reliability', ascending=True).head(5).to_string())
    return reliability_df


def check_duplicate_ticker_dates(df: pd.DataFrame) -> None:
    """
    Detect any duplicate rows sharing the same (ticker, date).
    """
    print("\n🔍 === Duplicate Ticker/Date ===")
    dup = df.duplicated(subset=['ticker', 'date'], keep=False)
    if not dup.any():
        print("✅ No duplicate ticker/date combinations found.")
    else:
        groups = df[dup].groupby(['ticker', 'date']).size().reset_index(name='count')
        total = dup.sum()
        print(f"⚠️  Found {len(groups)} combos with duplicates (total rows: {total}).")
        print(groups.head(10).to_string(index=False))

# === MAIN EXECUTION ===
if __name__ == '__main__':
    print("✅ Connected to RiskRadar Database!\n")

    # Load and prep data
    df_raw = get_all_data()

    # Data health checks
    check_coverage_summary(df_raw)
    check_records_per_date(df_raw)
    get_summary_statistics(df_raw)
    check_missing_data(df_raw)
    check_records_per_ticker(df_raw)
    check_reliability_scores(df_raw)
    check_duplicate_ticker_dates(df_raw)

    # Volatility analysis
    df_ret = compute_daily_returns(df_raw)
    vol_df = compute_rolling_volatility(df_ret, window=30)
    latest = vol_df['date'].max()
    check_volatility_summary(vol_df, latest)
    weights_df = compute_volatility_weights(vol_df, latest)

    # Export data for JS visualizations
    data_dir = os.path.join(BASE_DIR, 'app', 'data')
    export_to_json(vol_df, os.path.join(data_dir, 'volatility.json'))
    export_to_json(weights_df, os.path.join(data_dir, f'weights_{latest.date()}.json'))

    print("\n🏁 ✅ Database exploration and export completed.")