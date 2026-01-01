"""Transaction database model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from .database import Base


class Transaction(Base):
    """Transaction model representing financial transactions."""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    vendor = Column(String, nullable=True)
    risk_score = Column(Float, default=0.0)
    is_reconciled = Column(Boolean, default=False)
    reconciled_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, description='{self.description}', amount={self.amount})>"
