"""
Unit tests for UK Tax Computations Module
Tests user/business associations, CSV import validation, and tax computations
"""

import unittest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from uk_tax_computations import UKTaxComputations


class TestUKTaxComputations(unittest.TestCase):
    """Test cases for UK Tax Computations functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tax_comp = UKTaxComputations()
        self.tax_comp.add_user('user1', 'John Smith')
        self.tax_comp.add_user('user2', 'Jane Doe')
        self.tax_comp.add_business('biz1', 'Tech Solutions Ltd')
        self.tax_comp.add_business('biz2', 'Consulting Services Ltd')
    
    def test_add_user(self):
        """Test adding users to the system."""
        self.assertEqual(len(self.tax_comp.get_all_users()), 2)
        self.assertEqual(self.tax_comp.users['user1']['name'], 'John Smith')
        self.assertEqual(self.tax_comp.users['user2']['name'], 'Jane Doe')
    
    def test_add_business(self):
        """Test adding businesses to the system."""
        self.assertEqual(len(self.tax_comp.get_all_businesses()), 2)
        self.assertEqual(self.tax_comp.businesses['biz1']['name'], 'Tech Solutions Ltd')
        self.assertEqual(self.tax_comp.businesses['biz2']['name'], 'Consulting Services Ltd')
    
    def test_user_business_association(self):
        """Test that transactions are correctly associated with user and business."""
        csv_data = """date,description,amount,reference,category
2024-12-01,Payment,1000.00,REF001,Income
2024-12-05,Expense,-500.00,REF002,Expense"""
        
        result = self.tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')
        self.assertTrue(result['success'])
        self.assertEqual(result['imported_count'], 2)
        
        # Verify transactions are associated correctly
        transactions = self.tax_comp.get_transactions('user1', 'biz1')
        self.assertEqual(len(transactions), 2)
        for tx in transactions:
            self.assertEqual(tx['user_id'], 'user1')
            self.assertEqual(tx['business_id'], 'biz1')
    
    def test_multiple_user_business_combinations(self):
        """Test handling multiple user-business combinations."""
        csv1 = """date,description,amount
2024-12-01,Income,1000.00"""
        csv2 = """date,description,amount
2024-12-02,Income,2000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv1, 'user1', 'biz1')
        self.tax_comp.import_transactions_from_csv(csv2, 'user2', 'biz2')
        
        # Verify separate associations
        tx_user1_biz1 = self.tax_comp.get_transactions('user1', 'biz1')
        tx_user2_biz2 = self.tax_comp.get_transactions('user2', 'biz2')
        
        self.assertEqual(len(tx_user1_biz1), 1)
        self.assertEqual(len(tx_user2_biz2), 1)
        self.assertEqual(tx_user1_biz1[0]['amount'], 1000.00)
        self.assertEqual(tx_user2_biz2[0]['amount'], 2000.00)
    
    def test_csv_validation_valid(self):
        """Test CSV validation with valid data."""
        valid_csv = """date,description,amount
2024-12-01,Payment,1000.00
2024-12-05,Expense,-500.00"""
        
        result = self.tax_comp.validate_csv_data(valid_csv)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
        self.assertEqual(result['row_count'], 2)
    
    def test_csv_validation_missing_headers(self):
        """Test CSV validation with missing required headers."""
        invalid_csv = """date,description
2024-12-01,Payment"""
        
        result = self.tax_comp.validate_csv_data(invalid_csv)
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
        self.assertIn('amount', result['errors'][0].lower())
    
    def test_csv_validation_invalid_amount(self):
        """Test CSV validation with invalid amount values."""
        invalid_csv = """date,description,amount
2024-12-01,Payment,invalid
2024-12-05,Expense,-500.00"""
        
        result = self.tax_comp.validate_csv_data(invalid_csv)
        self.assertFalse(result['valid'])
        self.assertTrue(any('amount' in error.lower() for error in result['errors']))
    
    def test_csv_validation_empty_required_field(self):
        """Test CSV validation with empty required fields."""
        invalid_csv = """date,description,amount
2024-12-01,,1000.00"""
        
        result = self.tax_comp.validate_csv_data(invalid_csv)
        self.assertFalse(result['valid'])
        self.assertTrue(any('empty' in error.lower() for error in result['errors']))
    
    def test_csv_validation_insufficient_rows(self):
        """Test CSV validation with insufficient data rows."""
        invalid_csv = """date,description,amount"""
        
        result = self.tax_comp.validate_csv_data(invalid_csv)
        self.assertFalse(result['valid'])
        self.assertTrue(any('header' in error.lower() for error in result['errors']))
    
    def test_import_transactions_success(self):
        """Test successful transaction import."""
        csv_data = """date,description,amount,reference
2024-12-01,Payment,1000.00,REF001
2024-12-05,Expense,-500.00,REF002"""
        
        result = self.tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')
        self.assertTrue(result['success'])
        self.assertEqual(result['imported_count'], 2)
        self.assertIn('transactions', result)
    
    def test_import_transactions_invalid_csv(self):
        """Test transaction import with invalid CSV."""
        invalid_csv = """date,description
2024-12-01,Payment"""
        
        result = self.tax_comp.import_transactions_from_csv(invalid_csv, 'user1', 'biz1')
        self.assertFalse(result['success'])
        self.assertIn('validation', result)
    
    def test_compute_tax_with_transactions(self):
        """Test tax computation with imported transactions."""
        csv_data = """date,description,amount
2024-12-01,Income,50000.00
2024-12-05,Income,30000.00
2024-12-10,Expense,-20000.00
2024-12-15,Expense,-10000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')
        result = self.tax_comp.compute_tax_from_transactions('user1', 'biz1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['total_income'], 80000.00)
        self.assertEqual(result['total_expenses'], 30000.00)
        self.assertEqual(result['net_profit'], 50000.00)
        self.assertGreater(result['corporation_tax'], 0)
    
    def test_compute_tax_small_profits_rate(self):
        """Test tax computation using small profits rate (19%)."""
        csv_data = """date,description,amount
2024-12-01,Income,40000.00
2024-12-05,Expense,-10000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')
        result = self.tax_comp.compute_tax_from_transactions('user1', 'biz1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['net_profit'], 30000.00)
        self.assertEqual(result['tax_rate'], 0.19)
        self.assertEqual(result['corporation_tax'], 30000.00 * 0.19)
    
    def test_compute_tax_main_rate(self):
        """Test tax computation using main rate (25%)."""
        csv_data = """date,description,amount
2024-12-01,Income,300000.00
2024-12-05,Expense,-20000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')
        result = self.tax_comp.compute_tax_from_transactions('user1', 'biz1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['net_profit'], 280000.00)
        self.assertEqual(result['tax_rate'], 0.25)
        self.assertEqual(result['corporation_tax'], 280000.00 * 0.25)
    
    def test_compute_tax_marginal_relief(self):
        """Test tax computation with marginal relief."""
        csv_data = """date,description,amount
2024-12-01,Income,150000.00
2024-12-05,Expense,-50000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')
        result = self.tax_comp.compute_tax_from_transactions('user1', 'biz1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['net_profit'], 100000.00)
        # Marginal relief should apply
        expected_relief = (250000 - 100000) * 0.015
        expected_tax = (100000 * 0.25) - expected_relief
        self.assertAlmostEqual(result['corporation_tax'], expected_tax, places=2)
    
    def test_compute_tax_no_transactions(self):
        """Test tax computation with no transactions."""
        result = self.tax_comp.compute_tax_from_transactions('user1', 'biz1')
        
        self.assertFalse(result['success'])
        self.assertIn('No transactions', result['message'])
    
    def test_vat_computation(self):
        """Test VAT computation from transactions."""
        csv_data = """date,description,amount
2024-12-01,Sales,10000.00
2024-12-05,Purchase,-5000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')
        result = self.tax_comp.compute_tax_from_transactions('user1', 'biz1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['vat_on_sales'], 10000.00 * 0.20)
        self.assertEqual(result['vat_on_purchases'], 5000.00 * 0.20)
        self.assertEqual(result['vat_due'], (10000.00 * 0.20) - (5000.00 * 0.20))
    
    def test_transaction_filtering(self):
        """Test filtering transactions by user and business."""
        csv1 = """date,description,amount
2024-12-01,Income1,1000.00"""
        csv2 = """date,description,amount
2024-12-02,Income2,2000.00"""
        csv3 = """date,description,amount
2024-12-03,Income3,3000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv1, 'user1', 'biz1')
        self.tax_comp.import_transactions_from_csv(csv2, 'user1', 'biz2')
        self.tax_comp.import_transactions_from_csv(csv3, 'user2', 'biz1')
        
        # Filter by user only
        user1_txs = self.tax_comp.get_transactions(user_id='user1')
        self.assertEqual(len(user1_txs), 2)
        
        # Filter by business only
        biz1_txs = self.tax_comp.get_transactions(business_id='biz1')
        self.assertEqual(len(biz1_txs), 2)
        
        # Filter by both
        user1_biz1_txs = self.tax_comp.get_transactions('user1', 'biz1')
        self.assertEqual(len(user1_biz1_txs), 1)
        self.assertEqual(user1_biz1_txs[0]['amount'], 1000.00)
    
    def test_computation_per_user_business(self):
        """Test that computations are correctly isolated per user-business."""
        csv1 = """date,description,amount
2024-12-01,Income,10000.00
2024-12-05,Expense,-3000.00"""
        csv2 = """date,description,amount
2024-12-01,Income,20000.00
2024-12-05,Expense,-5000.00"""
        
        self.tax_comp.import_transactions_from_csv(csv1, 'user1', 'biz1')
        self.tax_comp.import_transactions_from_csv(csv2, 'user2', 'biz2')
        
        result1 = self.tax_comp.compute_tax_from_transactions('user1', 'biz1')
        result2 = self.tax_comp.compute_tax_from_transactions('user2', 'biz2')
        
        self.assertEqual(result1['net_profit'], 7000.00)
        self.assertEqual(result2['net_profit'], 15000.00)
        self.assertNotEqual(result1['corporation_tax'], result2['corporation_tax'])


if __name__ == '__main__':
    unittest.main()
