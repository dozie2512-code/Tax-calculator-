"""Pydantic schemas for request and response validation."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Transaction Schemas
class TransactionBase(BaseModel):
    """Base transaction schema."""
    description: str = Field(..., description="Transaction description")
    amount: float = Field(..., gt=0, description="Transaction amount")
    category: str = Field(..., description="Transaction category")
    vendor: Optional[str] = Field(None, description="Vendor name")
    date: Optional[datetime] = Field(None, description="Transaction date")


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    risk_score: float
    is_reconciled: bool
    reconciled_at: Optional[datetime]
    date: datetime
    
    class Config:
        from_attributes = True


class TransactionImportRequest(BaseModel):
    """Schema for bulk transaction import."""
    transactions: List[TransactionCreate]


class TransactionImportResponse(BaseModel):
    """Schema for transaction import response."""
    imported_count: int
    transactions: List[TransactionResponse]


# Accrual Schemas
class AccrualBase(BaseModel):
    """Base accrual schema."""
    period: str = Field(..., pattern=r'^\d{4}-\d{2}$', description="Period in YYYY-MM format")
    accrual_type: str = Field(..., description="Accrual type (payroll/utilities)")
    description: str
    amount: float = Field(..., gt=0)


class AccrualResponse(AccrualBase):
    """Schema for accrual response."""
    id: int
    is_posted: bool
    posted_at: Optional[datetime]
    based_on_historical: bool
    historical_average: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AccrualPostResponse(BaseModel):
    """Schema for accrual posting response."""
    message: str
    accrual: AccrualResponse


# Reconciliation Schemas
class AutoReconcileRequest(BaseModel):
    """Schema for auto-reconciliation request."""
    threshold: float = Field(default=50.0, ge=0, le=100, description="Risk score threshold")
    period: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$', description="Period in YYYY-MM format")


class AutoReconcileResponse(BaseModel):
    """Schema for auto-reconciliation response."""
    reconciled_count: int
    total_processed: int
    period: Optional[str]


class ReconciliationStatusResponse(BaseModel):
    """Schema for reconciliation status response."""
    period: str
    status: str
    total_transactions: int
    reconciled_count: int
    pending_count: int
    reconciliation_rate: float
    is_month_end_closed: bool


class MonthEndCloseRequest(BaseModel):
    """Schema for month-end close request."""
    period: str = Field(..., pattern=r'^\d{4}-\d{2}$', description="Period in YYYY-MM format")
    auto_reconcile: bool = Field(default=True, description="Enable auto-reconciliation")
    reconciliation_threshold: float = Field(default=50.0, ge=0, le=100, description="Risk score threshold")
    post_payroll_accrual: bool = Field(default=True, description="Post payroll accrual")
    post_utilities_accrual: bool = Field(default=True, description="Post utilities accrual")


class WorkflowStep(BaseModel):
    """Schema for workflow step."""
    step: str
    status: str
    message: str
    timestamp: datetime


class MonthEndCloseResponse(BaseModel):
    """Schema for month-end close response."""
    period: str
    status: str
    is_month_end_closed: bool
    workflow_steps: List[WorkflowStep]
    reconciliation_summary: ReconciliationStatusResponse
    requires_approval: bool
    approval_message: str
