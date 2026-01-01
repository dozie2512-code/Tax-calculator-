"""Reconciliation service with business logic."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from ..models import Transaction, ReconciliationRecord
from .accrual_service import AccrualService


class ReconciliationService:
    """Service for reconciliation operations."""
    
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
            year, month = period.split("-")
            query = query.filter(
                Transaction.date >= datetime(int(year), int(month), 1)
            )
            if int(month) < 12:
                query = query.filter(
                    Transaction.date < datetime(int(year), int(month) + 1, 1)
                )
            else:
                query = query.filter(
                    Transaction.date < datetime(int(year) + 1, 1, 1)
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
        
        # Get total transaction count
        total_query = db.query(Transaction)
        if period:
            year, month = period.split("-")
            total_query = total_query.filter(
                Transaction.date >= datetime(int(year), int(month), 1)
            )
            if int(month) < 12:
                total_query = total_query.filter(
                    Transaction.date < datetime(int(year), int(month) + 1, 1)
                )
            else:
                total_query = total_query.filter(
                    Transaction.date < datetime(int(year) + 1, 1, 1)
                )
        
        total_count = total_query.count()
        
        return {
            "reconciled_count": reconciled_count,
            "total_transactions": total_count,
            "threshold_used": threshold
        }
    
    @staticmethod
    def get_reconciliation_status(db: Session, period: str) -> dict:
        """Get reconciliation status for a period."""
        year, month = period.split("-")
        
        # Query transactions for the period
        query = db.query(Transaction).filter(
            Transaction.date >= datetime(int(year), int(month), 1)
        )
        if int(month) < 12:
            query = query.filter(
                Transaction.date < datetime(int(year), int(month) + 1, 1)
            )
        else:
            query = query.filter(
                Transaction.date < datetime(int(year) + 1, 1, 1)
            )
        
        total_count = query.count()
        reconciled_count = query.filter(Transaction.is_reconciled == True).count()
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
            # Get counts
            year, month = period.split("-")
            query = db.query(Transaction).filter(
                Transaction.date >= datetime(int(year), int(month), 1)
            )
            if int(month) < 12:
                query = query.filter(
                    Transaction.date < datetime(int(year), int(month) + 1, 1)
                )
            else:
                query = query.filter(
                    Transaction.date < datetime(int(year) + 1, 1, 1)
                )
            
            total = query.count()
            reconciled = query.filter(Transaction.is_reconciled == True).count()
            
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
            # Update existing record
            year, month = period.split("-")
            query = db.query(Transaction).filter(
                Transaction.date >= datetime(int(year), int(month), 1)
            )
            if int(month) < 12:
                query = query.filter(
                    Transaction.date < datetime(int(year), int(month) + 1, 1)
                )
            else:
                query = query.filter(
                    Transaction.date < datetime(int(year) + 1, 1, 1)
                )
            
            total = query.count()
            reconciled = query.filter(Transaction.is_reconciled == True).count()
            
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
