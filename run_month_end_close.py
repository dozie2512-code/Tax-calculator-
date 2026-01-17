"""
Main Orchestration Script for Autonomous Month-End Close Process
Coordinates all modules: reconciliation, accruals, and financial statements
"""

import os
import sys
import json
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from reconciliation import AccountReconciliation
from accruals import AccrualCalculator
from financial_statements import FinancialStatementGenerator
from tax_sync import TaxDataSynchronizer


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
    
    def step_4_tax_synchronization(self) -> dict:
        """
        Step 4: Synchronize tax data from postings.
        
        Returns:
            Tax synchronization results
        """
        print("\n" + "="*60)
        print("STEP 4: TAX DATA SYNCHRONIZATION")
        print("="*60)
        
        try:
            synchronizer = TaxDataSynchronizer('sample_data/transactions.csv')
            sync_result = synchronizer.export_synchronized_data(f'{self.output_dir}/tax_synchronized_data.json')
            
            self.results['steps']['tax_synchronization'] = {
                'status': 'Completed',
                'summary': sync_result.get('summary', {}),
                'entities_synced': list(sync_result.get('entities', {}).keys())
            }
            
            print("\n✓ Tax data synchronization completed successfully")
            return sync_result
            
        except Exception as e:
            print(f"\n✗ Tax data synchronization failed: {e}")
            self.results['steps']['tax_synchronization'] = {
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
        
        # Step 4: Tax Data Synchronization
        self.step_4_tax_synchronization()
        
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


def main():
    """
    Main entry point for the month-end close process.
    """
    process = MonthEndCloseProcess()
    process.run_complete_process()


if __name__ == '__main__':
    main()
