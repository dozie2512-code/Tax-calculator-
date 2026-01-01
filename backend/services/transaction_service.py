"""Transaction service with business logic."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional
from ..models.transaction import Transaction
from ..schemas import TransactionCreate


class TransactionService:
    """Service for managing transactions."""
    
    @staticmethod
    def calculate_risk_score(transaction: TransactionCreate) -> float:
        """
        Calculate risk score for a transaction.
        
        Risk factors:
        - Amount: Higher amounts = higher risk
        - Category: Certain categories are riskier
        - Vendor: Unknown vendors = higher risk
        
        Returns risk score between 0 and 100.
        """
        risk_score = 0.0
        
        # Amount-based risk (logarithmic scale)
        if transaction.amount > 10000:
            risk_score += 50
        elif transaction.amount > 5000:
            risk_score += 30
        elif transaction.amount > 1000:
            risk_score += 15
        else:
            risk_score += 5
        
        # Category-based risk
        high_risk_categories = ["consulting", "legal", "miscellaneous", "other"]
        low_risk_categories = ["utilities", "payroll", "rent", "insurance"]
        
        category_lower = transaction.category.lower()
        if any(cat in category_lower for cat in high_risk_categories):
            risk_score += 25
        elif any(cat in category_lower for cat in low_risk_categories):
            risk_score += 5
        else:
            risk_score += 15
        
        # Vendor-based risk
        if not transaction.vendor or transaction.vendor.strip() == "":
            risk_score += 15
        
        return min(risk_score, 100.0)
    
    @staticmethod
    def import_transactions(db: Session, transactions: List[TransactionCreate]) -> List[Transaction]:
        """Import multiple transactions into the database."""
        db_transactions = []
        
        for trans_data in transactions:
            # Calculate risk score
            risk_score = TransactionService.calculate_risk_score(trans_data)
            
            # Create transaction
            db_transaction = Transaction(
                description=trans_data.description,
                amount=trans_data.amount,
                category=trans_data.category,
                vendor=trans_data.vendor,
                date=trans_data.date or datetime.utcnow(),
                risk_score=risk_score,
                is_reconciled=False
            )
            db.add(db_transaction)
            db_transactions.append(db_transaction)
        
        db.commit()
        for trans in db_transactions:
            db.refresh(trans)
        
        return db_transactions
    
    @staticmethod
    def get_transactions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_reconciled: Optional[bool] = None
    ) -> List[Transaction]:
        """Get transactions with optional filtering."""
        query = db.query(Transaction)
        
        if is_reconciled is not None:
            query = query.filter(Transaction.is_reconciled == is_reconciled)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def auto_reconcile_low_risk(db: Session, threshold: float, period: Optional[str] = None) -> int:
        """
        Auto-reconcile transactions with risk score below threshold.
        
        Args:
            db: Database session
            threshold: Maximum risk score for auto-reconciliation
            period: Optional period filter (YYYY-MM)
        
        Returns:
            Number of transactions reconciled
        """
        query = db.query(Transaction).filter(
            Transaction.is_reconciled == False,
            Transaction.risk_score <= threshold
        )
        
        if period:
            # Filter by period (YYYY-MM)
            year, month = period.split("-")
            query = query.filter(
                func.strftime("%Y-%m", Transaction.date) == period
            )
        
        transactions = query.all()
        
        for transaction in transactions:
            transaction.is_reconciled = True
            transaction.reconciled_at = datetime.utcnow()
        
        db.commit()
        
        return len(transactions)
