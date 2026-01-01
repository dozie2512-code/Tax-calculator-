"""Reconciliation record database model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from .database import Base


class ReconciliationRecord(Base):
    """ReconciliationRecord model tracking month-end close status."""
    
    __tablename__ = "reconciliation_records"
    
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False, index=True)  # Format: YYYY-MM
    status = Column(String, nullable=False, default="pending")  # pending, in_progress, completed
    total_transactions = Column(Integer, default=0)
    reconciled_count = Column(Integer, default=0)
    pending_count = Column(Integer, default=0)
    is_month_end_closed = Column(Boolean, default=False)
    month_end_closed_at = Column(DateTime, nullable=True)
    workflow_steps = Column(Text, nullable=True)  # JSON string of workflow steps
    requires_approval = Column(Boolean, default=True)
    approved_by = Column(String, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ReconciliationRecord(id={self.id}, period='{self.period}', status='{self.status}')>"
