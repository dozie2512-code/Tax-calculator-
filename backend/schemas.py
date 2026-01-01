"""Pydantic schemas for API request/response models."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TransactionBase(BaseModel):
    """Base transaction schema."""
    description: str = Field(..., description="Transaction description")
    amount: float = Field(..., description="Transaction amount")
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
    created_at: datetime
    date: datetime
    
    class Config:
        from_attributes = True


class TransactionImportRequest(BaseModel):
    """Schema for importing multiple transactions."""
    transactions: List[TransactionCreate]


class TransactionImportResponse(BaseModel):
    """Schema for import response."""
    imported_count: int
    transactions: List[TransactionResponse]


class AccrualBase(BaseModel):
    """Base accrual schema."""
    period: str = Field(..., description="Accrual period (YYYY-MM)")
    accrual_type: str = Field(..., description="Accrual type (payroll/utilities)")
    description: str = Field(..., description="Accrual description")
    amount: float = Field(..., description="Accrual amount")


class AccrualCreate(AccrualBase):
    """Schema for creating an accrual."""
    pass


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


class ReconciliationRequest(BaseModel):
    """Schema for reconciliation request."""
    threshold: float = Field(default=1000.0, description="Risk threshold for auto-reconciliation")
    period: Optional[str] = Field(None, description="Period to reconcile (YYYY-MM)")


class ReconciliationResponse(BaseModel):
    """Schema for reconciliation response."""
    period: str
    reconciled_count: int
    total_transactions: int
    pending_count: int


class MonthEndCloseRequest(BaseModel):
    """Schema for month-end close request."""
    period: str = Field(..., description="Period to close (YYYY-MM)")
    auto_reconcile: bool = Field(default=True, description="Auto-reconcile low-risk transactions")
    reconciliation_threshold: float = Field(default=1000.0, description="Threshold for auto-reconciliation")
    post_payroll_accrual: bool = Field(default=True, description="Post payroll accruals")
    post_utilities_accrual: bool = Field(default=True, description="Post utilities accruals")


class MonthEndCloseResponse(BaseModel):
    """Schema for month-end close response."""
    period: str
    status: str
    reconciled_transactions: int
    posted_accruals: int
    pending_approval: bool
    message: str


class ReconciliationStatusResponse(BaseModel):
    """Schema for reconciliation status."""
    period: str
    status: str
    total_transactions: int
    reconciled_count: int
    pending_count: int
    is_month_end_closed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
