"""Accrual model for database."""
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from datetime import datetime
from .database import Base


class Accrual(Base):
    """Accrual model representing financial accruals."""
    
    __tablename__ = "accruals"
    
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False)  # e.g., "2026-01"
    accrual_type = Column(String, nullable=False)  # "payroll" or "utilities"
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    is_posted = Column(Boolean, default=False)
    posted_at = Column(DateTime, nullable=True)
    based_on_historical = Column(Boolean, default=False)
    historical_average = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
