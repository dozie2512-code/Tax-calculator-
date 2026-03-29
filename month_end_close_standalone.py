"""
Autonomous Month-End Close Process - Standalone Consolidated Version
=====================================================================

This standalone script consolidates all modules for the month-end close process:
- Utility functions for CSV handling and formatting
- Account reconciliation between GL and bank statements
- Accrual calculations and journal entry generation
- Financial statement generation (P&L, Balance Sheet, Cash Flow)
- Complete process orchestration

All functionality is contained in this single file for easy distribution and use.
No external dependencies required - uses only Python standard library.

Usage:
    python month_end_close_standalone.py

Author: Tax Calculator Project
Date: 2026-01-01
"""

import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple
from collections import defaultdict


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def read_csv_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Read a CSV file and return a list of dictionaries.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries where keys are column headers
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    
    return data


def write_csv_file(filepath: str, data: List[Dict[str, Any]], fieldnames: List[str]):
    """
    Write data to a CSV file.
    
    Args:
        filepath: Path to the output CSV file
        data: List of dictionaries to write
        fieldnames: List of column headers
    """
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {filepath}")
    except Exception as e:
        print(f"Error writing CSV file: {e}")


def parse_date(date_str: str, format: str = '%Y-%m-%d') -> datetime:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_str: Date string to parse
        format: Expected date format (default: '%Y-%m-%d')
        
    Returns:
        datetime object
    """
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        # Try alternative formats
        for fmt in ['%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {date_str}")


def format_currency(amount: float) -> str:
    """
    Format a number as currency (GBP).
    
    Args:
        amount: Numerical amount
        
    Returns:
        Formatted currency string
    """
    return f"£{amount:,.2f}"


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to int.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Int value or default
    """
    try:
        if isinstance(value, str) and not value.strip():
            return default
        return int(value)
    except (ValueError, TypeError):
        return default


# ============================================================================
# ACCOUNT RECONCILIATION MODULE
# ============================================================================

class AccountReconciliation:
    """
    Performs account reconciliation between general ledger and bank statements.
    Identifies matched and unmatched transactions, flags discrepancies.
    """
    
    def __init__(self, gl_file: str, bank_file: str):
        """
        Initialize the reconciliation with GL and bank statement files.
        
        Args:
            gl_file: Path to general ledger CSV file
            bank_file: Path to bank statement CSV file
        """
        self.gl_transactions = read_csv_file(gl_file)
        self.bank_transactions = read_csv_file(bank_file)
        self.matched = []
        self.unmatched_gl = []
        self.unmatched_bank = []
        self.discrepancies = []
        
    def reconcile(self, tolerance: float = 0.01) -> Dict[str, Any]:
        """
        Perform reconciliation between GL and bank transactions.
        
        Args:
            tolerance: Acceptable difference for amount matching (default: 0.01)
            
        Returns:
            Dictionary containing reconciliation results
        """
        # Create copies to track unmatched items
        remaining_gl = self.gl_transactions.copy()
        remaining_bank = self.bank_transactions.copy()
        
        # Try to match GL transactions with bank transactions
        for gl_tx in self.gl_transactions:
            gl_amount = safe_float(gl_tx.get('amount', 0))
            gl_date = gl_tx.get('date', '')
            gl_desc = gl_tx.get('description', '').lower()
            gl_ref = gl_tx.get('reference', '')
            
            match_found = False
            
            for bank_tx in remaining_bank[:]:
                bank_amount = safe_float(bank_tx.get('amount', 0))
                bank_date = bank_tx.get('date', '')
                bank_desc = bank_tx.get('description', '').lower()
                bank_ref = bank_tx.get('reference', '')
                
                # Matching criteria: amount, date, and reference/description similarity
                amount_match = abs(gl_amount - bank_amount) <= tolerance
                date_match = gl_date == bank_date
                ref_match = (gl_ref and gl_ref == bank_ref) or \
                           (gl_desc and bank_desc and gl_desc in bank_desc) or \
                           (bank_desc and gl_desc and bank_desc in gl_desc)
                
                if amount_match and (date_match or ref_match):
                    # Match found
                    self.matched.append({
                        'gl_transaction': gl_tx,
                        'bank_transaction': bank_tx,
                        'match_confidence': 'High' if date_match and ref_match else 'Medium'
                    })
                    
                    if gl_tx in remaining_gl:
                        remaining_gl.remove(gl_tx)
                    remaining_bank.remove(bank_tx)
                    match_found = True
                    break
            
            if not match_found and gl_amount != 0:
                # Check for potential discrepancies
                for bank_tx in self.bank_transactions:
                    bank_amount = safe_float(bank_tx.get('amount', 0))
                    if abs(abs(gl_amount) - abs(bank_amount)) < 100 and abs(gl_amount - bank_amount) > tolerance:
                        self.discrepancies.append({
                            'gl_transaction': gl_tx,
                            'bank_transaction': bank_tx,
                            'difference': gl_amount - bank_amount,
                            'type': 'Amount Mismatch'
                        })
        
        # Store remaining unmatched transactions
        self.unmatched_gl = remaining_gl
        self.unmatched_bank = remaining_bank
        
        return self.generate_summary()
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate a summary report of the reconciliation.
        
        Returns:
            Dictionary containing reconciliation summary
        """
        total_gl_amount = sum(safe_float(tx.get('amount', 0)) for tx in self.gl_transactions)
        total_bank_amount = sum(safe_float(tx.get('amount', 0)) for tx in self.bank_transactions)
        matched_amount = sum(safe_float(match['gl_transaction'].get('amount', 0)) 
                            for match in self.matched)
        
        summary = {
            'total_gl_transactions': len(self.gl_transactions),
            'total_bank_transactions': len(self.bank_transactions),
            'matched_transactions': len(self.matched),
            'unmatched_gl_transactions': len(self.unmatched_gl),
            'unmatched_bank_transactions': len(self.unmatched_bank),
            'discrepancies_found': len(self.discrepancies),
            'total_gl_amount': format_currency(total_gl_amount),
            'total_bank_amount': format_currency(total_bank_amount),
            'matched_amount': format_currency(matched_amount),
            'reconciliation_percentage': round((len(self.matched) / max(len(self.gl_transactions), 1)) * 100, 2)
        }
        
        return summary
    
    def export_results(self, output_prefix: str = 'reconciliation'):
        """
        Export reconciliation results to CSV files.
        
        Args:
            output_prefix: Prefix for output files
        """
        # Export matched transactions
        if self.matched:
            matched_data = []
            for match in self.matched:
                matched_data.append({
                    'gl_date': match['gl_transaction'].get('date', ''),
                    'gl_reference': match['gl_transaction'].get('reference', ''),
                    'gl_description': match['gl_transaction'].get('description', ''),
                    'gl_amount': match['gl_transaction'].get('amount', ''),
                    'bank_date': match['bank_transaction'].get('date', ''),
                    'bank_reference': match['bank_transaction'].get('reference', ''),
                    'bank_description': match['bank_transaction'].get('description', ''),
                    'bank_amount': match['bank_transaction'].get('amount', ''),
                    'confidence': match['match_confidence']
                })
            write_csv_file(f'{output_prefix}_matched.csv', matched_data, 
                          list(matched_data[0].keys()) if matched_data else [])
        
        # Export unmatched GL transactions
        if self.unmatched_gl:
            write_csv_file(f'{output_prefix}_unmatched_gl.csv', self.unmatched_gl,
                          list(self.unmatched_gl[0].keys()) if self.unmatched_gl else [])
        
        # Export unmatched bank transactions
        if self.unmatched_bank:
            write_csv_file(f'{output_prefix}_unmatched_bank.csv', self.unmatched_bank,
                          list(self.unmatched_bank[0].keys()) if self.unmatched_bank else [])
        
        # Export discrepancies
        if self.discrepancies:
            disc_data = []
            for disc in self.discrepancies:
                disc_data.append({
                    'gl_reference': disc['gl_transaction'].get('reference', ''),
                    'gl_description': disc['gl_transaction'].get('description', ''),
                    'gl_amount': disc['gl_transaction'].get('amount', ''),
                    'bank_reference': disc['bank_transaction'].get('reference', ''),
                    'bank_description': disc['bank_transaction'].get('description', ''),
                    'bank_amount': disc['bank_transaction'].get('amount', ''),
                    'difference': disc['difference'],
                    'type': disc['type']
                })
            write_csv_file(f'{output_prefix}_discrepancies.csv', disc_data,
                          list(disc_data[0].keys()) if disc_data else [])
        
        # Export summary as JSON
        summary = self.generate_summary()
        with open(f'{output_prefix}_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Reconciliation summary saved to {output_prefix}_summary.json")


# ============================================================================
# ACCRUAL POSTINGS MODULE
# ============================================================================

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


# ============================================================================
# FINANCIAL STATEMENT GENERATION MODULE
# ============================================================================

class FinancialStatementGenerator:
    """
    Generates financial statements from transaction data.
    Produces Profit & Loss (Income Statement), Balance Sheet, and Cash Flow Statement.
    """
    
    def __init__(self, transactions_file: str):
        """
        Initialize the statement generator with transaction data.
        
        Args:
            transactions_file: Path to CSV file containing all transactions
        """
        self.transactions = read_csv_file(transactions_file)
        self.accounts = defaultdict(lambda: {'balance': 0.0, 'type': 'Unknown', 'debits': 0.0, 'credits': 0.0})
        self.period_start = None
        self.period_end = None
        
        # Standard account type mappings (can be customized)
        self.account_types = {
            # Assets (1000-1999)
            '1000': 'Asset', '1100': 'Asset', '1200': 'Asset', '1300': 'Asset',
            # Liabilities (2000-2999)
            '2000': 'Liability', '2100': 'Liability', '2200': 'Liability', '2300': 'Liability',
            # Equity (3000-3999)
            '3000': 'Equity', '3100': 'Equity',
            # Revenue (4000-4999)
            '4000': 'Revenue', '4100': 'Revenue', '4200': 'Revenue',
            # Cost of Goods Sold (5000-5999)
            '5000': 'COGS', '5100': 'COGS',
            # Expenses (6000-7999)
            '6000': 'Expense', '6100': 'Expense', '6200': 'Expense',
            '7000': 'Expense', '7100': 'Expense', '7200': 'Expense'
        }
    
    def process_transactions(self):
        """
        Process all transactions and update account balances.
        """
        print(f"Processing {len(self.transactions)} transactions...")
        
        for tx in self.transactions:
            account = tx.get('account', '')
            debit = safe_float(tx.get('debit', 0))
            credit = safe_float(tx.get('credit', 0))
            date = tx.get('date', '')
            
            # Track period dates
            if date:
                if not self.period_start or date < self.period_start:
                    self.period_start = date
                if not self.period_end or date > self.period_end:
                    self.period_end = date
            
            # Determine account type
            account_type = self.account_types.get(account, 'Unknown')
            if account_type == 'Unknown' and account:
                # Try to infer from account number
                first_digit = account[0] if account else '0'
                if first_digit == '1':
                    account_type = 'Asset'
                elif first_digit == '2':
                    account_type = 'Liability'
                elif first_digit == '3':
                    account_type = 'Equity'
                elif first_digit == '4':
                    account_type = 'Revenue'
                elif first_digit == '5':
                    account_type = 'COGS'
                elif first_digit in ['6', '7']:
                    account_type = 'Expense'
            
            # Update account balances
            if account:
                self.accounts[account]['type'] = account_type
                self.accounts[account]['debits'] += debit
                self.accounts[account]['credits'] += credit
                
                # Calculate balance based on account type
                if account_type in ['Asset', 'Expense', 'COGS']:
                    # Normal debit balance accounts
                    self.accounts[account]['balance'] += debit - credit
                else:
                    # Normal credit balance accounts (Liability, Equity, Revenue)
                    self.accounts[account]['balance'] += credit - debit
        
        print(f"Processed {len(self.accounts)} unique accounts")
    
    def generate_profit_and_loss(self) -> Dict[str, Any]:
        """
        Generate Profit & Loss Statement (Income Statement).
        
        Returns:
            Dictionary containing P&L statement
        """
        revenue = 0.0
        cogs = 0.0
        expenses = 0.0
        
        revenue_details = []
        cogs_details = []
        expense_details = []
        
        for account, data in self.accounts.items():
            account_type = data['type']
            balance = data['balance']
            
            if account_type == 'Revenue':
                revenue += balance
                revenue_details.append({
                    'account': account,
                    'amount': balance
                })
            elif account_type == 'COGS':
                cogs += balance
                cogs_details.append({
                    'account': account,
                    'amount': balance
                })
            elif account_type == 'Expense':
                expenses += balance
                expense_details.append({
                    'account': account,
                    'amount': balance
                })
        
        gross_profit = revenue - cogs
        operating_income = gross_profit - expenses
        net_income = operating_income  # Simplified (no other income/expenses)
        
        pl_statement = {
            'statement_type': 'Profit & Loss Statement',
            'period_start': self.period_start,
            'period_end': self.period_end,
            'revenue': {
                'total': revenue,
                'formatted': format_currency(revenue),
                'details': revenue_details
            },
            'cost_of_goods_sold': {
                'total': cogs,
                'formatted': format_currency(cogs),
                'details': cogs_details
            },
            'gross_profit': {
                'total': gross_profit,
                'formatted': format_currency(gross_profit)
            },
            'operating_expenses': {
                'total': expenses,
                'formatted': format_currency(expenses),
                'details': expense_details
            },
            'operating_income': {
                'total': operating_income,
                'formatted': format_currency(operating_income)
            },
            'net_income': {
                'total': net_income,
                'formatted': format_currency(net_income)
            }
        }
        
        return pl_statement
    
    def generate_balance_sheet(self) -> Dict[str, Any]:
        """
        Generate Balance Sheet.
        
        Returns:
            Dictionary containing balance sheet
        """
        assets = 0.0
        liabilities = 0.0
        equity = 0.0
        
        asset_details = []
        liability_details = []
        equity_details = []
        
        for account, data in self.accounts.items():
            account_type = data['type']
            balance = data['balance']
            
            if account_type == 'Asset':
                assets += balance
                asset_details.append({
                    'account': account,
                    'amount': balance
                })
            elif account_type == 'Liability':
                liabilities += balance
                liability_details.append({
                    'account': account,
                    'amount': balance
                })
            elif account_type == 'Equity':
                equity += balance
                equity_details.append({
                    'account': account,
                    'amount': balance
                })
        
        # Add net income to equity
        pl_statement = self.generate_profit_and_loss()
        net_income = pl_statement['net_income']['total']
        equity += net_income
        equity_details.append({
            'account': 'Retained Earnings (Net Income)',
            'amount': net_income
        })
        
        total_liabilities_equity = liabilities + equity
        balanced = abs(assets - total_liabilities_equity) < 0.01
        
        balance_sheet = {
            'statement_type': 'Balance Sheet',
            'as_of_date': self.period_end or datetime.now().strftime('%Y-%m-%d'),
            'assets': {
                'total': assets,
                'formatted': format_currency(assets),
                'details': asset_details
            },
            'liabilities': {
                'total': liabilities,
                'formatted': format_currency(liabilities),
                'details': liability_details
            },
            'equity': {
                'total': equity,
                'formatted': format_currency(equity),
                'details': equity_details
            },
            'total_liabilities_and_equity': {
                'total': total_liabilities_equity,
                'formatted': format_currency(total_liabilities_equity)
            },
            'balanced': balanced
        }
        
        return balance_sheet
    
    def generate_cash_flow(self) -> Dict[str, Any]:
        """
        Generate Cash Flow Statement (simplified version).
        
        Returns:
            Dictionary containing cash flow statement
        """
        # Simplified cash flow based on account movements
        operating_cash = 0.0
        investing_cash = 0.0
        financing_cash = 0.0
        
        operating_details = []
        investing_details = []
        financing_details = []
        
        # Get net income from P&L
        pl_statement = self.generate_profit_and_loss()
        net_income = pl_statement['net_income']['total']
        operating_cash += net_income
        operating_details.append({
            'description': 'Net Income',
            'amount': net_income
        })
        
        # Analyze account changes for cash flow classification
        for account, data in self.accounts.items():
            account_type = data['type']
            balance = data['balance']
            
            # Simplified classification
            if account_type in ['Asset', 'Liability'] and account.startswith('1'):
                # Current assets changes (simplified)
                if account not in ['1000', '1001']:  # Exclude cash accounts
                    operating_cash -= balance
                    operating_details.append({
                        'description': f'Account {account} change',
                        'amount': -balance
                    })
            elif account.startswith('15'):  # Fixed assets (example)
                investing_cash -= balance
                investing_details.append({
                    'description': f'Asset acquisition {account}',
                    'amount': -balance
                })
            elif account_type == 'Liability' and account.startswith('25'):  # Long-term debt
                financing_cash += balance
                financing_details.append({
                    'description': f'Debt change {account}',
                    'amount': balance
                })
        
        net_cash_change = operating_cash + investing_cash + financing_cash
        
        cash_flow = {
            'statement_type': 'Cash Flow Statement',
            'period_start': self.period_start,
            'period_end': self.period_end,
            'operating_activities': {
                'total': operating_cash,
                'formatted': format_currency(operating_cash),
                'details': operating_details
            },
            'investing_activities': {
                'total': investing_cash,
                'formatted': format_currency(investing_cash),
                'details': investing_details
            },
            'financing_activities': {
                'total': financing_cash,
                'formatted': format_currency(financing_cash),
                'details': financing_details
            },
            'net_cash_change': {
                'total': net_cash_change,
                'formatted': format_currency(net_cash_change)
            }
        }
        
        return cash_flow
    
    def generate_all_statements(self) -> Dict[str, Any]:
        """
        Generate all financial statements.
        
        Returns:
            Dictionary containing all statements
        """
        self.process_transactions()
        
        statements = {
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'profit_and_loss': self.generate_profit_and_loss(),
            'balance_sheet': self.generate_balance_sheet(),
            'cash_flow': self.generate_cash_flow()
        }
        
        return statements
    
    def export_statements(self, output_file: str = 'output/financial_statements.json'):
        """
        Export all financial statements to JSON file.
        
        Args:
            output_file: Path to output JSON file
        """
        statements = self.generate_all_statements()
        
        with open(output_file, 'w') as f:
            json.dump(statements, f, indent=2)
        
        print(f"Financial statements exported to {output_file}")
        
        return statements


# ============================================================================
# MONTH-END CLOSE ORCHESTRATION
# ============================================================================

class MonthEndCloseProcess:
    """
    Orchestrates the complete month-end close process.
    """
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize the month-end close process.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        self.results = {
            'process_start': datetime.now().isoformat(),
            'status': 'In Progress',
            'steps': {}
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def step_1_reconciliation(self) -> dict:
        """
        Step 1: Perform account reconciliation.
        
        Returns:
            Reconciliation results
        """
        print("\n" + "="*60)
        print("STEP 1: ACCOUNT RECONCILIATION")
        print("="*60)
        
        try:
            reconciler = AccountReconciliation(
                'sample_data/general_ledger.csv',
                'sample_data/bank_statement.csv'
            )
            
            summary = reconciler.reconcile()
            reconciler.export_results(f'{self.output_dir}/reconciliation')
            
            self.results['steps']['reconciliation'] = {
                'status': 'Completed',
                'summary': summary
            }
            
            print("\n✓ Reconciliation completed successfully")
            return summary
            
        except Exception as e:
            print(f"\n✗ Reconciliation failed: {e}")
            self.results['steps']['reconciliation'] = {
                'status': 'Failed',
                'error': str(e)
            }
            return {}
    
    def step_2_accruals(self) -> dict:
        """
        Step 2: Calculate and post accruals.
        
        Returns:
            Accruals summary
        """
        print("\n" + "="*60)
        print("STEP 2: ACCRUAL POSTINGS")
        print("="*60)
        
        try:
            calculator = AccrualCalculator()
            
            # Process accruals from file
            accruals = calculator.process_accruals_from_file('sample_data/accruals.csv')
            calculator.export_journal_entries(f'{self.output_dir}/journal_entries.json')
            
            summary = calculator.get_summary()
            
            self.results['steps']['accruals'] = {
                'status': 'Completed',
                'summary': summary,
                'accruals_count': len(accruals)
            }
            
            print("\n✓ Accrual postings completed successfully")
            return summary
            
        except Exception as e:
            print(f"\n✗ Accrual postings failed: {e}")
            self.results['steps']['accruals'] = {
                'status': 'Failed',
                'error': str(e)
            }
            return {}
    
    def step_3_financial_statements(self) -> dict:
        """
        Step 3: Generate financial statements.
        
        Returns:
            Financial statements
        """
        print("\n" + "="*60)
        print("STEP 3: FINANCIAL STATEMENT GENERATION")
        print("="*60)
        
        try:
            generator = FinancialStatementGenerator('sample_data/transactions.csv')
            statements = generator.export_statements(f'{self.output_dir}/financial_statements.json')
            
            self.results['steps']['financial_statements'] = {
                'status': 'Completed',
                'profit_and_loss': {
                    'net_income': statements['profit_and_loss']['net_income']['formatted']
                },
                'balance_sheet': {
                    'total_assets': statements['balance_sheet']['assets']['formatted'],
                    'balanced': statements['balance_sheet']['balanced']
                }
            }
            
            print("\n✓ Financial statements generated successfully")
            return statements
            
        except Exception as e:
            print(f"\n✗ Financial statement generation failed: {e}")
            self.results['steps']['financial_statements'] = {
                'status': 'Failed',
                'error': str(e)
            }
            return {}
    
    def run_complete_process(self):
        """
        Run the complete month-end close process.
        """
        print("\n" + "="*60)
        print("AUTONOMOUS MONTH-END CLOSE PROCESS")
        print("="*60)
        print(f"Started at: {self.results['process_start']}")
        
        # Step 1: Reconciliation
        self.step_1_reconciliation()
        
        # Step 2: Accruals
        self.step_2_accruals()
        
        # Step 3: Financial Statements
        self.step_3_financial_statements()
        
        # Mark process as complete
        self.results['process_end'] = datetime.now().isoformat()
        self.results['status'] = 'Completed'
        
        # Save final results
        self.save_results()
        
        # Print summary
        self.print_summary()
    
    def save_results(self):
        """
        Save the complete process results to JSON file.
        """
        results_file = f'{self.output_dir}/month_end_close_results.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nComplete results saved to: {results_file}")
    
    def print_summary(self):
        """
        Print a summary of the month-end close process.
        """
        print("\n" + "="*60)
        print("MONTH-END CLOSE SUMMARY")
        print("="*60)
        
        for step_name, step_data in self.results['steps'].items():
            status = step_data.get('status', 'Unknown')
            status_symbol = "✓" if status == "Completed" else "✗"
            print(f"\n{status_symbol} {step_name.upper()}: {status}")
            
            if status == "Completed" and 'summary' in step_data:
                summary = step_data['summary']
                if isinstance(summary, dict):
                    for key, value in list(summary.items())[:5]:  # Show first 5 items
                        print(f"  - {key}: {value}")
        
        print(f"\nProcess Status: {self.results['status']}")
        print(f"Started: {self.results['process_start']}")
        print(f"Ended: {self.results.get('process_end', 'N/A')}")
        print("\nAll output files are available in the 'output' directory.")
        print("Review the results in the approval dashboard: frontend/dashboard.html")
        print("="*60 + "\n")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main entry point for the month-end close process.
    """
    process = MonthEndCloseProcess()
    process.run_complete_process()


if __name__ == '__main__':
    main()
