"""Transaction service with risk scoring logic."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import Transaction


class TransactionService:
    """Service for managing transactions with automatic risk scoring."""
    
    @staticmethod
    def calculate_risk_score(amount: float, category: str, vendor: Optional[str]) -> float:
        """
        Calculate risk score based on amount, category, and vendor.
        Score ranges from 0-100, with higher scores indicating higher risk.
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
        high_risk_categories = ['consulting', 'legal', 'miscellaneous']
        low_risk_categories = ['utilities', 'payroll', 'rent', 'insurance']
        
        category_lower = category.lower()
        if category_lower in high_risk_categories:
            risk_score += 25
        elif category_lower in low_risk_categories:
            risk_score += 5
        else:
            risk_score += 15
        
        # Vendor-based risk
        if not vendor or vendor.strip() == "":
            risk_score += 15
        
        return min(risk_score, 100.0)
    
    @staticmethod
    def import_transactions(db: Session, transactions_data: List[dict]) -> List[Transaction]:
        """
        Import multiple transactions with automatic risk scoring.
        """
        imported_transactions = []
        
        for txn_data in transactions_data:
            # Calculate risk score
            risk_score = TransactionService.calculate_risk_score(
                amount=txn_data['amount'],
                category=txn_data['category'],
                vendor=txn_data.get('vendor')
            )
            
            # Create transaction
            transaction = Transaction(
                description=txn_data['description'],
                amount=txn_data['amount'],
                category=txn_data['category'],
                vendor=txn_data.get('vendor'),
                date=txn_data.get('date', datetime.utcnow()),
                risk_score=risk_score,
                is_reconciled=False
            )
            
            db.add(transaction)
            imported_transactions.append(transaction)
        
        db.commit()
        
        # Refresh to get IDs
        for txn in imported_transactions:
            db.refresh(txn)
        
        return imported_transactions
    
    @staticmethod
    def get_transactions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        period: Optional[str] = None,
        is_reconciled: Optional[bool] = None
    ) -> List[Transaction]:
        """
        Get transactions with optional filtering.
        """
        query = db.query(Transaction)
        
        # Filter by period if provided
        if period:
            query = query.filter(
                func.strftime('%Y-%m', Transaction.date) == period
            )
        
        # Filter by reconciliation status if provided
        if is_reconciled is not None:
            query = query.filter(Transaction.is_reconciled == is_reconciled)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()
