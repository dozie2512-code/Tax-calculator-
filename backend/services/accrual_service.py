"""Accrual service with historical data analysis."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import Accrual, Transaction


class AccrualService:
    """Service for managing accruals with historical data analysis."""
    
    @staticmethod
    def calculate_historical_average(
        db: Session,
        category: str,
        lookback_months: int = 6
    ) -> Optional[float]:
        """
        Calculate historical average for a category based on past transactions.
        """
        # Get average of transactions in the category
        result = db.query(
            func.avg(Transaction.amount)
        ).filter(
            Transaction.category == category,
            Transaction.is_reconciled == True
        ).scalar()
        
        return result if result else None
    
    @staticmethod
    def post_payroll_accrual(db: Session, period: str) -> Accrual:
        """
        Post payroll accrual for a period based on historical data.
        """
        # Check if accrual already exists
        existing = db.query(Accrual).filter(
            Accrual.period == period,
            Accrual.accrual_type == 'payroll'
        ).first()
        
        if existing:
            return existing
        
        # Calculate historical average
        historical_avg = AccrualService.calculate_historical_average(
            db, 'payroll', lookback_months=6
        )
        
        # Use historical average or default amount
        if historical_avg and historical_avg > 0:
            amount = historical_avg
            based_on_historical = True
        else:
            # Default fallback amount
            amount = 50000.0
            based_on_historical = False
        
        # Create accrual
        accrual = Accrual(
            period=period,
            accrual_type='payroll',
            description=f'Payroll accrual for {period}',
            amount=amount,
            is_posted=True,
            posted_at=datetime.utcnow(),
            based_on_historical=based_on_historical,
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
        """
        # Check if accrual already exists
        existing = db.query(Accrual).filter(
            Accrual.period == period,
            Accrual.accrual_type == 'utilities'
        ).first()
        
        if existing:
            return existing
        
        # Calculate historical average
        historical_avg = AccrualService.calculate_historical_average(
            db, 'utilities', lookback_months=6
        )
        
        # Use historical average or default amount
        if historical_avg and historical_avg > 0:
            amount = historical_avg
            based_on_historical = True
        else:
            # Default fallback amount
            amount = 1200.0
            based_on_historical = False
        
        # Create accrual
        accrual = Accrual(
            period=period,
            accrual_type='utilities',
            description=f'Utilities accrual for {period}',
            amount=amount,
            is_posted=True,
            posted_at=datetime.utcnow(),
            based_on_historical=based_on_historical,
            historical_average=historical_avg
        )
        
        db.add(accrual)
        db.commit()
        db.refresh(accrual)
        
        return accrual
    
    @staticmethod
    def get_accruals(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        period: Optional[str] = None,
        accrual_type: Optional[str] = None
    ) -> List[Accrual]:
        """
        Get accruals with optional filtering.
        """
        query = db.query(Accrual)
        
        if period:
            query = query.filter(Accrual.period == period)
        
        if accrual_type:
            query = query.filter(Accrual.accrual_type == accrual_type)
        
        return query.offset(skip).limit(limit).all()
