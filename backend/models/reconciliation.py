"""Reconciliation record database model."""
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class ReconciliationRecord(Base):
    """Reconciliation record database model."""
    
    __tablename__ = "reconciliation_records"

    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False, index=True)  # YYYY-MM format
    status = Column(String, default="pending")  # pending, in_progress, completed
    total_transactions = Column(Integer, default=0)
    reconciled_count = Column(Integer, default=0)
    pending_count = Column(Integer, default=0)
    is_month_end_closed = Column(Boolean, default=False)
