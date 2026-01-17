"""
Example usage of the Tax Optimization Engine

This script demonstrates how to use the refactored tax optimization
module for different user types with proper error handling.
"""

from backend.tax_optimization_engine import TaxOptimizationEngine
import json


def print_director_example():
    """Example: Company Director optimization."""
    print("\n" + "="*70)
    print("EXAMPLE 1: COMPANY DIRECTOR TAX OPTIMIZATION")
    print("="*70)
    
    engine = TaxOptimizationEngine()
    
    # Example data
    salary = 30_000
    dividends = 20_000
    company_profit = 60_000
    pension = 5_000
    
    print(f"\nCurrent situation:")
    print(f"  Salary: £{salary:,}")
    print(f"  Dividends: £{dividends:,}")
    print(f"  Company Profit: £{company_profit:,}")
    print(f"  Pension Contribution: £{pension:,}")
    
    # Get optimization recommendation
    result = engine.optimize_for_director(
        salary=salary,
        dividends=dividends,
        company_profit=company_profit,
        pension_contribution=pension
    )
    
    print(f"\nCurrent Position:")
    print(f"  Total Tax: £{result['current_position']['total_tax']:,.2f}")
    print(f"  Net Income: £{result['current_position']['net_income']:,.2f}")
    
    print(f"\nOptimal Position:")
    print(f"  Recommended Salary: £{result['optimal_position']['salary']:,.2f}")
    print(f"  Recommended Dividends: £{result['optimal_position']['dividends']:,.2f}")
    print(f"  Total Tax: £{result['optimal_position']['total_tax']:,.2f}")
    print(f"  Net Income: £{result['optimal_position']['net_income']:,.2f}")
    
    print(f"\n💰 Potential Annual Saving: £{result['potential_saving']:,.2f}")
    
    print(f"\nRecommended Strategies:")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"  {i}. {rec['strategy']}: {rec['description']}")


def print_sole_trader_example():
    """Example: Sole Trader optimization."""
    print("\n" + "="*70)
    print("EXAMPLE 2: SOLE TRADER TAX OPTIMIZATION")
    print("="*70)
    
    engine = TaxOptimizationEngine()
    
    # Example data
    trading_income = 75_000
    expenses = 15_000
    pension = 10_000
    capital = 5_000
    
    print(f"\nCurrent situation:")
    print(f"  Trading Income: £{trading_income:,}")
    print(f"  Allowable Expenses: £{expenses:,}")
    print(f"  Pension Contribution: £{pension:,}")
    print(f"  Capital Allowances: £{capital:,}")
    
    result = engine.optimize_for_sole_trader(
        trading_income=trading_income,
        allowable_expenses=expenses,
        pension_contribution=pension,
        capital_allowances=capital
    )
    
    print(f"\nIncome Analysis:")
    print(f"  Taxable Profit: £{result['income_analysis']['taxable_profit']:,.2f}")
    print(f"  Method Used: {result['income_analysis']['method_used']}")
    
    print(f"\nTax Position:")
    print(f"  Income Tax: £{result['tax_position']['income_tax']:,.2f}")
    print(f"  National Insurance: £{result['tax_position']['employee_ni']:,.2f}")
    print(f"  Total Deductions: £{result['tax_position']['total_employee_deductions']:,.2f}")
    print(f"  Net Income: £{result['tax_position']['net_income']:,.2f}")
    
    if result['pension_relief']:
        print(f"\nPension Relief:")
        print(f"  Total Relief: £{result['pension_relief']['total_relief']:,.2f}")
        print(f"  Effective Cost: £{result['pension_relief']['effective_contribution']:,.2f}")
    
    print(f"\nRecommended Strategies ({len(result['recommendations'])} total):")
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"  {i}. {rec['strategy']}: {rec['description']}")


def print_landlord_example():
    """Example: Landlord optimization."""
    print("\n" + "="*70)
    print("EXAMPLE 3: LANDLORD TAX OPTIMIZATION")
    print("="*70)
    
    engine = TaxOptimizationEngine()
    
    # Example data
    rental_income = 36_000
    mortgage_interest = 12_000
    other_expenses = 6_000
    properties = 4
    
    print(f"\nProperty Portfolio:")
    print(f"  Rental Income: £{rental_income:,}")
    print(f"  Mortgage Interest: £{mortgage_interest:,}")
    print(f"  Other Expenses: £{other_expenses:,}")
    print(f"  Number of Properties: {properties}")
    print(f"  Furnished: Yes")
    
    result = engine.optimize_for_landlord(
        rental_income=rental_income,
        mortgage_interest=mortgage_interest,
        other_expenses=other_expenses,
        is_furnished=True,
        number_of_properties=properties
    )
    
    print(f"\nTax Calculation:")
    print(f"  Method: {result['tax_calculation']['method_used']}")
    print(f"  Taxable Income: £{result['tax_calculation']['taxable_income']:,.2f}")
    print(f"  Income Tax: £{result['tax_calculation']['income_tax']:,.2f}")
    
    print(f"\nIncorporation Analysis:")
    print(f"  Current Tax (Personal): £{result['incorporation_analysis']['current_tax']:,.2f}")
    print(f"  Corp Tax if Incorporated: £{result['incorporation_analysis']['corporation_tax_if_incorporated']:,.2f}")
    print(f"  Potential Saving: £{result['incorporation_analysis']['potential_saving']:,.2f}")
    print(f"  Incorporation Recommended: {'✓ Yes' if result['incorporation_analysis']['recommended'] else '✗ No'}")
    
    print(f"\nTop Strategies ({len(result['recommendations'])} total):")
    for i, rec in enumerate(result['recommendations'][:4], 1):
        print(f"  {i}. {rec['strategy']}")


def demonstrate_error_handling():
    """Demonstrate error handling."""
    print("\n" + "="*70)
    print("EXAMPLE 4: ERROR HANDLING")
    print("="*70)
    
    engine = TaxOptimizationEngine()
    
    print("\n1. Testing negative salary (should fail):")
    try:
        engine.optimize_for_director(
            salary=-10000,
            dividends=20000,
            company_profit=50000
        )
        print("   ✗ Error: Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly caught error: {str(e)[:60]}...")
    
    print("\n2. Testing missing required field (should fail):")
    try:
        engine.optimize_for_sole_trader(trading_income=50000)
    except TypeError as e:
        print(f"   ✓ Correctly caught error: {str(e)[:60]}...")
    
    print("\n3. Testing invalid user type (should fail):")
    try:
        engine.comprehensive_tax_plan('employee', salary=30000)
    except ValueError as e:
        print(f"   ✓ Correctly caught error: {str(e)[:60]}...")
    
    print("\n4. Testing valid input (should succeed):")
    try:
        result = engine.optimize_for_director(
            salary=25000,
            dividends=15000,
            company_profit=50000
        )
        print(f"   ✓ Success! Potential saving: £{result['potential_saving']:,.2f}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("TAX OPTIMIZATION ENGINE - USAGE EXAMPLES")
    print("="*70)
    print("\nThis demonstrates the refactored tax optimization module with:")
    print("  • Modular design with reusable components")
    print("  • Comprehensive error handling")
    print("  • Named constants replacing hardcoded values")
    print("  • Improved documentation and comments")
    
    # Run examples
    print_director_example()
    print_sole_trader_example()
    print_landlord_example()
    demonstrate_error_handling()
    
    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
