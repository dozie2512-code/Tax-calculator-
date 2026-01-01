"""Reconciliation API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models import get_db
from ..schemas import (
    AutoReconcileRequest,
    AutoReconcileResponse,
    ReconciliationStatusResponse,
    MonthEndCloseRequest,
    MonthEndCloseResponse
)
from ..services import ReconciliationService

router = APIRouter(prefix="/reconciliation", tags=["reconciliation"])


@router.post("/auto", response_model=AutoReconcileResponse)
def auto_reconcile(
    request: AutoReconcileRequest,
    db: Session = Depends(get_db)
):
    """
    Auto-reconcile low-risk transactions.
    
    Transactions with risk score <= threshold will be automatically reconciled.
    
    - **threshold**: Maximum risk score for auto-reconciliation (0-100)
    - **period**: Optional period filter (YYYY-MM format)
    """
    try:
        result = ReconciliationService.auto_reconcile(
            db, request.threshold, request.period
        )
        return result
    except HTTPException:
        # Re-raise HTTPException from validation
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during auto-reconciliation: {str(e)}")


@router.get("/status", response_model=ReconciliationStatusResponse)
def get_reconciliation_status(
    period: str,
    db: Session = Depends(get_db)
):
    """
    Get reconciliation status for a period.
    
    Returns the current reconciliation status including:
    - Total transactions
    - Reconciled count
    - Pending count
    - Month-end close status
    
    - **period**: Period in YYYY-MM format (e.g., "2026-01")
    """
    try:
        status = ReconciliationService.get_reconciliation_status(db, period)
        return status
    except HTTPException:
        # Re-raise HTTPException from validation
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting reconciliation status: {str(e)}")


@router.post("/month-end/close", response_model=MonthEndCloseResponse)
def month_end_close(
    request: MonthEndCloseRequest,
    db: Session = Depends(get_db)
):
    """
    Perform autonomous month-end close process.
    
    This endpoint orchestrates the complete month-end close workflow:
    1. Auto-reconcile low-risk transactions (if enabled)
    2. Post payroll accrual (if enabled)
    3. Post utilities accrual (if enabled)
    4. Mark period as closed
    
    - **period**: Period in YYYY-MM format
    - **auto_reconcile**: Enable auto-reconciliation
    - **reconciliation_threshold**: Risk score threshold for auto-reconciliation
    - **post_payroll_accrual**: Post payroll accrual
    - **post_utilities_accrual**: Post utilities accrual
    """
    try:
        result = ReconciliationService.month_end_close(
            db,
            period=request.period,
            auto_reconcile=request.auto_reconcile,
            reconciliation_threshold=request.reconciliation_threshold,
            post_payroll_accrual=request.post_payroll_accrual,
            post_utilities_accrual=request.post_utilities_accrual
        )
        return result
    except HTTPException:
        # Re-raise HTTPException from validation
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during month-end close: {str(e)}")
