"""Transaction router with API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import get_db
from ..schemas import (
    TransactionCreate,
    TransactionResponse,
    TransactionImportRequest,
    TransactionImportResponse
)
from ..services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/import", response_model=TransactionImportResponse)
def import_transactions(
    request: TransactionImportRequest,
    db: Session = Depends(get_db)
):
    """
    Import multiple transactions into the system.
    
    This endpoint allows bulk import of transactions with automatic risk scoring.
    """
    transactions = TransactionService.import_transactions(db, request.transactions)
    
    return {
        "imported_count": len(transactions),
        "transactions": transactions
    }


@router.get("/", response_model=List[TransactionResponse])
def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_reconciled: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """
    List transactions with optional filtering.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **is_reconciled**: Filter by reconciliation status (optional)
    """
    transactions = TransactionService.get_transactions(
        db, skip=skip, limit=limit, is_reconciled=is_reconciled
    )
    return transactions
