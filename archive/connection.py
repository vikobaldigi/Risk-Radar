from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Define the base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database URL
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'riskradar.db')}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()