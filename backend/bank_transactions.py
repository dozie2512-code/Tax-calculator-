"""
Bank Transaction Parser and Categorization Module
Handles CSV upload, parsing, and automatic categorization of bank transactions
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import re


class BankTransactionParser:
    """Parses bank transaction CSV files and categorizes transactions for tax purposes"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize bank transaction parser
        
        Args:
            data_dir: Directory to store transaction data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.transactions_dir = self.data_dir / "transactions"
        self.transactions_dir.mkdir(exist_ok=True)
        
        # Tax computation categories for UK businesses
        self.categories = {
            "income": ["Sales", "Service Revenue", "Interest Income", "Other Income"],
            "expenses": ["Rent", "Utilities", "Salaries", "Insurance", "Office Supplies",
                        "Professional Fees", "Travel", "Marketing", "Equipment", "Other Expenses"],
            "taxes": ["VAT Payment", "PAYE", "Corporation Tax", "Self Assessment"],
            "capital": ["Equipment Purchase", "Property Purchase", "Loan Payment", "Investment"],
            "uncategorized": ["Uncategorized"]
        }
        
        # Categorization rules based on description keywords
        self.categorization_rules = self._build_categorization_rules()
    
    def _build_categorization_rules(self) -> Dict[str, str]:
        """Build keyword-based categorization rules"""
        return {
            # Income keywords
            r'(payment|deposit|transfer in|credit|invoice|sale)': 'Sales',
            r'(interest|dividend)': 'Interest Income',
            
            # Expense keywords
            r'(rent|lease|landlord)': 'Rent',
            r'(electric|gas|water|utility|utilities)': 'Utilities',
            r'(salary|salaries|wage|payroll|paye)': 'Salaries',
            r'(insurance|policy)': 'Insurance',
            r'(stationery|supplies|office)': 'Office Supplies',
            r'(accountant|lawyer|consultant|professional)': 'Professional Fees',
            r'(travel|hotel|flight|train|taxi|uber)': 'Travel',
            r'(advertising|marketing|promotion)': 'Marketing',
            r'(equipment|computer|software|hardware)': 'Equipment',
            
            # Tax keywords
            r'(vat|value added tax)': 'VAT Payment',
            r'(corporation tax|ct600)': 'Corporation Tax',
            r'(self assessment|sa)': 'Self Assessment',
        }
    
    def parse_csv(self, csv_content: str, business_id: str) -> Dict[str, Any]:
        """
        Parse bank transaction CSV content
        
        Args:
            csv_content: CSV file content as string
            business_id: Business ID to associate transactions with
            
        Returns:
            Dict with parsed transactions and summary
        """
        transactions = []
        errors = []
        
        lines = csv_content.strip().split('\n')
        if len(lines) < 2:
            return {
                "success": False,
                "error": "CSV file must contain headers and at least one transaction"
            }
        
        # Parse CSV
        reader = csv.DictReader(lines)
        
        for idx, row in enumerate(reader, start=2):  # Start from 2 (header is 1)
            try:
                transaction = self._parse_transaction_row(row, business_id)
                transactions.append(transaction)
            except Exception as e:
                errors.append(f"Line {idx}: {str(e)}")
        
        if not transactions:
            return {
                "success": False,
                "error": "No valid transactions found",
                "errors": errors
            }
        
        # Save transactions
        self._save_transactions(business_id, transactions)
        
        # Generate summary
        summary = self._generate_summary(transactions)
        
        return {
            "success": True,
            "transactions_count": len(transactions),
            "transactions": transactions,
            "summary": summary,
            "errors": errors if errors else None
        }
    
    def _parse_transaction_row(self, row: Dict[str, str], business_id: str) -> Dict[str, Any]:
        """Parse a single transaction row"""
        # Expected columns: date, description, amount (or debit/credit)
        date_str = row.get('date', row.get('Date', ''))
        description = row.get('description', row.get('Description', ''))
        
        # Handle amount field (could be single amount or debit/credit columns)
        amount = 0.0
        if 'amount' in row or 'Amount' in row:
            amount = float(row.get('amount', row.get('Amount', '0')).replace(',', ''))
        elif 'debit' in row or 'credit' in row:
            debit = float(row.get('debit', row.get('Debit', '0')).replace(',', '') or '0')
            credit = float(row.get('credit', row.get('Credit', '0')).replace(',', '') or '0')
            amount = credit - debit  # Positive for income, negative for expenses
        
        # Parse date
        parsed_date = self._parse_date(date_str)
        
        # Categorize transaction
        category = self._categorize_transaction(description, amount)
        
        return {
            "date": parsed_date,
            "description": description,
            "amount": amount,
            "category": category,
            "business_id": business_id,
            "reference": row.get('reference', row.get('Reference', '')),
            "imported_at": datetime.now().isoformat()
        }
    
    def _parse_date(self, date_str: str) -> str:
        """Parse date string to ISO format"""
        # Try common date formats
        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%d-%m-%Y',
            '%Y/%m/%d'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")
    
    def _categorize_transaction(self, description: str, amount: float) -> str:
        """
        Automatically categorize transaction based on description and amount
        
        Args:
            description: Transaction description
            amount: Transaction amount (positive = income, negative = expense)
            
        Returns:
            Category name
        """
        desc_lower = description.lower()
        
        # Check against categorization rules
        for pattern, category in self.categorization_rules.items():
            if re.search(pattern, desc_lower):
                return category
        
        # Default categorization based on amount direction
        if amount > 0:
            return 'Sales'  # Default income category
        elif amount < 0:
            return 'Other Expenses'  # Default expense category
        else:
            return 'Uncategorized'
    
    def _save_transactions(self, business_id: str, transactions: List[Dict[str, Any]]):
        """Save transactions to business-specific file"""
        filename = self.transactions_dir / f"{business_id}_transactions.json"
        
        # Load existing transactions
        existing = []
        if filename.exists():
            with open(filename, 'r') as f:
                existing = json.load(f)
        
        # Append new transactions
        existing.extend(transactions)
        
        # Save all transactions
        with open(filename, 'w') as f:
            json.dump(existing, f, indent=2)
    
    def _generate_summary(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for transactions"""
        total_income = sum(t['amount'] for t in transactions if t['amount'] > 0)
        total_expenses = sum(abs(t['amount']) for t in transactions if t['amount'] < 0)
        
        # Category breakdown
        category_totals = {}
        for transaction in transactions:
            category = transaction['category']
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += abs(transaction['amount'])
        
        return {
            "total_transactions": len(transactions),
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "net_amount": round(total_income - total_expenses, 2),
            "categories": category_totals
        }
    
    def get_business_transactions(self, business_id: str, 
                                  start_date: Optional[str] = None,
                                  end_date: Optional[str] = None,
                                  category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get transactions for a business with optional filters
        
        Args:
            business_id: Business ID
            start_date: Start date filter (ISO format)
            end_date: End date filter (ISO format)
            category: Category filter
            
        Returns:
            List of filtered transactions
        """
        filename = self.transactions_dir / f"{business_id}_transactions.json"
        
        if not filename.exists():
            return []
        
        with open(filename, 'r') as f:
            transactions = json.load(f)
        
        # Apply filters
        filtered = transactions
        
        if start_date:
            filtered = [t for t in filtered if t['date'] >= start_date]
        
        if end_date:
            filtered = [t for t in filtered if t['date'] <= end_date]
        
        if category:
            filtered = [t for t in filtered if t['category'] == category]
        
        return filtered
    
    def update_transaction_category(self, business_id: str, transaction_idx: int, 
                                   new_category: str) -> Dict[str, Any]:
        """
        Update the category of a specific transaction
        
        Args:
            business_id: Business ID
            transaction_idx: Index of transaction to update
            new_category: New category name
            
        Returns:
            Dict with success status
        """
        filename = self.transactions_dir / f"{business_id}_transactions.json"
        
        if not filename.exists():
            return {"success": False, "error": "No transactions found for business"}
        
        with open(filename, 'r') as f:
            transactions = json.load(f)
        
        if transaction_idx < 0 or transaction_idx >= len(transactions):
            return {"success": False, "error": "Invalid transaction index"}
        
        transactions[transaction_idx]['category'] = new_category
        transactions[transaction_idx]['updated_at'] = datetime.now().isoformat()
        
        with open(filename, 'w') as f:
            json.dump(transactions, f, indent=2)
        
        return {"success": True, "transaction": transactions[transaction_idx]}


# Demo function for testing
if __name__ == "__main__":
    parser = BankTransactionParser()
    
    # Sample CSV content
    sample_csv = """date,description,amount
2024-01-15,Customer payment - ABC Corp,15000.00
2024-01-16,Rent payment to landlord,-3000.00
2024-01-17,Office supplies - Staples,-250.50
2024-01-18,Electricity bill payment,-180.00
2024-01-20,Professional fees - Accountant,-500.00
2024-01-22,Customer deposit - XYZ Ltd,8500.00
2024-01-25,Marketing - Google Ads,-1200.00"""
    
    print("Parsing sample bank transactions...")
    result = parser.parse_csv(sample_csv, "business-123")
    
    if result["success"]:
        print(f"\nSuccessfully parsed {result['transactions_count']} transactions")
        print("\nSummary:")
        print(f"  Total Income: £{result['summary']['total_income']:,.2f}")
        print(f"  Total Expenses: £{result['summary']['total_expenses']:,.2f}")
        print(f"  Net Amount: £{result['summary']['net_amount']:,.2f}")
        
        print("\nCategory Breakdown:")
        for category, amount in result['summary']['categories'].items():
            print(f"  {category}: £{amount:,.2f}")
        
        print("\nTransactions:")
        for tx in result['transactions']:
            print(f"  {tx['date']} | {tx['description'][:40]:40} | £{tx['amount']:10,.2f} | {tx['category']}")
    else:
        print(f"Error: {result['error']}")
