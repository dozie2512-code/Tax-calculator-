"""Accrual database model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from .database import Base


class Accrual(Base):
    """Accrual model representing financial accruals."""
    
    __tablename__ = "accruals"
    
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False, index=True)  # Format: YYYY-MM
    accrual_type = Column(String, nullable=False)  # payroll, utilities
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    is_posted = Column(Boolean, default=False)
    posted_at = Column(DateTime, nullable=True)
    based_on_historical = Column(Boolean, default=False)
    historical_average = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Accrual(id={self.id}, type='{self.accrual_type}', period='{self.period}', amount={self.amount})>"
