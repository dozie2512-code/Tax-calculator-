"""
Accrual Postings Module for Autonomous Month-End Close Process
Automatically calculates and generates journal entries for accruals
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from utils import read_csv_file, write_csv_file, safe_float, safe_int, format_currency


class AccrualCalculator:
    """
    Calculates accruals for interest, depreciation, and other periodic expenses.
    Generates journal entries for the calculated accruals.
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize the accrual calculator with configuration.
        
        Args:
            config_file: Optional path to configuration file for accrual rates
        """
        self.journal_entries = []
        self.accruals = {}
        
        # Default accrual rates (can be overridden by config file)
        self.config = {
            'interest_rate': 0.05,  # 5% annual interest rate
            'depreciation_rate': 0.10,  # 10% straight-line depreciation
            'accrual_accounts': {
                'interest_expense': '7200',
                'interest_payable': '2300',
                'depreciation_expense': '7100',
                'accumulated_depreciation': '1500'
            }
        }
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str):
        """
        Load accrual configuration from JSON file.
        
        Args:
            config_file: Path to JSON configuration file
        """
        try:
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
            print(f"Configuration loaded from {config_file}")
        except FileNotFoundError:
            print(f"Config file not found: {config_file}. Using defaults.")
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
    
    def calculate_interest_accrual(self, principal: float, months: int = 1) -> Dict[str, Any]:
        """
        Calculate interest accrual for the period.
        
        Args:
            principal: Principal amount
            months: Number of months (default: 1)
            
        Returns:
            Dictionary containing accrual details
        """
        annual_rate = self.config.get('interest_rate', 0.05)
        monthly_rate = annual_rate / 12
        interest_amount = principal * monthly_rate * months
        
        accrual = {
            'type': 'Interest Accrual',
            'principal': principal,
            'rate': annual_rate,
            'period_months': months,
            'accrual_amount': round(interest_amount, 2),
            'calculation_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        return accrual
    
    def calculate_depreciation_accrual(self, asset_cost: float, 
                                      salvage_value: float = 0, 
                                      useful_life_years: int = 5) -> Dict[str, Any]:
        """
        Calculate monthly depreciation accrual using straight-line method.
        
        Args:
            asset_cost: Original cost of the asset
            salvage_value: Expected salvage value at end of useful life
            useful_life_years: Expected useful life in years
            
        Returns:
            Dictionary containing depreciation details
        """
        depreciable_amount = asset_cost - salvage_value
        annual_depreciation = depreciable_amount / useful_life_years
        monthly_depreciation = annual_depreciation / 12
        
        accrual = {
            'type': 'Depreciation Accrual',
            'asset_cost': asset_cost,
            'salvage_value': salvage_value,
            'useful_life_years': useful_life_years,
            'monthly_depreciation': round(monthly_depreciation, 2),
            'annual_depreciation': round(annual_depreciation, 2),
            'calculation_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        return accrual
    
    def calculate_expense_accrual(self, expense_name: str, 
                                  annual_amount: float, 
                                  months: int = 1) -> Dict[str, Any]:
        """
        Calculate accrual for periodic expenses (e.g., rent, utilities).
        
        Args:
            expense_name: Name of the expense
            annual_amount: Annual expense amount
            months: Number of months to accrue (default: 1)
            
        Returns:
            Dictionary containing expense accrual details
        """
        monthly_amount = annual_amount / 12
        accrual_amount = monthly_amount * months
        
        accrual = {
            'type': f'{expense_name} Accrual',
            'annual_amount': annual_amount,
            'monthly_amount': round(monthly_amount, 2),
            'period_months': months,
            'accrual_amount': round(accrual_amount, 2),
            'calculation_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        return accrual
    
    def generate_journal_entry(self, accrual: Dict[str, Any], 
                              debit_account: str, 
                              credit_account: str,
                              entry_date: str = None) -> Dict[str, Any]:
        """
        Generate a journal entry for an accrual.
        
        Args:
            accrual: Accrual dictionary with calculation details
            debit_account: Account to debit
            credit_account: Account to credit
            entry_date: Date for the journal entry (default: today)
            
        Returns:
            Dictionary containing journal entry details
        """
        if not entry_date:
            entry_date = datetime.now().strftime('%Y-%m-%d')
        
        amount = accrual.get('accrual_amount', 0) or \
                accrual.get('monthly_depreciation', 0)
        
        entry = {
            'entry_date': entry_date,
            'description': accrual.get('type', 'Accrual Entry'),
            'lines': [
                {
                    'account': debit_account,
                    'account_type': 'Expense',
                    'debit': round(amount, 2),
                    'credit': 0
                },
                {
                    'account': credit_account,
                    'account_type': 'Liability/Contra-Asset',
                    'debit': 0,
                    'credit': round(amount, 2)
                }
            ],
            'total_debit': round(amount, 2),
            'total_credit': round(amount, 2),
            'balanced': True
        }
        
        self.journal_entries.append(entry)
        return entry
    
    def process_accruals_from_file(self, accruals_file: str) -> List[Dict[str, Any]]:
        """
        Process accruals from a CSV file containing accrual specifications.
        
        Args:
            accruals_file: Path to CSV file with accrual data
            
        Returns:
            List of calculated accruals
        """
        accrual_data = read_csv_file(accruals_file)
        calculated_accruals = []
        
        for row in accrual_data:
            accrual_type = row.get('type', '').lower()
            
            if accrual_type == 'interest':
                principal = safe_float(row.get('principal', 0))
                months = safe_int(row.get('months', 1), 1)
                accrual = self.calculate_interest_accrual(principal, months)
                calculated_accruals.append(accrual)
                
                # Generate journal entry
                self.generate_journal_entry(
                    accrual,
                    self.config['accrual_accounts']['interest_expense'],
                    self.config['accrual_accounts']['interest_payable'],
                    row.get('date')
                )
                
            elif accrual_type == 'depreciation':
                asset_cost = safe_float(row.get('asset_cost', 0))
                salvage = safe_float(row.get('salvage_value', 0))
                life = safe_int(row.get('useful_life_years', 5), 5)
                accrual = self.calculate_depreciation_accrual(asset_cost, salvage, life)
                calculated_accruals.append(accrual)
                
                # Generate journal entry
                self.generate_journal_entry(
                    accrual,
                    self.config['accrual_accounts']['depreciation_expense'],
                    self.config['accrual_accounts']['accumulated_depreciation'],
                    row.get('date')
                )
                
            elif accrual_type == 'expense':
                expense_name = row.get('name', 'General Expense')
                annual_amount = safe_float(row.get('annual_amount', 0))
                months = safe_int(row.get('months', 1), 1)
                accrual = self.calculate_expense_accrual(expense_name, annual_amount, months)
                calculated_accruals.append(accrual)
                
                # Generate journal entry (use generic accounts)
                debit_acct = row.get('debit_account', '6000')
                credit_acct = row.get('credit_account', '2000')
                self.generate_journal_entry(accrual, debit_acct, credit_acct, row.get('date'))
        
        return calculated_accruals
    
    def export_journal_entries(self, output_file: str = 'output/journal_entries.json'):
        """
        Export journal entries to JSON file.
        
        Args:
            output_file: Path to output JSON file
        """
        with open(output_file, 'w') as f:
            json.dump(self.journal_entries, f, indent=2)
        print(f"Journal entries exported to {output_file}")
        
        # Also create CSV version for easier viewing
        csv_file = output_file.replace('.json', '.csv')
        csv_data = []
        for entry in self.journal_entries:
            for line in entry['lines']:
                csv_data.append({
                    'date': entry['entry_date'],
                    'description': entry['description'],
                    'account': line['account'],
                    'account_type': line['account_type'],
                    'debit': line['debit'],
                    'credit': line['credit']
                })
        
        if csv_data:
            write_csv_file(csv_file, csv_data, list(csv_data[0].keys()))
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of all accruals and journal entries.
        
        Returns:
            Dictionary containing summary information
        """
        total_debits = sum(entry['total_debit'] for entry in self.journal_entries)
        total_credits = sum(entry['total_credit'] for entry in self.journal_entries)
        
        summary = {
            'total_journal_entries': len(self.journal_entries),
            'total_debits': format_currency(total_debits),
            'total_credits': format_currency(total_credits),
            'balanced': total_debits == total_credits,
            'entry_types': {}
        }
        
        # Count entry types
        for entry in self.journal_entries:
            desc = entry['description']
            summary['entry_types'][desc] = summary['entry_types'].get(desc, 0) + 1
        
        return summary


def main():
    """
    Main function to demonstrate accrual calculation functionality.
    """
    print("=== Accrual Postings Module ===\n")
    
    calculator = AccrualCalculator()
    
    # Example: Calculate interest accrual
    print("Calculating interest accrual...")
    interest = calculator.calculate_interest_accrual(principal=100000, months=1)
    print(f"Interest Accrual: {format_currency(interest['accrual_amount'])}")
    calculator.generate_journal_entry(
        interest,
        calculator.config['accrual_accounts']['interest_expense'],
        calculator.config['accrual_accounts']['interest_payable']
    )
    
    # Example: Calculate depreciation accrual
    print("Calculating depreciation accrual...")
    depreciation = calculator.calculate_depreciation_accrual(
        asset_cost=50000, 
        salvage_value=5000, 
        useful_life_years=5
    )
    print(f"Monthly Depreciation: {format_currency(depreciation['monthly_depreciation'])}")
    calculator.generate_journal_entry(
        depreciation,
        calculator.config['accrual_accounts']['depreciation_expense'],
        calculator.config['accrual_accounts']['accumulated_depreciation']
    )
    
    # Display summary
    print("\n--- Accruals Summary ---")
    summary = calculator.get_summary()
    for key, value in summary.items():
        if key != 'entry_types':
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Export journal entries
    print("\nExporting journal entries...")
    calculator.export_journal_entries('output/journal_entries.json')
    
    print("\n✓ Accrual calculations complete!")


if __name__ == '__main__':
    main()
