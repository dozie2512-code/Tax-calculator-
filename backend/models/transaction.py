"""Transaction model for database."""
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from datetime import datetime
from .database import Base


class Transaction(Base):
    """Transaction model representing financial transactions."""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    vendor = Column(String, nullable=True)
    risk_score = Column(Float, default=0.0)
    is_reconciled = Column(Boolean, default=False)
    reconciled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
