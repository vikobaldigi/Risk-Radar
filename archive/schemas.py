from sqlalchemy import Column, Integer, String, Float, Date
from .connection import Base

class StockData(Base):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)