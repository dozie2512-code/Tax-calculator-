"""Accrual API endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models import get_db
from ..schemas import AccrualResponse
from ..services import AccrualService

router = APIRouter(prefix="/accruals", tags=["accruals"])


@router.post("/payroll", response_model=AccrualResponse)
def post_payroll_accrual(
    period: str,
    db: Session = Depends(get_db)
):
    """
    Post payroll accrual for a period.
    
    The accrual amount is calculated based on historical payroll transactions
    (average of previous periods).
    
    - **period**: Period in YYYY-MM format (e.g., "2026-01")
    """
    try:
        accrual = AccrualService.post_payroll_accrual(db, period)
        return accrual
    except HTTPException:
        # Re-raise HTTPException from validation
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting payroll accrual: {str(e)}")


@router.post("/utilities", response_model=AccrualResponse)
def post_utilities_accrual(
    period: str,
    db: Session = Depends(get_db)
):
    """
    Post utilities accrual for a period.
    
    The accrual amount is calculated based on historical utilities transactions
    (average of previous periods).
    
    - **period**: Period in YYYY-MM format (e.g., "2026-01")
    """
    try:
        accrual = AccrualService.post_utilities_accrual(db, period)
        return accrual
    except HTTPException:
        # Re-raise HTTPException from validation
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting utilities accrual: {str(e)}")


@router.get("", response_model=List[AccrualResponse])
def list_accruals(
    period: Optional[str] = None,
    accrual_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List accruals with optional filtering.
    
    - **period**: Filter by period (YYYY-MM format)
    - **accrual_type**: Filter by type (payroll, utilities)
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        accruals = AccrualService.get_accruals(
            db, period=period, accrual_type=accrual_type, skip=skip, limit=limit
        )
        return accruals
    except HTTPException:
        # Re-raise HTTPException from validation
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing accruals: {str(e)}")
