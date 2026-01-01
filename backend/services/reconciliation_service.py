"""Reconciliation service with business logic."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
from ..models.reconciliation import ReconciliationRecord
from ..models.transaction import Transaction
from ..models.accrual import Accrual
from .transaction_service import TransactionService
from .accrual_service import AccrualService


class ReconciliationService:
    """Service for managing reconciliation and month-end close."""
    
    @staticmethod
    def get_or_create_reconciliation_record(db: Session, period: str) -> ReconciliationRecord:
        """Get or create a reconciliation record for a period."""
        record = db.query(ReconciliationRecord).filter(
            ReconciliationRecord.period == period
        ).first()
        
        if not record:
            record = ReconciliationRecord(
                period=period,
                status="pending",
                total_transactions=0,
                reconciled_count=0,
                pending_count=0
            )
            db.add(record)
            db.commit()
            db.refresh(record)
        
        return record
    
    @staticmethod
    def update_reconciliation_status(db: Session, period: str) -> ReconciliationRecord:
        """Update reconciliation status based on current transactions."""
        record = ReconciliationService.get_or_create_reconciliation_record(db, period)
        
        # Count transactions for the period
        year, month = period.split("-")
        
        total = db.query(func.count(Transaction.id)).filter(
            func.strftime("%Y-%m", Transaction.date) == period
        ).scalar()
        
        reconciled = db.query(func.count(Transaction.id)).filter(
            func.strftime("%Y-%m", Transaction.date) == period,
            Transaction.is_reconciled == True
        ).scalar()
        
        pending = total - reconciled
        
        # Update record
        record.total_transactions = total
        record.reconciled_count = reconciled
        record.pending_count = pending
        record.updated_at = datetime.utcnow()
        
        if pending == 0 and total > 0:
            record.status = "completed"
        elif reconciled > 0:
            record.status = "in_progress"
        else:
            record.status = "pending"
        
        db.commit()
        db.refresh(record)
        
        return record
    
    @staticmethod
    def autonomous_month_end_close(
        db: Session,
        period: str,
        auto_reconcile: bool = True,
        reconciliation_threshold: float = 1000.0,
        post_payroll_accrual: bool = True,
        post_utilities_accrual: bool = True
    ) -> dict:
        """
        Perform autonomous month-end close process.
        
        Steps:
        1. Auto-reconcile low-risk transactions (if enabled)
        2. Post payroll accruals (if enabled)
        3. Post utilities accruals (if enabled)
        4. Update reconciliation status
        5. Mark as pending manual approval
        
        Args:
            db: Database session
            period: Period to close (YYYY-MM)
            auto_reconcile: Whether to auto-reconcile low-risk transactions
            reconciliation_threshold: Risk threshold for auto-reconciliation
            post_payroll_accrual: Whether to post payroll accruals
            post_utilities_accrual: Whether to post utilities accruals
        
        Returns:
            Dictionary with close results
        """
        reconciled_count = 0
        posted_accruals = 0
        
        # Step 1: Auto-reconcile low-risk transactions
        if auto_reconcile:
            reconciled_count = TransactionService.auto_reconcile_low_risk(
                db, threshold=reconciliation_threshold, period=period
            )
        
        # Step 2: Post payroll accrual
        if post_payroll_accrual:
            # Check if accrual already exists
            existing = db.query(func.count()).filter(
                Accrual.period == period,
                Accrual.accrual_type == "payroll"
            ).scalar()
            
            if existing == 0:
                AccrualService.post_payroll_accrual(db, period)
                posted_accruals += 1
        
        # Step 3: Post utilities accrual
        if post_utilities_accrual:
            # Check if accrual already exists
            existing = db.query(func.count()).filter(
                Accrual.period == period,
                Accrual.accrual_type == "utilities"
            ).scalar()
            
            if existing == 0:
                AccrualService.post_utilities_accrual(db, period)
                posted_accruals += 1
        
        # Step 4: Update reconciliation status
        record = ReconciliationService.update_reconciliation_status(db, period)
        
        # Step 5: Mark as pending approval (not fully closed yet)
        record.notes = "Autonomous month-end close completed. Pending manual approval."
        record.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "period": period,
            "status": "pending_approval",
            "reconciled_transactions": reconciled_count,
            "posted_accruals": posted_accruals,
            "pending_approval": True,
            "message": f"Month-end close for {period} completed. {reconciled_count} transactions auto-reconciled, {posted_accruals} accruals posted. Pending manual approval."
        }
    
    @staticmethod
    def get_reconciliation_status(db: Session, period: str) -> Optional[ReconciliationRecord]:
        """Get reconciliation status for a period."""
        return db.query(ReconciliationRecord).filter(
            ReconciliationRecord.period == period
        ).first()
