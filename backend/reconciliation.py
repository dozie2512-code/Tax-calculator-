"""
Account Reconciliation Module for Autonomous Month-End Close Process
Handles reconciliation between general ledger and bank statements
"""

import json
from typing import List, Dict, Any, Tuple
from utils import read_csv_file, write_csv_file, safe_float, format_currency


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


def main():
    """
    Main function to demonstrate reconciliation functionality.
    """
    print("=== Account Reconciliation Module ===\n")
    
    # Initialize reconciliation
    reconciler = AccountReconciliation(
        'sample_data/general_ledger.csv',
        'sample_data/bank_statement.csv'
    )
    
    # Perform reconciliation
    print("Performing reconciliation...")
    summary = reconciler.reconcile()
    
    # Display summary
    print("\n--- Reconciliation Summary ---")
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Export results
    print("\nExporting results...")
    reconciler.export_results('output/reconciliation')
    
    print("\n✓ Reconciliation complete!")


if __name__ == '__main__':
    main()
