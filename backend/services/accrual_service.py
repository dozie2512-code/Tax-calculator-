"""Accrual service with business logic."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional
from ..models.accrual import Accrual
from ..models.transaction import Transaction
from ..schemas import AccrualCreate


class AccrualService:
    """Service for managing accruals."""
    
    @staticmethod
    def calculate_historical_average(
        db: Session,
        category: str,
        months_back: int = 3
    ) -> float:
        """
        Calculate historical average for a category based on past transactions.
        
        Args:
            db: Database session
            category: Transaction category to analyze
            months_back: Number of months to look back
        
        Returns:
            Average amount for the category
        """
        # Get transactions for the category from past months
        transactions = db.query(Transaction).filter(
            Transaction.category.ilike(f"%{category}%"),
            Transaction.is_reconciled == True
        ).order_by(Transaction.date.desc()).limit(months_back * 10).all()
        
        if not transactions:
            # Return default values if no historical data
            if "payroll" in category.lower():
                return 50000.0  # Default payroll
            elif "utilities" in category.lower() or "utility" in category.lower():
                return 5000.0  # Default utilities
            return 0.0
        
        # Calculate average
        total = sum(t.amount for t in transactions)
        return total / len(transactions)
    
    @staticmethod
    def post_payroll_accrual(db: Session, period: str) -> Accrual:
        """
        Post payroll accrual based on historical data.
        
        Args:
            db: Database session
            period: Period for accrual (YYYY-MM)
        
        Returns:
            Created accrual
        """
        # Calculate historical average
        historical_avg = AccrualService.calculate_historical_average(
            db, category="payroll", months_back=3
        )
        
        # Create accrual
        accrual = Accrual(
            period=period,
            accrual_type="payroll",
            description=f"Payroll accrual for {period}",
            amount=historical_avg,
            is_posted=True,
            posted_at=datetime.utcnow(),
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
        Post utilities accrual based on historical data.
        
        Args:
            db: Database session
            period: Period for accrual (YYYY-MM)
        
        Returns:
            Created accrual
        """
        # Calculate historical average
        historical_avg = AccrualService.calculate_historical_average(
            db, category="utilities", months_back=3
        )
        
        # Create accrual
        accrual = Accrual(
            period=period,
            accrual_type="utilities",
            description=f"Utilities accrual for {period}",
            amount=historical_avg,
            is_posted=True,
            posted_at=datetime.utcnow(),
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
        skip: int = 0,
        limit: int = 100,
        period: Optional[str] = None,
        accrual_type: Optional[str] = None
    ) -> List[Accrual]:
        """Get accruals with optional filtering."""
        query = db.query(Accrual)
        
        if period:
            query = query.filter(Accrual.period == period)
        
        if accrual_type:
            query = query.filter(Accrual.accrual_type == accrual_type)
        
        return query.offset(skip).limit(limit).all()
