#!/usr/bin/env python3
"""
Test script for Tax Optimization API
Tests all endpoints without starting a persistent server
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.tax_optimization_engine import TaxOptimizationEngine
import json

def test_director_optimization():
    """Test director optimization"""
    print("Testing Director Optimization...")
    engine = TaxOptimizationEngine()
    
    result = engine.optimize_for_director(
        salary=30000,
        dividends=20000,
        company_profit=60000,
        pension_contribution=0
    )
    
    print(f"✓ Current total tax: £{result['current_position']['total_tax']:,.2f}")
    print(f"✓ Optimal total tax: £{result['optimal_position']['total_tax']:,.2f}")
    print(f"✓ Potential saving: £{result['potential_saving']:,.2f}")
    print(f"✓ Recommendations: {len(result['recommendations'])}")
    print()

def test_sole_trader_optimization():
    """Test sole trader optimization"""
    print("Testing Sole Trader Optimization...")
    engine = TaxOptimizationEngine()
    
    result = engine.optimize_for_sole_trader(
        trading_income=50000,
        allowable_expenses=8000,
        pension_contribution=3000,
        capital_allowances=2000
    )
    
    print(f"✓ Trading income: £{result['income_analysis']['trading_income']:,.2f}")
    print(f"✓ Taxable profit: £{result['income_analysis']['taxable_profit']:,.2f}")
    print(f"✓ Method used: {result['income_analysis']['method_used']}")
    print(f"✓ Recommendations: {len(result['recommendations'])}")
    print()

def test_company_owner_optimization():
    """Test company owner optimization"""
    print("Testing Company Owner Optimization...")
    engine = TaxOptimizationEngine()
    
    result = engine.optimize_for_company_owner(
        company_profit=100000,
        salary=30000,
        dividends=40000,
        r_and_d_expenditure=15000,
        capital_investment=20000
    )
    
    print(f"✓ Company profit: £{result['company_analysis']['profit']:,.2f}")
    print(f"✓ Corporation tax: £{result['company_analysis']['corporation_tax']:,.2f}")
    print(f"✓ Total reliefs: £{result['reliefs_claimed']['total_relief']:,.2f}")
    print(f"✓ Recommendations: {len(result['recommendations'])}")
    print()

def test_landlord_optimization():
    """Test landlord optimization"""
    print("Testing Landlord Optimization...")
    engine = TaxOptimizationEngine()
    
    result = engine.optimize_for_landlord(
        rental_income=30000,
        mortgage_interest=8000,
        other_expenses=5000,
        is_furnished=True,
        number_of_properties=2
    )
    
    print(f"✓ Rental income: £{result['property_details']['rental_income']:,.2f}")
    print(f"✓ Taxable income: £{result['tax_calculation']['taxable_income']:,.2f}")
    print(f"✓ Method used: {result['tax_calculation']['method_used']}")
    print(f"✓ Incorporation recommended: {result['incorporation_analysis']['recommended']}")
    print(f"✓ Recommendations: {len(result['recommendations'])}")
    print()

if __name__ == '__main__':
    print("=" * 60)
    print("Tax Optimization Engine Tests")
    print("=" * 60)
    print()
    
    try:
        test_director_optimization()
        test_sole_trader_optimization()
        test_company_owner_optimization()
        test_landlord_optimization()
        
        print("=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
