# app/services/clean_duplicates.py

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# === CONFIGURATION ===

# Find the correct database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{BASE_DIR}/app/database/riskradar.db"

# Setup SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# === FUNCTIONS ===

def find_duplicates():
    """
    Find ticker/date duplicates.
    """
    session = SessionLocal()
    try:
        query = text("""
            SELECT ticker, date, COUNT(*) as cnt
            FROM stock_data
            GROUP BY ticker, date
            HAVING cnt > 1
        """)
        duplicates = session.execute(query).fetchall()
        return duplicates
    finally:
        session.close()

def delete_duplicates():
    """
    Keep only 1 record per ticker/date combination.
    """
    session = SessionLocal()
    try:
        # Find all duplicate ticker/date combos
        duplicates = find_duplicates()
        print(f"🔎 Found {len(duplicates)} duplicate ticker/date pairs.")

        for ticker, date, count in duplicates:
            # Find all IDs for that ticker/date
            ids_query = text("""
                SELECT id
                FROM stock_data
                WHERE ticker = :ticker AND date = :date
                ORDER BY id ASC
            """)
            rows = session.execute(ids_query, {"ticker": ticker, "date": date}).fetchall()
            ids = [row[0] for row in rows]

            # Keep the first ID, delete the rest
            ids_to_delete = ids[1:]

            if ids_to_delete:
                # Build dynamic delete query
                placeholders = ", ".join([str(id) for id in ids_to_delete])
                delete_sql = f"""
                    DELETE FROM stock_data
                    WHERE id IN ({placeholders})
                """
                session.execute(text(delete_sql))

        session.commit()
        print("✅ Duplicates cleaned successfully!")

    except Exception as e:
        session.rollback()
        print(f"❌ Error during duplicate cleanup: {e}")
    finally:
        session.close()

# === RUN SCRIPT ===

if __name__ == "__main__":
    print("🧹 Connecting to RiskRadar database to clean duplicates...\n")
    delete_duplicates()