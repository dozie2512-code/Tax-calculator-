"""Reconciliation record model for database."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime
from .database import Base


class ReconciliationRecord(Base):
    """ReconciliationRecord model for tracking reconciliation activities."""
    
    __tablename__ = "reconciliation_records"
    
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False)  # e.g., "2026-01"
    status = Column(String, default="pending")  # pending, completed, approved
    total_transactions = Column(Integer, default=0)
    reconciled_count = Column(Integer, default=0)
    pending_count = Column(Integer, default=0)
    is_month_end_closed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
