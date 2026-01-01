"""Reconciliation router with API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..models.database import get_db
from ..schemas import (
    ReconciliationRequest,
    ReconciliationResponse,
    ReconciliationStatusResponse,
    MonthEndCloseRequest,
    MonthEndCloseResponse
)
from ..services.reconciliation_service import ReconciliationService
from ..services.transaction_service import TransactionService

router = APIRouter(prefix="/reconciliation", tags=["reconciliation"])


@router.post("/auto", response_model=ReconciliationResponse)
def auto_reconcile_transactions(
    request: ReconciliationRequest,
    db: Session = Depends(get_db)
):
    """
    Auto-reconcile low-risk transactions.
    
    This endpoint automatically reconciles transactions with a risk score
    below the specified threshold. The risk score is calculated based on
    transaction amount, category, and vendor information.
    
    - **threshold**: Maximum risk score for auto-reconciliation (default: 1000.0)
    - **period**: Optional period filter (YYYY-MM format)
    """
    # Perform auto-reconciliation
    reconciled_count = TransactionService.auto_reconcile_low_risk(
        db, threshold=request.threshold, period=request.period
    )
    
    # Update reconciliation status
    if request.period:
        record = ReconciliationService.update_reconciliation_status(db, request.period)
        
        return ReconciliationResponse(
            period=record.period,
            reconciled_count=reconciled_count,
            total_transactions=record.total_transactions,
            pending_count=record.pending_count
        )
    else:
        return ReconciliationResponse(
            period="all",
            reconciled_count=reconciled_count,
            total_transactions=reconciled_count,
            pending_count=0
        )


@router.get("/status", response_model=ReconciliationStatusResponse)
def get_reconciliation_status(
    period: str = Query(..., description="Period to check (YYYY-MM)", regex=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db)
):
    """
    Get reconciliation status for a specific period.
    
    This endpoint returns the current reconciliation status including
    total transactions, reconciled count, and pending count.
    
    - **period**: Period in YYYY-MM format (e.g., "2026-01")
    """
    # Update status first
    record = ReconciliationService.update_reconciliation_status(db, period)
    
    if not record:
        raise HTTPException(status_code=404, detail=f"No reconciliation record found for period {period}")
    
    return record


@router.post("/month-end/close", response_model=MonthEndCloseResponse)
def autonomous_month_end_close(
    request: MonthEndCloseRequest,
    db: Session = Depends(get_db)
):
    """
    Perform autonomous month-end close process.
    
    This endpoint executes a comprehensive month-end close process that includes:
    1. Auto-reconciliation of low-risk transactions
    2. Posting of payroll accruals based on historical data
    3. Posting of utilities accruals based on historical data
    4. Updating reconciliation status
    
    The process is marked as pending manual approval after completion.
    
    - **period**: Period to close (YYYY-MM format)
    - **auto_reconcile**: Whether to auto-reconcile low-risk transactions
    - **reconciliation_threshold**: Risk threshold for auto-reconciliation
    - **post_payroll_accrual**: Whether to post payroll accruals
    - **post_utilities_accrual**: Whether to post utilities accruals
    """
    result = ReconciliationService.autonomous_month_end_close(
        db=db,
        period=request.period,
        auto_reconcile=request.auto_reconcile,
        reconciliation_threshold=request.reconciliation_threshold,
        post_payroll_accrual=request.post_payroll_accrual,
        post_utilities_accrual=request.post_utilities_accrual
    )
    
    return MonthEndCloseResponse(**result)
