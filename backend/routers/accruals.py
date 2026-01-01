"""Accrual router with API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import get_db
from ..schemas import AccrualResponse
from ..services.accrual_service import AccrualService

router = APIRouter(prefix="/accruals", tags=["accruals"])


@router.post("/payroll", response_model=AccrualResponse)
def post_payroll_accrual(
    period: str = Query(..., description="Period for accrual (YYYY-MM)", regex=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db)
):
    """
    Post payroll accrual based on historical data.
    
    This endpoint automatically calculates and posts a payroll accrual
    based on the average of previous months' payroll transactions.
    
    - **period**: Period in YYYY-MM format (e.g., "2026-01")
    """
    accrual = AccrualService.post_payroll_accrual(db, period)
    return accrual


@router.post("/utilities", response_model=AccrualResponse)
def post_utilities_accrual(
    period: str = Query(..., description="Period for accrual (YYYY-MM)", regex=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db)
):
    """
    Post utilities accrual based on historical data.
    
    This endpoint automatically calculates and posts a utilities accrual
    based on the average of previous months' utilities transactions.
    
    - **period**: Period in YYYY-MM format (e.g., "2026-01")
    """
    accrual = AccrualService.post_utilities_accrual(db, period)
    return accrual


@router.get("/", response_model=List[AccrualResponse])
def list_accruals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    period: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}$"),
    accrual_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    List accruals with optional filtering.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **period**: Filter by period (YYYY-MM format)
    - **accrual_type**: Filter by accrual type (payroll/utilities)
    """
    accruals = AccrualService.get_accruals(
        db, skip=skip, limit=limit, period=period, accrual_type=accrual_type
    )
    return accruals
