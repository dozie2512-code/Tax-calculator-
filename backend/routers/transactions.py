"""Transaction API endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import get_db
from ..schemas import (
    TransactionImport,
    TransactionImportResponse,
    TransactionResponse
)
from ..services import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/import", response_model=TransactionImportResponse)
def import_transactions(
    import_data: TransactionImport,
    db: Session = Depends(get_db)
):
    """
    Import multiple transactions with automatic risk scoring.
    
    Each transaction will be assigned a risk score based on:
    - Transaction amount
    - Category
    - Vendor information
    """
    # Convert to dict list
    transactions_data = [txn.model_dump() for txn in import_data.transactions]
    
    # Import transactions
    imported = TransactionService.import_transactions(db, transactions_data)
    
    return {
        "imported_count": len(imported),
        "transactions": imported
    }


@router.get("", response_model=List[TransactionResponse])
def list_transactions(
    period: Optional[str] = None,
    is_reconciled: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List transactions with optional filtering.
    
    - **period**: Filter by period (YYYY-MM format)
    - **is_reconciled**: Filter by reconciliation status
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    transactions = TransactionService.get_transactions(
        db, period=period, is_reconciled=is_reconciled, skip=skip, limit=limit
    )
    return transactions
