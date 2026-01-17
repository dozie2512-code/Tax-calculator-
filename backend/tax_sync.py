"""
Tax Data Synchronization Module
Synchronizes data from postings to optimize tax computations for various entities and tax classes.
Supports: Directors, Employees, Sole Traders, Landlords
Tax Classes: PAYE, Company Tax, CGT, Withholding Tax, VAT
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict
from utils import read_csv_file, safe_float, format_currency


# Configuration Constants
TRADING_ALLOWANCE_THRESHOLD = 10000  # Use trading allowance if income below this
PROPERTY_ALLOWANCE_THRESHOLD = 5000  # Use property allowance if rental income below this
DIRECTOR_KEYWORDS = ['director', 'director salary', 'director remuneration']


class TaxDataSynchronizer:
    """
    Synchronizes financial postings data into tax computation slots.
    Optimizes for reliefs, allowances, allowable expenses, and capital allowances.
    """
    
    def __init__(self, transactions_file: str = None):
        """
        Initialize the tax data synchronizer.
        
        Args:
            transactions_file: Path to transactions CSV file
        """
        self.transactions = []
        self.tax_data = {
            'sole_trader': {},
            'company': {},
            'landlord': {},
            'employee': {}
        }
        self.allowances = {}
        self.reliefs = {}
        self.capital_allowances = {}
        
        if transactions_file:
            self.load_transactions(transactions_file)
    
    def load_transactions(self, transactions_file: str):
        """
        Load transactions from CSV file.
        
        Args:
            transactions_file: Path to CSV file
        """
        self.transactions = read_csv_file(transactions_file)
        print(f"Loaded {len(self.transactions)} transactions")
    
    def categorize_transactions(self) -> Dict[str, List[Dict]]:
        """
        Categorize transactions by entity type and tax relevance.
        
        Returns:
            Dictionary of categorized transactions
        """
        categorized = {
            'income': [],
            'expenses': [],
            'capital_expenditure': [],
            'vat_transactions': [],
            'payroll': [],
            'dividends': [],
            'interest': [],
            'rental': []
        }
        
        for tx in self.transactions:
            account = tx.get('account', '')
            description = tx.get('description', '').lower()
            debit = safe_float(tx.get('debit', 0))
            credit = safe_float(tx.get('credit', 0))
            amount = debit if debit > 0 else credit
            
            # Categorize based on account codes and descriptions
            if account.startswith('4'):  # Revenue accounts
                categorized['income'].append({
                    'account': account,
                    'description': description,
                    'amount': amount,
                    'date': tx.get('date', ''),
                    'type': 'revenue'
                })
            elif account.startswith('5'):  # COGS
                categorized['expenses'].append({
                    'account': account,
                    'description': description,
                    'amount': amount,
                    'date': tx.get('date', ''),
                    'type': 'cogs',
                    'allowable': True
                })
            elif account.startswith('6') or account.startswith('7'):  # Expenses
                categorized['expenses'].append({
                    'account': account,
                    'description': description,
                    'amount': amount,
                    'date': tx.get('date', ''),
                    'type': 'expense',
                    'allowable': self._is_allowable_expense(description)
                })
            elif account.startswith('15'):  # Fixed assets
                categorized['capital_expenditure'].append({
                    'account': account,
                    'description': description,
                    'amount': amount,
                    'date': tx.get('date', ''),
                    'type': 'capital'
                })
            
            # Identify specific transaction types
            if 'vat' in description or 'tax' in description:
                categorized['vat_transactions'].append(tx)
            if 'salary' in description or 'wage' in description or 'payroll' in description:
                categorized['payroll'].append(tx)
            if 'dividend' in description:
                categorized['dividends'].append(tx)
            if 'interest' in description:
                categorized['interest'].append(tx)
            if 'rent' in description or 'rental' in description:
                categorized['rental'].append(tx)
        
        return categorized
    
    def _is_allowable_expense(self, description: str) -> bool:
        """
        Determine if an expense is allowable for tax purposes.
        
        Args:
            description: Expense description
            
        Returns:
            Boolean indicating if expense is allowable
        """
        allowable_keywords = [
            'office', 'supplies', 'travel', 'marketing', 'advertising',
            'professional', 'software', 'equipment', 'insurance',
            'utilities', 'telephone', 'internet', 'postage',
            'stationery', 'training', 'subscription', 'maintenance'
        ]
        
        non_allowable_keywords = [
            'entertainment', 'personal', 'client entertainment',
            'fine', 'penalty'
        ]
        
        description_lower = description.lower()
        
        # Check for non-allowable first
        if any(keyword in description_lower for keyword in non_allowable_keywords):
            return False
        
        # Check for allowable
        if any(keyword in description_lower for keyword in allowable_keywords):
            return True
        
        # Default to allowable for business expenses
        return True
    
    def synchronize_sole_trader_data(self, categorized: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Synchronize data for sole trader tax computations.
        
        Args:
            categorized: Categorized transactions
            
        Returns:
            Dictionary with sole trader tax data
        """
        gross_income = sum(tx['amount'] for tx in categorized['income'])
        
        allowable_expenses = sum(
            tx['amount'] for tx in categorized['expenses']
            if tx.get('allowable', False)
        )
        
        # Calculate capital allowances
        capital_expenditure = sum(
            tx['amount'] for tx in categorized['capital_expenditure']
        )
        capital_allowance = self._calculate_capital_allowance(capital_expenditure)
        
        # Trading allowance option
        trading_allowance = 1000
        use_trading_allowance = gross_income < TRADING_ALLOWANCE_THRESHOLD
        
        self.tax_data['sole_trader'] = {
            'gross_income': gross_income,
            'allowable_expenses': allowable_expenses,
            'capital_allowance': capital_allowance,
            'trading_allowance': trading_allowance,
            'use_trading_allowance': use_trading_allowance,
            'profit': gross_income - (trading_allowance if use_trading_allowance else allowable_expenses),
            'vat_collected': sum(safe_float(tx.get('credit', 0)) for tx in categorized['vat_transactions'])
        }
        
        return self.tax_data['sole_trader']
    
    def synchronize_company_data(self, categorized: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Synchronize data for limited company tax computations.
        
        Args:
            categorized: Categorized transactions
            
        Returns:
            Dictionary with company tax data
        """
        revenue = sum(tx['amount'] for tx in categorized['income'])
        expenses = sum(tx['amount'] for tx in categorized['expenses'])
        
        # Director's remuneration
        director_salary = sum(
            safe_float(tx.get('debit', 0)) for tx in categorized['payroll']
            if any(keyword in tx.get('description', '').lower() for keyword in DIRECTOR_KEYWORDS)
        )
        
        dividends = sum(
            safe_float(tx.get('debit', 0)) for tx in categorized['dividends']
        )
        
        company_profit = revenue - expenses
        
        self.tax_data['company'] = {
            'company_profit': company_profit,
            'director_salary': director_salary,
            'dividends': dividends,
            'revenue': revenue,
            'expenses': expenses,
            'vat_collected': sum(safe_float(tx.get('credit', 0)) for tx in categorized['vat_transactions'])
        }
        
        return self.tax_data['company']
    
    def synchronize_landlord_data(self, categorized: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Synchronize data for landlord tax computations.
        
        Args:
            categorized: Categorized transactions
            
        Returns:
            Dictionary with landlord tax data
        """
        rental_income = 0
        for tx in categorized['rental']:
            debit = safe_float(tx.get('debit', 0))
            credit = safe_float(tx.get('credit', 0))
            # Rental income is typically a credit (revenue)
            rental_income += credit if credit > 0 else debit
        
        property_expenses = sum(
            tx['amount'] for tx in categorized['expenses']
            if 'property' in tx.get('description', '').lower() or
               'maintenance' in tx.get('description', '').lower() or
               'repair' in tx.get('description', '').lower()
        )
        
        # Property allowance
        property_allowance = 1000
        use_property_allowance = rental_income < PROPERTY_ALLOWANCE_THRESHOLD
        
        # Capital gains from property sales
        capital_gains = 0  # Would need specific property sale transactions
        
        self.tax_data['landlord'] = {
            'rental_income': rental_income,
            'property_expenses': property_expenses,
            'property_allowance': property_allowance,
            'use_property_allowance': use_property_allowance,
            'capital_gains': capital_gains,
            'other_income': 0
        }
        
        return self.tax_data['landlord']
    
    def synchronize_employee_data(self, categorized: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Synchronize data for employee tax computations (PAYE).
        
        Args:
            categorized: Categorized transactions
            
        Returns:
            Dictionary with employee tax data
        """
        gross_salary = sum(
            safe_float(tx.get('credit', 0)) for tx in categorized['payroll']
            if 'salary' in tx.get('description', '').lower() or
               'wage' in tx.get('description', '').lower()
        )
        
        bonus = sum(
            safe_float(tx.get('credit', 0)) for tx in categorized['payroll']
            if 'bonus' in tx.get('description', '').lower()
        )
        
        # Other income from investments, dividends, etc.
        other_income = sum(tx['amount'] for tx in categorized['dividends']) + \
                      sum(safe_float(tx.get('credit', 0)) for tx in categorized['interest'])
        
        self.tax_data['employee'] = {
            'gross_salary': gross_salary,
            'bonus': bonus,
            'other_income': other_income,
            'pension_contributions': 0  # Would need pension transaction data
        }
        
        return self.tax_data['employee']
    
    def _calculate_capital_allowance(self, capital_expenditure: float) -> Dict[str, float]:
        """
        Calculate capital allowances for different asset types.
        
        Args:
            capital_expenditure: Total capital expenditure
            
        Returns:
            Dictionary with capital allowance calculations
        """
        # Annual Investment Allowance (AIA) - 100% relief up to £1,000,000
        aia_limit = 1000000
        aia_relief = min(capital_expenditure, aia_limit)
        
        # Writing Down Allowance (WDA) - 18% for main pool, 6% for special rate pool
        remaining_expenditure = max(0, capital_expenditure - aia_limit)
        main_pool_wda = remaining_expenditure * 0.18
        
        return {
            'aia_relief': aia_relief,
            'wda_relief': main_pool_wda,
            'total_relief': aia_relief + main_pool_wda
        }
    
    def calculate_optimized_allowances(self) -> Dict[str, Any]:
        """
        Calculate optimized allowances and reliefs across all entity types.
        
        Returns:
            Dictionary with optimized allowances
        """
        self.allowances = {
            'personal_allowance': 12570,
            'trading_allowance': 1000,
            'property_allowance': 1000,
            'dividend_allowance': 500,
            'savings_allowance_basic': 1000,
            'savings_allowance_higher': 500,
            'marriage_allowance': 1260,
            'pension_annual_allowance': 60000,
            'capital_gains_allowance': 3000
        }
        
        return self.allowances
    
    def synchronize_all_entities(self) -> Dict[str, Any]:
        """
        Synchronize data for all entity types.
        
        Returns:
            Dictionary with all synchronized tax data
        """
        print("\n=== Tax Data Synchronization ===\n")
        
        categorized = self.categorize_transactions()
        
        print("Synchronizing Sole Trader data...")
        self.synchronize_sole_trader_data(categorized)
        
        print("Synchronizing Company data...")
        self.synchronize_company_data(categorized)
        
        print("Synchronizing Landlord data...")
        self.synchronize_landlord_data(categorized)
        
        print("Synchronizing Employee data...")
        self.synchronize_employee_data(categorized)
        
        print("Calculating optimized allowances...")
        self.calculate_optimized_allowances()
        
        return {
            'synchronization_date': datetime.now().isoformat(),
            'entities': self.tax_data,
            'allowances': self.allowances,
            'summary': self._generate_summary(categorized)
        }
    
    def _generate_summary(self, categorized: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Generate summary of synchronized data.
        
        Args:
            categorized: Categorized transactions
            
        Returns:
            Summary dictionary
        """
        return {
            'total_income': format_currency(sum(tx['amount'] for tx in categorized['income'])),
            'total_expenses': format_currency(sum(tx['amount'] for tx in categorized['expenses'])),
            'allowable_expenses': format_currency(
                sum(tx['amount'] for tx in categorized['expenses'] if tx.get('allowable', False))
            ),
            'capital_expenditure': format_currency(sum(tx['amount'] for tx in categorized['capital_expenditure'])),
            'vat_transactions_count': len(categorized['vat_transactions']),
            'payroll_transactions_count': len(categorized['payroll'])
        }
    
    def export_synchronized_data(self, output_file: str = 'output/tax_synchronized_data.json'):
        """
        Export synchronized tax data to JSON file.
        
        Args:
            output_file: Path to output JSON file
        """
        synchronized_data = self.synchronize_all_entities()
        
        with open(output_file, 'w') as f:
            json.dump(synchronized_data, f, indent=2)
        
        print(f"\n✓ Tax data synchronized and exported to {output_file}")
        return synchronized_data


def main():
    """
    Main function to demonstrate tax data synchronization.
    """
    print("=== Tax Data Synchronization Module ===\n")
    
    synchronizer = TaxDataSynchronizer('sample_data/transactions.csv')
    
    # Synchronize all entity data
    result = synchronizer.export_synchronized_data('output/tax_synchronized_data.json')
    
    # Display summary
    print("\n--- Synchronization Summary ---")
    for key, value in result['summary'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n--- Entity Data ---")
    for entity, data in result['entities'].items():
        print(f"\n{entity.replace('_', ' ').title()}:")
        for key, value in data.items():
            if isinstance(value, (int, float)):
                print(f"  {key.replace('_', ' ').title()}: {format_currency(value)}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n✓ Tax data synchronization complete!")


if __name__ == '__main__':
    main()
