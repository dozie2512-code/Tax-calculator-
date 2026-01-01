"""Transaction API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.models import get_db
from backend.schemas import (
    TransactionImportRequest,
    TransactionImportResponse,
    TransactionResponse
)
from backend.services import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/import", response_model=TransactionImportResponse)
def import_transactions(
    request: TransactionImportRequest,
    db: Session = Depends(get_db)
):
    """
    Import multiple transactions with automatic risk scoring.
    
    Risk scores are automatically calculated based on:
    - Transaction amount
    - Category
    - Vendor information
    """
    transactions_data = [txn.model_dump() for txn in request.transactions]
    imported = TransactionService.import_transactions(db, transactions_data)
    
    return TransactionImportResponse(
        imported_count=len(imported),
        transactions=[TransactionResponse.model_validate(txn) for txn in imported]
    )


@router.get("", response_model=List[TransactionResponse])
def list_transactions(
    skip: int = 0,
    limit: int = 100,
    period: Optional[str] = None,
    is_reconciled: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    List transactions with optional filtering.
    
    - **period**: Filter by period (YYYY-MM format)
    - **is_reconciled**: Filter by reconciliation status
    """
    transactions = TransactionService.get_transactions(
        db, skip=skip, limit=limit, period=period, is_reconciled=is_reconciled
    )
    return [TransactionResponse.model_validate(txn) for txn in transactions]
