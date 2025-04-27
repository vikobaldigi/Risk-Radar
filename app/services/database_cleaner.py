# app/services/database_cleaner.py

import os
from sqlalchemy import create_engine, text

# ——— CONFIGURATION ———
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{BASE_DIR}/app/database/riskradar.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

def find_duplicate_keys():
    """
    Returns all (ticker, date) combos that occur more than once.
    """
    dup_query = text("""
        SELECT ticker, date, COUNT(*) AS cnt
        FROM stock_data
        GROUP BY ticker, date
        HAVING cnt > 1
    """)
    with engine.connect() as conn:
        return conn.execute(dup_query).fetchall()

def remove_duplicates():
    """
    Deletes all but the first row for each (ticker, date).
    """
    delete_stmt = text("""
        DELETE FROM stock_data
        WHERE rowid NOT IN (
          SELECT MIN(rowid)
          FROM stock_data
          GROUP BY ticker, date
        )
    """)
    with engine.begin() as conn:
        result = conn.execute(delete_stmt)
        print(f"🗑️  Deleted {result.rowcount} duplicate rows.")

def vacuum_and_index():
    """
    Reclaim free space and add unique index to prevent future dupes.
    """
    with engine.begin() as conn:
        conn.execute(text("VACUUM"))
        conn.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_ticker_date
            ON stock_data(ticker, date)
        """))
        print("🛠  Vacuumed database and created unique index on (ticker, date).")

if __name__ == "__main__":
    print("🔍  Checking for duplicate (ticker, date) entries…")
    dupes = find_duplicate_keys()
    if not dupes:
        print("✅  No duplicates found.")
    else:
        print(f"⚠️  Found {len(dupes)} duplicate key(s). Cleaning up…")
        remove_duplicates()
        vacuum_and_index()
        print("✅  Cleanup complete.")