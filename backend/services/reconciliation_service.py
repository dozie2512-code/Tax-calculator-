"""Reconciliation service with business logic."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from ..models import Transaction, ReconciliationRecord
from .accrual_service import AccrualService
from ..utils import get_period_date_range


class ReconciliationService:
    """Service for reconciliation operations."""
    
    @staticmethod
    def _get_period_transaction_query(db: Session, period: str):
        """
        Helper method to get query for transactions in a period.
        
        Args:
            db: Database session
            period: Period in YYYY-MM format
            
        Returns:
            SQLAlchemy query filtered by period
        """
        start_date, end_date = get_period_date_range(period)
        return db.query(Transaction).filter(
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
    
    @staticmethod
    def _get_period_counts(db: Session, period: str) -> tuple[int, int]:
        """
        Helper method to get transaction counts for a period.
        
        Args:
            db: Database session
            period: Period in YYYY-MM format
            
        Returns:
            Tuple of (total_count, reconciled_count)
        """
        query = ReconciliationService._get_period_transaction_query(db, period)
        total = query.count()
        reconciled = query.filter(Transaction.is_reconciled == True).count()
        return total, reconciled
    
    @staticmethod
    def auto_reconcile(
        db: Session,
        threshold: float,
        period: Optional[str] = None
    ) -> dict:
        """
        Auto-reconcile transactions with risk score <= threshold.
        
        Args:
            db: Database session
            threshold: Maximum risk score for auto-reconciliation
            period: Optional period filter (YYYY-MM)
        
        Returns:
            Dictionary with reconciliation results
        """
        # Build query for unreconciled transactions
        query = db.query(Transaction).filter(
            Transaction.is_reconciled == False,
            Transaction.risk_score <= threshold
        )
        
        # Apply period filter if provided
        if period:
            start_date, end_date = get_period_date_range(period)
            query = query.filter(
                Transaction.date >= start_date,
                Transaction.date < end_date
            )
        
        # Get transactions to reconcile
        transactions = query.all()
        
        # Mark as reconciled
        reconciled_count = 0
        for txn in transactions:
            txn.is_reconciled = True
            txn.reconciled_at = datetime.utcnow()
            reconciled_count += 1
        
        db.commit()
        
        # Get total transaction count using helper
        total_query = ReconciliationService._get_period_transaction_query(db, period) if period else db.query(Transaction)
        total_count = total_query.count()
        
        return {
            "reconciled_count": reconciled_count,
            "total_transactions": total_count,
            "threshold_used": threshold
        }
    
    @staticmethod
    def get_reconciliation_status(db: Session, period: str) -> dict:
        """Get reconciliation status for a period."""
        # Use helper method to get counts
        total_count, reconciled_count = ReconciliationService._get_period_counts(db, period)
        pending_count = total_count - reconciled_count
        
        # Check if month-end is closed
        record = db.query(ReconciliationRecord).filter(
            ReconciliationRecord.period == period
        ).first()
        
        is_closed = record.is_month_end_closed if record else False
        status = "completed" if is_closed else ("in_progress" if reconciled_count > 0 else "pending")
        
        percentage = (reconciled_count / total_count * 100) if total_count > 0 else 0.0
        
        return {
            "period": period,
            "status": status,
            "total_transactions": total_count,
            "reconciled_count": reconciled_count,
            "pending_count": pending_count,
            "is_month_end_closed": is_closed,
            "reconciliation_percentage": round(percentage, 2)
        }
    
    @staticmethod
    def month_end_close(
        db: Session,
        period: str,
        auto_reconcile: bool,
        reconciliation_threshold: float,
        post_payroll_accrual: bool,
        post_utilities_accrual: bool
    ) -> dict:
        """
        Perform autonomous month-end close process.
        
        Steps:
        1. Auto-reconcile transactions if requested
        2. Post accruals if requested
        3. Update reconciliation record
        4. Mark period as closed
        """
        accruals_posted = []
        reconciled_count = 0
        
        # Step 1: Auto-reconcile
        if auto_reconcile:
            result = ReconciliationService.auto_reconcile(
                db, reconciliation_threshold, period
            )
            reconciled_count = result["reconciled_count"]
        
        # Step 2: Post accruals
        if post_payroll_accrual:
            AccrualService.post_payroll_accrual(db, period)
            accruals_posted.append("payroll")
        
        if post_utilities_accrual:
            AccrualService.post_utilities_accrual(db, period)
            accruals_posted.append("utilities")
        
        # Step 3: Update or create reconciliation record
        record = db.query(ReconciliationRecord).filter(
            ReconciliationRecord.period == period
        ).first()
        
        if not record:
            # Get counts using helper method
            total, reconciled = ReconciliationService._get_period_counts(db, period)
            
            record = ReconciliationRecord(
                period=period,
                status="completed",
                total_transactions=total,
                reconciled_count=reconciled,
                pending_count=total - reconciled,
                is_month_end_closed=True
            )
            db.add(record)
        else:
            # Update existing record using helper method
            total, reconciled = ReconciliationService._get_period_counts(db, period)
            
            record.status = "completed"
            record.total_transactions = total
            record.reconciled_count = reconciled
            record.pending_count = total - reconciled
            record.is_month_end_closed = True
        
        db.commit()
        db.refresh(record)
        
        return {
            "period": period,
            "status": "completed",
            "reconciled_count": reconciled_count,
            "accruals_posted": accruals_posted,
            "is_closed": True,
            "message": f"Month-end close completed for {period}"
        }
