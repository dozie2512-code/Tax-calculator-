"""Pydantic schemas for request and response validation."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Transaction Schemas
class TransactionBase(BaseModel):
    """Base transaction schema."""
    description: str
    amount: float
    category: str
    vendor: Optional[str] = None
    date: Optional[datetime] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionImport(BaseModel):
    """Schema for importing multiple transactions."""
    transactions: List[TransactionCreate]


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    risk_score: float
    is_reconciled: bool
    reconciled_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TransactionImportResponse(BaseModel):
    """Schema for import response."""
    imported_count: int
    transactions: List[TransactionResponse]


# Accrual Schemas
class AccrualResponse(BaseModel):
    """Schema for accrual response."""
    id: int
    period: str
    accrual_type: str
    description: str
    amount: float
    is_posted: bool
    based_on_historical: bool
    historical_average: Optional[float] = None

    class Config:
        from_attributes = True


# Reconciliation Schemas
class AutoReconcileRequest(BaseModel):
    """Schema for auto-reconcile request."""
    threshold: float = Field(default=50.0, ge=0, le=100)
    period: Optional[str] = None


class AutoReconcileResponse(BaseModel):
    """Schema for auto-reconcile response."""
    reconciled_count: int
    total_transactions: int
    threshold_used: float


class ReconciliationStatusResponse(BaseModel):
    """Schema for reconciliation status response."""
    period: str
    status: str
    total_transactions: int
    reconciled_count: int
    pending_count: int
    is_month_end_closed: bool
    reconciliation_percentage: float


class MonthEndCloseRequest(BaseModel):
    """Schema for month-end close request."""
    period: str
    auto_reconcile: bool = True
    reconciliation_threshold: float = Field(default=50.0, ge=0, le=100)
    post_payroll_accrual: bool = True
    post_utilities_accrual: bool = True


class MonthEndCloseResponse(BaseModel):
    """Schema for month-end close response."""
    period: str
    status: str
    reconciled_count: int
    accruals_posted: List[str]
    is_closed: bool
    message: str
