"""Reconciliation API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.models import get_db
from backend.schemas import (
    AutoReconcileRequest,
    AutoReconcileResponse,
    ReconciliationStatusResponse,
    MonthEndCloseRequest,
    MonthEndCloseResponse,
    WorkflowStep
)
from backend.services import ReconciliationService

router = APIRouter(prefix="/reconciliation", tags=["Reconciliation"])


@router.post("/auto", response_model=AutoReconcileResponse)
def auto_reconcile_transactions(
    request: AutoReconcileRequest,
    db: Session = Depends(get_db)
):
    """
    Auto-reconcile low-risk transactions.
    
    Transactions with risk scores below the specified threshold are automatically
    reconciled. This reduces manual work and enables zero-touch accounting.
    
    - **threshold**: Risk score threshold (0-100). Default is 50.
    - **period**: Optional period to filter transactions (YYYY-MM format)
    """
    result = ReconciliationService.auto_reconcile_transactions(
        db, threshold=request.threshold, period=request.period
    )
    
    return AutoReconcileResponse(
        reconciled_count=result['reconciled_count'],
        total_processed=result['total_processed'],
        period=request.period
    )


@router.get("/status", response_model=ReconciliationStatusResponse)
def get_reconciliation_status(
    period: str = Query(..., pattern=r'^\d{4}-\d{2}$', description="Period in YYYY-MM format"),
    db: Session = Depends(get_db)
):
    """
    Get reconciliation status for a period.
    
    Returns summary of transaction reconciliation progress including:
    - Total transactions
    - Reconciled count
    - Pending count
    - Reconciliation rate
    - Month-end close status
    """
    status = ReconciliationService.get_reconciliation_status(db, period)
    return ReconciliationStatusResponse(**status)


@router.post("/month-end/close", response_model=MonthEndCloseResponse)
def perform_month_end_close(
    request: MonthEndCloseRequest,
    db: Session = Depends(get_db)
):
    """
    Perform autonomous month-end close with zero-touch approach.
    
    This endpoint orchestrates the complete month-end close process:
    1. Auto-reconcile low-risk transactions based on threshold
    2. Post payroll accrual (based on historical data)
    3. Post utilities accrual (based on historical data)
    4. Prepare financial statements
    5. Generate summary for human approval
    
    **Zero-Touch Accounting:** All tasks are automated. Human approval is only
    required for final sign-off, with no manual data entry or calculations needed.
    
    - **period**: Period to close (YYYY-MM format)
    - **auto_reconcile**: Enable automatic reconciliation (default: true)
    - **reconciliation_threshold**: Risk score threshold for auto-reconciliation (default: 50.0)
    - **post_payroll_accrual**: Post payroll accrual (default: true)
    - **post_utilities_accrual**: Post utilities accrual (default: true)
    """
    result = ReconciliationService.perform_month_end_close(
        db=db,
        period=request.period,
        auto_reconcile=request.auto_reconcile,
        reconciliation_threshold=request.reconciliation_threshold,
        post_payroll_accrual=request.post_payroll_accrual,
        post_utilities_accrual=request.post_utilities_accrual
    )
    
    return MonthEndCloseResponse(
        period=result['period'],
        status=result['status'],
        is_month_end_closed=result['is_month_end_closed'],
        workflow_steps=[WorkflowStep(**step) for step in result['workflow_steps']],
        reconciliation_summary=ReconciliationStatusResponse(**result['reconciliation_summary']),
        requires_approval=result['requires_approval'],
        approval_message=result['approval_message']
    )
