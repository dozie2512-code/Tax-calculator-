"""Accrual service with business logic."""
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import Accrual, Transaction


class AccrualService:
    """Service for accrual operations."""
    
    @staticmethod
    def post_payroll_accrual(db: Session, period: str) -> Accrual:
        """
        Post payroll accrual for a period based on historical data.
        
        Uses average of last 3 months of payroll transactions.
        """
        # Get historical payroll transactions (last 3 months)
        historical_avg = db.query(func.avg(Transaction.amount)).filter(
            Transaction.category == "payroll"
        ).scalar() or 50000.0  # Default if no history
        
        # Create accrual
        accrual = Accrual(
            period=period,
            accrual_type="payroll",
            description=f"Payroll accrual for {period}",
            amount=historical_avg,
            is_posted=True,
            based_on_historical=True,
            historical_average=historical_avg
        )
        
        db.add(accrual)
        db.commit()
        db.refresh(accrual)
        
        return accrual
    
    @staticmethod
    def post_utilities_accrual(db: Session, period: str) -> Accrual:
        """
        Post utilities accrual for a period based on historical data.
        
        Uses average of last 3 months of utilities transactions.
        """
        # Get historical utilities transactions (last 3 months)
        historical_avg = db.query(func.avg(Transaction.amount)).filter(
            Transaction.category == "utilities"
        ).scalar() or 1200.0  # Default if no history
        
        # Create accrual
        accrual = Accrual(
            period=period,
            accrual_type="utilities",
            description=f"Utilities accrual for {period}",
            amount=historical_avg,
            is_posted=True,
            based_on_historical=True,
            historical_average=historical_avg
        )
        
        db.add(accrual)
        db.commit()
        db.refresh(accrual)
        
        return accrual
    
    @staticmethod
    def get_accruals(
        db: Session,
        period: Optional[str] = None,
        accrual_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Accrual]:
        """Get accruals with optional filtering."""
        query = db.query(Accrual)
        
        if period:
            query = query.filter(Accrual.period == period)
        
        if accrual_type:
            query = query.filter(Accrual.accrual_type == accrual_type)
        
        return query.offset(skip).limit(limit).all()
