"""
Financial Statement Preparation Module for Autonomous Month-End Close Process
Generates Profit & Loss, Balance Sheet, and Cash Flow statements from transaction data
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict
from utils import read_csv_file, safe_float, format_currency


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


def main():
    """
    Main function to demonstrate financial statement generation.
    """
    print("=== Financial Statement Generation Module ===\n")
    
    generator = FinancialStatementGenerator('sample_data/transactions.csv')
    
    print("Generating financial statements...")
    statements = generator.export_statements('output/financial_statements.json')
    
    # Display summary
    print("\n--- Financial Statements Summary ---")
    print(f"\nProfit & Loss:")
    print(f"  Revenue: {statements['profit_and_loss']['revenue']['formatted']}")
    print(f"  Expenses: {statements['profit_and_loss']['operating_expenses']['formatted']}")
    print(f"  Net Income: {statements['profit_and_loss']['net_income']['formatted']}")
    
    print(f"\nBalance Sheet:")
    print(f"  Assets: {statements['balance_sheet']['assets']['formatted']}")
    print(f"  Liabilities: {statements['balance_sheet']['liabilities']['formatted']}")
    print(f"  Equity: {statements['balance_sheet']['equity']['formatted']}")
    print(f"  Balanced: {statements['balance_sheet']['balanced']}")
    
    print(f"\nCash Flow:")
    print(f"  Operating: {statements['cash_flow']['operating_activities']['formatted']}")
    print(f"  Investing: {statements['cash_flow']['investing_activities']['formatted']}")
    print(f"  Financing: {statements['cash_flow']['financing_activities']['formatted']}")
    print(f"  Net Change: {statements['cash_flow']['net_cash_change']['formatted']}")
    
    print("\n✓ Financial statements generation complete!")


if __name__ == '__main__':
    main()
