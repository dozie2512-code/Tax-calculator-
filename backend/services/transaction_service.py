"""Transaction service with business logic."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Transaction


def calculate_risk_score(amount: float, category: str, vendor: Optional[str]) -> float:
    """
    Calculate risk score for a transaction (0-100).
    
    Risk factors:
    - Amount-based risk
    - Category-based risk
    - Vendor-based risk
    """
    risk_score = 0.0
    
    # Amount-based risk
    if amount > 10000:
        risk_score += 50
    elif amount > 5000:
        risk_score += 30
    elif amount > 1000:
        risk_score += 15
    else:
        risk_score += 5
    
    # Category-based risk
    high_risk_categories = ["consulting", "legal", "miscellaneous"]
    low_risk_categories = ["utilities", "payroll", "rent", "insurance"]
    
    if category.lower() in high_risk_categories:
        risk_score += 25
    elif category.lower() in low_risk_categories:
        risk_score += 5
    else:
        risk_score += 15
    
    # Vendor-based risk
    if not vendor or vendor.strip() == "":
        risk_score += 15
    
    return min(risk_score, 100.0)


class TransactionService:
    """Service for transaction operations."""
    
    @staticmethod
    def import_transactions(db: Session, transactions: List[dict]) -> List[Transaction]:
        """Import multiple transactions with automatic risk scoring."""
        imported = []
        
        for txn_data in transactions:
            # Calculate risk score
            risk_score = calculate_risk_score(
                amount=txn_data["amount"],
                category=txn_data["category"],
                vendor=txn_data.get("vendor")
            )
            
            # Create transaction
            transaction = Transaction(
                date=txn_data.get("date", datetime.utcnow()),
                description=txn_data["description"],
                amount=txn_data["amount"],
                category=txn_data["category"],
                vendor=txn_data.get("vendor"),
                risk_score=risk_score,
                is_reconciled=False
            )
            
            db.add(transaction)
            imported.append(transaction)
        
        db.commit()
        
        # Refresh all transactions
        for txn in imported:
            db.refresh(txn)
        
        return imported
    
    @staticmethod
    def get_transactions(
        db: Session,
        period: Optional[str] = None,
        is_reconciled: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions with optional filtering."""
        query = db.query(Transaction)
        
        if period:
            # Filter by period (YYYY-MM)
            year, month = period.split("-")
            query = query.filter(
                Transaction.date >= datetime(int(year), int(month), 1)
            )
            # Simple month filter (doesn't handle end of month perfectly)
            if int(month) < 12:
                query = query.filter(
                    Transaction.date < datetime(int(year), int(month) + 1, 1)
                )
            else:
                query = query.filter(
                    Transaction.date < datetime(int(year) + 1, 1, 1)
                )
        
        if is_reconciled is not None:
            query = query.filter(Transaction.is_reconciled == is_reconciled)
        
        return query.offset(skip).limit(limit).all()
