"""Accrual database model."""
from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base


class Accrual(Base):
    """Accrual database model."""
    
    __tablename__ = "accruals"

    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False, index=True)  # YYYY-MM format
    accrual_type = Column(String, nullable=False)  # payroll, utilities
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    is_posted = Column(Boolean, default=True)
    based_on_historical = Column(Boolean, default=False)
    historical_average = Column(Float, nullable=True)
