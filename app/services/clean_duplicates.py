# app/services/clean_duplicates.py

import os
from sqlalchemy import create_engine, text

# === CONFIGURATION ===
# Dynamically locate the SQLite database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{BASE_DIR}/app/database/riskradar.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)


def clean_duplicates():
    """
    1. Remove duplicate rows (identical ticker & date), keeping the first entry by rowid.
    2. VACUUM the database to reclaim space.
    3. Create a unique index on (ticker, date) to prevent future duplicates.
    """
    # 1️⃣ Delete duplicates in a single transaction
    with engine.begin() as conn:
        result = conn.execute(text("""
            DELETE FROM stock_data
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM stock_data
                GROUP BY ticker, date
            );
        """))
        print(f"🗑️  Deleted {result.rowcount} duplicate rows.")

    # 2️⃣ VACUUM and 3️⃣ create unique index
    # VACUUM must run outside of an active transaction
    with engine.connect() as conn:
        conn.execute(text("VACUUM;"))
        print("🧹  Database vacuumed.")
        conn.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_ticker_date
            ON stock_data (ticker, date);
        """))
        print("🔧  Created unique index on (ticker, date).")


if __name__ == "__main__":
    print("🔍  Starting duplicate cleanup and optimization...")
    clean_duplicates()
    print("✅  Cleanup complete.")