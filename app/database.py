# app/database.py

import os
import urllib.request
from sqlalchemy import create_engine

DB_FOLDER = os.path.join(os.path.dirname(__file__), "database")
DB_FILE = "riskradar.db"
DB_PATH = os.path.join(DB_FOLDER, DB_FILE)
DROPBOX_URL = "https://www.dropbox.com/scl/fi/x2bgjbm1804rkj5d2izxy/riskradar.db?rlkey=ee0vfjkaf6i0c9dczqurdzfuv&st=boccvoqy&dl=1"

# Ensure database is downloaded
if not os.path.exists(DB_PATH):
    print("⬇️ Downloading riskradar.db from Dropbox...")
    os.makedirs(DB_FOLDER, exist_ok=True)
    urllib.request.urlretrieve(DROPBOX_URL, DB_PATH)
    print("✅ Database downloaded.")

# Create SQLAlchemy engine
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)