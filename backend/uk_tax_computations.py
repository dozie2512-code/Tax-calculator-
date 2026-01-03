"""
UK Tax Computations Module for Autonomous Month-End Close Process
Handles multi-user and multi-business tax computations with CSV import support
"""

import json
from typing import List, Dict, Any, Optional
from utils import read_csv_file, write_csv_file, safe_float, format_currency
import csv
from datetime import datetime


class UKTaxComputations:
    """
    Performs UK tax computations for multiple users and businesses.
    Supports importing bank transaction data from CSV files.
    """
    
    def __init__(self):
        """Initialize the UK Tax Computations handler."""
        self.users = {}  # user_id -> user_data
        self.businesses = {}  # business_id -> business_data
        self.transactions = []  # All imported transactions
        self.user_business_transactions = {}  # (user_id, business_id) -> transactions
        self.computations = {}  # (user_id, business_id) -> computation results
        
    def add_user(self, user_id: str, user_name: str, user_data: Optional[Dict] = None):
        """
        Add a user to the system.
        
        Args:
            user_id: Unique identifier for the user
            user_name: Display name for the user
            user_data: Additional user data
        """
        self.users[user_id] = {
            'id': user_id,
            'name': user_name,
            'data': user_data or {}
        }
        
    def add_business(self, business_id: str, business_name: str, business_data: Optional[Dict] = None):
        """
        Add a business to the system.
        
        Args:
            business_id: Unique identifier for the business
            business_name: Display name for the business
            business_data: Additional business data
        """
        self.businesses[business_id] = {
            'id': business_id,
            'name': business_name,
            'data': business_data or {}
        }
        
    def validate_csv_data(self, csv_content: str) -> Dict[str, Any]:
        """
        Validate CSV data format and content.
        
        Args:
            csv_content: CSV content as string
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        is_valid = True
        row_count = 0
        
        try:
            lines = csv_content.strip().split('\n')
            if len(lines) < 2:
                errors.append("CSV must contain at least a header row and one data row")
                return {'valid': False, 'errors': errors, 'warnings': warnings, 'row_count': 0}
            
            # Parse CSV
            reader = csv.DictReader(lines)
            headers = reader.fieldnames
            
            # Required fields for bank transactions
            required_fields = ['date', 'description', 'amount']
            missing_fields = [field for field in required_fields if field not in headers]
            
            if missing_fields:
                errors.append(f"Missing required fields: {', '.join(missing_fields)}")
                is_valid = False
            
            # Validate each row
            for idx, row in enumerate(reader, start=2):
                row_count += 1
                
                # Validate date
                if 'date' in row:
                    try:
                        datetime.strptime(row['date'], '%Y-%m-%d')
                    except ValueError:
                        try:
                            datetime.strptime(row['date'], '%d/%m/%Y')
                        except ValueError:
                            warnings.append(f"Row {idx}: Date format may be invalid: {row['date']}")
                
                # Validate amount
                if 'amount' in row:
                    try:
                        float(row['amount'])
                    except ValueError:
                        errors.append(f"Row {idx}: Invalid amount value: {row['amount']}")
                        is_valid = False
                
                # Check for empty required fields
                for field in required_fields:
                    if field in row and not row[field].strip():
                        errors.append(f"Row {idx}: {field} is empty")
                        is_valid = False
                        
        except Exception as e:
            errors.append(f"CSV parsing error: {str(e)}")
            is_valid = False
        
        return {
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'row_count': row_count
        }
    
    def import_transactions_from_csv(self, csv_content: str, user_id: str, business_id: str) -> Dict[str, Any]:
        """
        Import bank transaction data from CSV content.
        
        Args:
            csv_content: CSV content as string
            user_id: User ID to associate transactions with
            business_id: Business ID to associate transactions with
            
        Returns:
            Dictionary with import results
        """
        # Validate CSV first
        validation_result = self.validate_csv_data(csv_content)
        if not validation_result['valid']:
            return {
                'success': False,
                'message': 'CSV validation failed',
                'validation': validation_result
            }
        
        # Parse and import transactions
        imported_count = 0
        transactions = []
        
        try:
            lines = csv_content.strip().split('\n')
            reader = csv.DictReader(lines)
            
            for row in reader:
                transaction = {
                    'user_id': user_id,
                    'business_id': business_id,
                    'date': row.get('date', ''),
                    'description': row.get('description', ''),
                    'amount': safe_float(row.get('amount', 0)),
                    'reference': row.get('reference', ''),
                    'category': row.get('category', ''),
                    'imported_at': datetime.now().isoformat()
                }
                transactions.append(transaction)
                self.transactions.append(transaction)
                imported_count += 1
            
            # Store transactions by user-business combination
            key = (user_id, business_id)
            if key not in self.user_business_transactions:
                self.user_business_transactions[key] = []
            self.user_business_transactions[key].extend(transactions)
            
            return {
                'success': True,
                'message': f'Successfully imported {imported_count} transactions',
                'imported_count': imported_count,
                'transactions': transactions,
                'validation': validation_result
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Import error: {str(e)}',
                'validation': validation_result
            }
    
    def get_transactions(self, user_id: Optional[str] = None, business_id: Optional[str] = None) -> List[Dict]:
        """
        Get transactions filtered by user and/or business.
        
        Args:
            user_id: Optional user ID filter
            business_id: Optional business ID filter
            
        Returns:
            List of transactions
        """
        if user_id is None and business_id is None:
            return self.transactions
        
        filtered = []
        for tx in self.transactions:
            if user_id and tx.get('user_id') != user_id:
                continue
            if business_id and tx.get('business_id') != business_id:
                continue
            filtered.append(tx)
        
        return filtered
    
    def compute_tax_from_transactions(self, user_id: str, business_id: str) -> Dict[str, Any]:
        """
        Compute taxes based on imported transactions for a specific user and business.
        
        Args:
            user_id: User ID
            business_id: Business ID
            
        Returns:
            Dictionary with tax computation results
        """
        key = (user_id, business_id)
        transactions = self.user_business_transactions.get(key, [])
        
        if not transactions:
            return {
                'success': False,
                'message': 'No transactions found for this user and business',
                'user_id': user_id,
                'business_id': business_id
            }
        
        # Calculate totals from transactions
        total_income = sum(tx['amount'] for tx in transactions if tx['amount'] > 0)
        total_expenses = abs(sum(tx['amount'] for tx in transactions if tx['amount'] < 0))
        net_profit = total_income - total_expenses
        
        # Categorize transactions
        income_transactions = [tx for tx in transactions if tx['amount'] > 0]
        expense_transactions = [tx for tx in transactions if tx['amount'] < 0]
        
        # Simple Corporation Tax calculation (UK rates 2024/25)
        taxable_profit = net_profit
        corporation_tax = 0
        tax_rate = 0
        
        if taxable_profit > 0:
            if taxable_profit <= 50000:
                tax_rate = 0.19  # Small profits rate
                corporation_tax = taxable_profit * tax_rate
            elif taxable_profit >= 250000:
                tax_rate = 0.25  # Main rate
                corporation_tax = taxable_profit * tax_rate
            else:
                # Marginal relief applies
                tax_rate = 0.25
                marginal_relief = (250000 - taxable_profit) * 0.015
                corporation_tax = (taxable_profit * tax_rate) - marginal_relief
        
        # VAT calculation (assuming standard rate on sales)
        vat_on_sales = total_income * 0.20
        vat_on_purchases = total_expenses * 0.20
        vat_due = vat_on_sales - vat_on_purchases
        
        result = {
            'success': True,
            'user_id': user_id,
            'business_id': business_id,
            'transaction_count': len(transactions),
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'taxable_profit': taxable_profit,
            'corporation_tax': corporation_tax,
            'tax_rate': tax_rate,
            'vat_on_sales': vat_on_sales,
            'vat_on_purchases': vat_on_purchases,
            'vat_due': vat_due,
            'income_transactions': income_transactions,
            'expense_transactions': expense_transactions,
            'computation_date': datetime.now().isoformat()
        }
        
        # Store computation
        self.computations[key] = result
        
        return result
    
    def export_computation_results(self, user_id: str, business_id: str, output_file: str):
        """
        Export computation results to a JSON file.
        
        Args:
            user_id: User ID
            business_id: Business ID
            output_file: Output file path
        """
        key = (user_id, business_id)
        if key not in self.computations:
            print(f"No computation results found for user {user_id} and business {business_id}")
            return
        
        with open(output_file, 'w') as f:
            json.dump(self.computations[key], f, indent=2)
        print(f"Computation results exported to {output_file}")
    
    def get_all_users(self) -> List[Dict]:
        """Get all users in the system."""
        return list(self.users.values())
    
    def get_all_businesses(self) -> List[Dict]:
        """Get all businesses in the system."""
        return list(self.businesses.values())


def main():
    """
    Main function to demonstrate UK Tax Computations functionality.
    """
    print("=== UK Tax Computations Module ===\n")
    
    # Initialize
    tax_comp = UKTaxComputations()
    
    # Add sample users
    tax_comp.add_user('user1', 'John Smith')
    tax_comp.add_user('user2', 'Jane Doe')
    
    # Add sample businesses
    tax_comp.add_business('biz1', 'Tech Solutions Ltd')
    tax_comp.add_business('biz2', 'Consulting Services Ltd')
    
    print("Users and businesses added successfully")
    print(f"Users: {[u['name'] for u in tax_comp.get_all_users()]}")
    print(f"Businesses: {[b['name'] for b in tax_comp.get_all_businesses()]}\n")
    
    # Sample CSV data
    sample_csv = """date,description,amount,reference,category
2024-12-01,Client Payment,15000.00,INV001,Income
2024-12-05,Office Rent,-3000.00,RENT12,Expense
2024-12-10,Consulting Fee,8500.00,INV002,Income
2024-12-15,Supplier Payment,-2000.00,PO123,Expense
2024-12-20,Project Payment,12000.00,INV003,Income"""
    
    # Import transactions
    print("Importing transactions for user1 and biz1...")
    result = tax_comp.import_transactions_from_csv(sample_csv, 'user1', 'biz1')
    print(f"Import result: {result['message']}")
    
    if result['success']:
        # Compute taxes
        print("\nComputing taxes...")
        computation = tax_comp.compute_tax_from_transactions('user1', 'biz1')
        
        if computation['success']:
            print("\n--- Tax Computation Results ---")
            print(f"Total Income: {format_currency(computation['total_income'])}")
            print(f"Total Expenses: {format_currency(computation['total_expenses'])}")
            print(f"Net Profit: {format_currency(computation['net_profit'])}")
            print(f"Corporation Tax: {format_currency(computation['corporation_tax'])}")
            print(f"VAT Due: {format_currency(computation['vat_due'])}")
    
    print("\n✓ UK Tax Computations demo complete!")


if __name__ == '__main__':
    main()
