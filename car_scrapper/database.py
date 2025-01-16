# database.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DB_URI = "sqlite:///listings.db"
Base = declarative_base()
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(String, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    location = Column(String)
    year = Column(Integer)
    mileage = Column(Integer)
    last_seen = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    listing_id = Column(String, ForeignKey('listings.id'))
    old_price = Column(Integer)
    new_price = Column(Integer)
    changed_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
