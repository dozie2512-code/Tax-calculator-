"""Accrual API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.models import get_db
from backend.schemas import AccrualResponse, AccrualPostResponse
from backend.services import AccrualService

router = APIRouter(prefix="/accruals", tags=["Accruals"])


@router.post("/payroll", response_model=AccrualPostResponse)
def post_payroll_accrual(
    period: str = Query(..., pattern=r'^\d{4}-\d{2}$', description="Period in YYYY-MM format"),
    db: Session = Depends(get_db)
):
    """
    Post payroll accrual for a period.
    
    The amount is calculated based on historical payroll transactions.
    If no historical data is available, a default amount is used.
    """
    accrual = AccrualService.post_payroll_accrual(db, period)
    
    message = "Payroll accrual posted successfully"
    if accrual.based_on_historical:
        message += f" based on historical average of ${accrual.historical_average:,.2f}"
    else:
        message += " using default amount (no historical data available)"
    
    return AccrualPostResponse(
        message=message,
        accrual=AccrualResponse.model_validate(accrual)
    )


@router.post("/utilities", response_model=AccrualPostResponse)
def post_utilities_accrual(
    period: str = Query(..., pattern=r'^\d{4}-\d{2}$', description="Period in YYYY-MM format"),
    db: Session = Depends(get_db)
):
    """
    Post utilities accrual for a period.
    
    The amount is calculated based on historical utilities transactions.
    If no historical data is available, a default amount is used.
    """
    accrual = AccrualService.post_utilities_accrual(db, period)
    
    message = "Utilities accrual posted successfully"
    if accrual.based_on_historical:
        message += f" based on historical average of ${accrual.historical_average:,.2f}"
    else:
        message += " using default amount (no historical data available)"
    
    return AccrualPostResponse(
        message=message,
        accrual=AccrualResponse.model_validate(accrual)
    )


@router.get("", response_model=List[AccrualResponse])
def list_accruals(
    skip: int = 0,
    limit: int = 100,
    period: Optional[str] = Query(None, pattern=r'^\d{4}-\d{2}$'),
    accrual_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List accruals with optional filtering.
    
    - **period**: Filter by period (YYYY-MM format)
    - **accrual_type**: Filter by type (payroll/utilities)
    """
    accruals = AccrualService.get_accruals(
        db, skip=skip, limit=limit, period=period, accrual_type=accrual_type
    )
    return [AccrualResponse.model_validate(accrual) for accrual in accruals]
