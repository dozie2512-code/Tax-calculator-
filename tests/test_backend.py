"""
Unit Tests for Tax Calculator Backend Modules

Tests cover:
- Xero API integration
- Tax optimization logic
- HMRC rules calculations

Run: python tests/test_backend.py
"""

import unittest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from xero_api import XeroAPIClient, DataSyncManager
from tax_optimizer import TaxOptimizer, TaxRules, AllowableExpenses


class TestXeroAPI(unittest.TestCase):
    """Test cases for Xero API integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = XeroAPIClient()
    
    def test_authentication(self):
        """Test Xero authentication"""
        result = self.client.authenticate()
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('message', result)
    
    def test_fetch_invoices(self):
        """Test fetching invoices"""
        # Authenticate first
        self.client.authenticate()
        
        result = self.client.fetch_invoices()
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('data', result)
        
        if result['success']:
            self.assertIsInstance(result['data'], list)
            self.assertGreater(len(result['data']), 0)
    
    def test_fetch_expenses(self):
        """Test fetching expenses"""
        self.client.authenticate()
        
        result = self.client.fetch_expenses()
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('data', result)
        
        if result['success']:
            self.assertIsInstance(result['data'], list)
    
    def test_fetch_accounts(self):
        """Test fetching chart of accounts"""
        self.client.authenticate()
        
        result = self.client.fetch_accounts()
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('data', result)
    
    def test_sync_data(self):
        """Test data synchronization"""
        self.client.authenticate()
        
        result = self.client.sync_data(['invoices', 'expenses'])
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('results', result)
        self.assertIn('invoices', result['results'])
        self.assertIn('expenses', result['results'])


class TestDataSyncManager(unittest.TestCase):
    """Test cases for Data Sync Manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = XeroAPIClient()
        self.sync_manager = DataSyncManager(self.client)
    
    def test_sync_all(self):
        """Test syncing all data types"""
        self.client.authenticate()
        
        result = self.sync_manager.sync_all(save_to_file=False)
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('timestamp', result)
        self.assertIn('results', result)


class TestTaxRules(unittest.TestCase):
    """Test cases for Tax Rules"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.rules = TaxRules()
    
    def test_tax_rules_values(self):
        """Test tax rules have correct values"""
        # Personal allowance
        self.assertEqual(self.rules.personal_allowance, 12570)
        
        # Tax rates
        self.assertEqual(self.rules.basic_rate, 0.20)
        self.assertEqual(self.rules.higher_rate, 0.40)
        self.assertEqual(self.rules.additional_rate, 0.45)
        
        # Thresholds
        self.assertEqual(self.rules.basic_rate_limit, 50270)
        self.assertEqual(self.rules.higher_rate_limit, 125140)
        
        # Corporation tax
        self.assertEqual(self.rules.corporation_small_rate, 0.19)
        self.assertEqual(self.rules.corporation_main_rate, 0.25)


class TestTaxOptimizer(unittest.TestCase):
    """Test cases for Tax Optimizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.optimizer = TaxOptimizer()
    
    def test_calculate_personal_allowance_below_threshold(self):
        """Test personal allowance calculation below taper threshold"""
        allowance = self.optimizer.calculate_personal_allowance(50000)
        self.assertEqual(allowance, 12570)
    
    def test_calculate_personal_allowance_at_threshold(self):
        """Test personal allowance at taper threshold"""
        allowance = self.optimizer.calculate_personal_allowance(100000)
        self.assertEqual(allowance, 12570)
    
    def test_calculate_personal_allowance_above_threshold(self):
        """Test personal allowance tapering"""
        # At £110,000, should reduce by £5,000 (half of £10,000 excess)
        allowance = self.optimizer.calculate_personal_allowance(110000)
        self.assertEqual(allowance, 7570)  # 12570 - 5000
    
    def test_calculate_personal_allowance_fully_tapered(self):
        """Test personal allowance fully tapered out"""
        # At £125,140 or above, allowance should be zero
        allowance = self.optimizer.calculate_personal_allowance(125140)
        self.assertEqual(allowance, 0)
    
    def test_optimize_sole_trader_basic(self):
        """Test sole trader optimization"""
        result = self.optimizer.optimize_sole_trader(
            income=60000,
            expenses=10000
        )
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['entity_type'], 'Sole Trader')
        self.assertEqual(result['current_profit'], 50000)
        self.assertIn('suggestions', result)
        self.assertIn('allowable_expenses', result)
        self.assertIsInstance(result['suggestions'], list)
    
    def test_optimize_sole_trader_low_expenses(self):
        """Test sole trader with expenses below trading allowance"""
        result = self.optimizer.optimize_sole_trader(
            income=5000,
            expenses=500
        )
        
        # Should suggest using trading allowance
        suggestions = result['suggestions']
        self.assertGreater(len(suggestions), 0)
        
        # Check if trading allowance suggestion exists
        trading_allowance_suggested = any(
            'Trading Allowance' in s['title'] 
            for s in suggestions
        )
        self.assertTrue(trading_allowance_suggested)
    
    def test_optimize_company_basic(self):
        """Test company optimization"""
        result = self.optimizer.optimize_company(
            profit=100000,
            salary=12570,
            dividends=40000
        )
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['entity_type'], 'Limited Company')
        self.assertEqual(result['company_profit'], 100000)
        self.assertIn('suggestions', result)
        self.assertIsInstance(result['suggestions'], list)
    
    def test_optimize_company_low_salary(self):
        """Test company with salary below optimal"""
        result = self.optimizer.optimize_company(
            profit=100000,
            salary=8000,
            dividends=50000
        )
        
        # Should suggest increasing salary
        suggestions = result['suggestions']
        salary_optimization = any(
            'Salary' in s['title']
            for s in suggestions
        )
        self.assertTrue(salary_optimization)
    
    def test_optimize_landlord_basic(self):
        """Test landlord optimization"""
        result = self.optimizer.optimize_landlord(
            rental_income=20000,
            expenses=5000,
            mortgage_interest=3000
        )
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['entity_type'], 'Landlord')
        self.assertEqual(result['rental_income'], 20000)
        self.assertIn('suggestions', result)
        self.assertIsInstance(result['suggestions'], list)
    
    def test_optimize_employee_basic(self):
        """Test employee optimization"""
        result = self.optimizer.optimize_employee(
            salary=45000,
            bonus=5000,
            other_income=2000
        )
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['entity_type'], 'Employee')
        self.assertEqual(result['total_income'], 52000)
        self.assertIn('suggestions', result)
        self.assertIsInstance(result['suggestions'], list)
    
    def test_optimize_employee_high_income(self):
        """Test employee with high income"""
        result = self.optimizer.optimize_employee(
            salary=110000,
            bonus=0,
            other_income=0
        )
        
        # Should suggest salary sacrifice due to high income
        suggestions = result['suggestions']
        self.assertGreater(len(suggestions), 0)
        
        # Should mention personal allowance tapering
        tapering_mentioned = any(
            'Allowance Tapering' in s['title'] or 'Salary Sacrifice' in s['title']
            for s in suggestions
        )
        self.assertTrue(tapering_mentioned)


class TestAllowableExpenses(unittest.TestCase):
    """Test cases for Allowable Expenses"""
    
    def test_sole_trader_expenses(self):
        """Test sole trader allowable expenses"""
        expenses = AllowableExpenses.get_sole_trader_expenses()
        
        self.assertIsInstance(expenses, list)
        self.assertGreater(len(expenses), 0)
        
        # Check structure of expense items
        for expense in expenses:
            self.assertIn('category', expense)
            self.assertIn('items', expense)
            self.assertIn('fully_deductible', expense)
            self.assertIn('notes', expense)
    
    def test_company_expenses(self):
        """Test company allowable expenses"""
        expenses = AllowableExpenses.get_company_expenses()
        
        self.assertIsInstance(expenses, list)
        self.assertGreater(len(expenses), 0)
        
        # Should include salaries
        categories = [e['category'] for e in expenses]
        self.assertIn('Salaries', categories)
    
    def test_landlord_expenses(self):
        """Test landlord allowable expenses"""
        expenses = AllowableExpenses.get_landlord_expenses()
        
        self.assertIsInstance(expenses, list)
        self.assertGreater(len(expenses), 0)
        
        # Should include maintenance and mortgage interest
        categories = [e['category'] for e in expenses]
        self.assertIn('Maintenance & Repairs', categories)
        self.assertIn('Mortgage Interest', categories)
    
    def test_employee_expenses(self):
        """Test employee allowable expenses"""
        expenses = AllowableExpenses.get_employee_expenses()
        
        self.assertIsInstance(expenses, list)
        self.assertGreater(len(expenses), 0)
        
        # Should include travel
        categories = [e['category'] for e in expenses]
        self.assertIn('Travel', categories)


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Tax Calculator Backend Tests")
    print("=" * 60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestXeroAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestDataSyncManager))
    suite.addTests(loader.loadTestsFromTestCase(TestTaxRules))
    suite.addTests(loader.loadTestsFromTestCase(TestTaxOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestAllowableExpenses))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
