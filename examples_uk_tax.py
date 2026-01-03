"""
UK Tax Calculator - Usage Examples

This file demonstrates various use cases for the UK Tax Calculator,
including PAYE, Self Assessment, and Corporation Tax calculations.
"""

from backend.uk_tax_calculator import (
    calculate_paye,
    calculate_self_assessment,
    calculate_corporate_tax,
    ValidationError
)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n{title}")
    print("-" * 80)


def example_paye_basic():
    """Example: Basic rate taxpayer"""
    print_subsection("Example 1: Basic Rate Taxpayer (£30,000)")
    
    result = calculate_paye(gross_income=30000)
    
    print(f"Gross Income:        £{result['gross_income']:>12,.2f}")
    print(f"Personal Allowance:  £{result['personal_allowance']:>12,.2f}")
    print(f"Taxable Income:      £{result['taxable_income']:>12,.2f}")
    print(f"\nTax (20% basic):     £{result['tax_breakdown']['basic_rate']:>12,.2f}")
    print(f"Total Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Net Income:          £{result['net_income']:>12,.2f}")
    print(f"Effective Rate:      {result['total_tax']/result['gross_income']*100:>11.2f}%")


def example_paye_higher():
    """Example: Higher rate taxpayer"""
    print_subsection("Example 2: Higher Rate Taxpayer (£75,000)")
    
    result = calculate_paye(gross_income=75000)
    
    print(f"Gross Income:        £{result['gross_income']:>12,.2f}")
    print(f"Personal Allowance:  £{result['personal_allowance']:>12,.2f}")
    print(f"Taxable Income:      £{result['taxable_income']:>12,.2f}")
    print(f"\nTax Breakdown:")
    print(f"  Basic Rate (20%):  £{result['tax_breakdown']['basic_rate']:>12,.2f}")
    print(f"  Higher Rate (40%): £{result['tax_breakdown']['higher_rate']:>12,.2f}")
    print(f"\nTotal Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Net Income:          £{result['net_income']:>12,.2f}")
    print(f"Effective Rate:      {result['total_tax']/result['gross_income']*100:>11.2f}%")


def example_paye_additional():
    """Example: Additional rate taxpayer"""
    print_subsection("Example 3: Additional Rate Taxpayer (£180,000)")
    
    result = calculate_paye(gross_income=180000)
    
    print(f"Gross Income:        £{result['gross_income']:>12,.2f}")
    print(f"Personal Allowance:  £{result['personal_allowance']:>12,.2f}")
    print(f"Taxable Income:      £{result['taxable_income']:>12,.2f}")
    print(f"\nTax Breakdown:")
    print(f"  Basic Rate (20%):  £{result['tax_breakdown']['basic_rate']:>12,.2f}")
    print(f"  Higher Rate (40%): £{result['tax_breakdown']['higher_rate']:>12,.2f}")
    print(f"  Additional (45%):  £{result['tax_breakdown']['additional_rate']:>12,.2f}")
    print(f"\nTotal Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Net Income:          £{result['net_income']:>12,.2f}")
    print(f"Effective Rate:      {result['total_tax']/result['gross_income']*100:>11.2f}%")


def example_paye_pension():
    """Example: With pension contributions"""
    print_subsection("Example 4: With Pension Contributions (£60,000 income, £8,000 pension)")
    
    result = calculate_paye(gross_income=60000, deductions=8000)
    result_no_pension = calculate_paye(gross_income=60000)
    
    print(f"Gross Income:        £{result['gross_income']:>12,.2f}")
    print(f"Pension Deduction:   £{result['deductions']:>12,.2f}")
    print(f"Personal Allowance:  £{result['personal_allowance']:>12,.2f}")
    print(f"Taxable Income:      £{result['taxable_income']:>12,.2f}")
    print(f"\nTax Breakdown:")
    print(f"  Basic Rate (20%):  £{result['tax_breakdown']['basic_rate']:>12,.2f}")
    print(f"  Higher Rate (40%): £{result['tax_breakdown']['higher_rate']:>12,.2f}")
    print(f"\nTotal Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Tax Saved by Pension: £{result_no_pension['total_tax'] - result['total_tax']:>11,.2f}")


def example_paye_tapered():
    """Example: Tapered personal allowance"""
    print_subsection("Example 5: Tapered Personal Allowance (£125,000)")
    
    result = calculate_paye(gross_income=125000)
    
    print(f"Gross Income:        £{result['gross_income']:>12,.2f}")
    print(f"Personal Allowance:  £{result['personal_allowance']:>12,.2f}")
    print(f"  (Tapered: £1 reduction for every £2 over £100,000)")
    print(f"Taxable Income:      £{result['taxable_income']:>12,.2f}")
    print(f"\nTotal Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Net Income:          £{result['net_income']:>12,.2f}")


def example_sa_employment_property():
    """Example: Employment + rental income"""
    print_subsection("Example 6: Employment + Rental Income")
    
    income_sources = [
        {'type': 'employment', 'amount': 40000},
        {'type': 'property', 'amount': 15000}
    ]
    deductions = {'pension': 3000}
    
    result = calculate_self_assessment(income_sources, deductions)
    
    print("Income Sources:")
    print(f"  Employment:        £{result['income_breakdown']['employment']:>12,.2f}")
    print(f"  Property:          £{result['income_breakdown']['property']:>12,.2f}")
    print(f"Total Income:        £{result['total_income']:>12,.2f}")
    print(f"\nDeductions:")
    print(f"  Pension:           £{result['deductions_breakdown']['pension']:>12,.2f}")
    print(f"Total Deductions:    £{result['total_deductions']:>12,.2f}")
    print(f"\nTaxable Income:      £{result['taxable_income']:>12,.2f}")
    print(f"Total Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Net Income:          £{result['net_income']:>12,.2f}")


def example_sa_multiple_sources():
    """Example: Multiple income sources"""
    print_subsection("Example 7: Multiple Income Sources (Self-Employed + Property + Investment)")
    
    income_sources = [
        {'type': 'self_employment', 'amount': 45000},
        {'type': 'property', 'amount': 18000},
        {'type': 'investment', 'amount': 8000}
    ]
    deductions = {
        'pension': 5000,
        'charity': 1200,
        'trading_losses': 2000
    }
    
    result = calculate_self_assessment(income_sources, deductions)
    
    print("Income Sources:")
    print(f"  Self-Employment:   £{result['income_breakdown']['self_employment']:>12,.2f}")
    print(f"  Property:          £{result['income_breakdown']['property']:>12,.2f}")
    print(f"  Investment:        £{result['income_breakdown']['investment']:>12,.2f}")
    print(f"Total Income:        £{result['total_income']:>12,.2f}")
    print(f"\nDeductions:")
    print(f"  Pension:           £{result['deductions_breakdown']['pension']:>12,.2f}")
    print(f"  Charity:           £{result['deductions_breakdown']['charity']:>12,.2f}")
    print(f"  Trading Losses:    £{result['deductions_breakdown']['trading_losses']:>12,.2f}")
    print(f"Total Deductions:    £{result['total_deductions']:>12,.2f}")
    print(f"\nTaxable Income:      £{result['taxable_income']:>12,.2f}")
    print(f"Total Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Net Income:          £{result['net_income']:>12,.2f}")


def example_sa_portfolio():
    """Example: Portfolio income earner"""
    print_subsection("Example 8: Portfolio Income (Multiple Properties + Investments)")
    
    income_sources = [
        {'type': 'employment', 'amount': 50000},
        {'type': 'property', 'amount': 20000},
        {'type': 'property', 'amount': 15000},
        {'type': 'investment', 'amount': 10000}
    ]
    deductions = {'pension': 6000, 'charity': 2000}
    
    result = calculate_self_assessment(income_sources, deductions)
    
    print(f"Total Income:        £{result['total_income']:>12,.2f}")
    print(f"  Employment:        £{result['income_breakdown']['employment']:>12,.2f}")
    print(f"  Property:          £{result['income_breakdown']['property']:>12,.2f}")
    print(f"  Investment:        £{result['income_breakdown']['investment']:>12,.2f}")
    print(f"\nTotal Tax:           £{result['total_tax']:>12,.2f}")
    print(f"Net Income:          £{result['net_income']:>12,.2f}")


def example_corp_small():
    """Example: Small company (19% rate)"""
    print_subsection("Example 9: Small Company (Profit < £50,000)")
    
    result = calculate_corporate_tax(
        gross_profit=80000,
        allowable_expenses=35000
    )
    
    print(f"Gross Profit:        £{result['gross_profit']:>12,.2f}")
    print(f"Allowable Expenses:  £{result['allowable_expenses']:>12,.2f}")
    print(f"Adjusted Profit:     £{result['adjusted_profit']:>12,.2f}")
    print(f"\nTaxable Profit:      £{result['taxable_profit']:>12,.2f}")
    print(f"Tax Rate:            {result['applicable_rate']*100:>11.0f}%")
    print(f"Corporation Tax:     £{result['corporation_tax']:>12,.2f}")
    print(f"Effective Rate:      {result['effective_rate']:>11.2f}%")
    print(f"Net Profit:          £{result['net_profit']:>12,.2f}")


def example_corp_large():
    """Example: Large company (25% rate)"""
    print_subsection("Example 10: Large Company (Profit > £250,000)")
    
    result = calculate_corporate_tax(
        gross_profit=600000,
        allowable_expenses=250000
    )
    
    print(f"Gross Profit:        £{result['gross_profit']:>12,.2f}")
    print(f"Allowable Expenses:  £{result['allowable_expenses']:>12,.2f}")
    print(f"Adjusted Profit:     £{result['adjusted_profit']:>12,.2f}")
    print(f"\nTaxable Profit:      £{result['taxable_profit']:>12,.2f}")
    print(f"Tax Rate:            {result['applicable_rate']*100:>11.0f}%")
    print(f"Corporation Tax:     £{result['corporation_tax']:>12,.2f}")
    print(f"Effective Rate:      {result['effective_rate']:>11.2f}%")
    print(f"Net Profit:          £{result['net_profit']:>12,.2f}")


def example_corp_marginal():
    """Example: Marginal relief band"""
    print_subsection("Example 11: Marginal Relief (£50k < Profit < £250k)")
    
    result = calculate_corporate_tax(
        gross_profit=200000,
        allowable_expenses=50000
    )
    
    print(f"Gross Profit:        £{result['gross_profit']:>12,.2f}")
    print(f"Allowable Expenses:  £{result['allowable_expenses']:>12,.2f}")
    print(f"Taxable Profit:      £{result['taxable_profit']:>12,.2f}")
    print(f"\nStandard Rate:       {result['applicable_rate']*100:>11.0f}%")
    print(f"Marginal Relief:     £{result['marginal_relief']:>12,.2f}")
    print(f"Corporation Tax:     £{result['corporation_tax']:>12,.2f}")
    print(f"Effective Rate:      {result['effective_rate']:>11.2f}%")
    print(f"\n  (Marginal relief reduces effective rate below 25%)")


def example_corp_rd_sme():
    """Example: SME with R&D"""
    print_subsection("Example 12: SME with R&D Tax Credits")
    
    result = calculate_corporate_tax(
        gross_profit=400000,
        allowable_expenses=100000,
        rd_expenditure=50000,
        is_sme=True
    )
    
    print(f"Gross Profit:        £{result['gross_profit']:>12,.2f}")
    print(f"Allowable Expenses:  £{result['allowable_expenses']:>12,.2f}")
    print(f"Adjusted Profit:     £{result['adjusted_profit']:>12,.2f}")
    print(f"\nR&D Expenditure:     £{result['rd_expenditure']:>12,.2f}")
    print(f"R&D Tax Credit (86%):£{result['rd_tax_credit']:>12,.2f}")
    print(f"\nTaxable Profit:      £{result['taxable_profit']:>12,.2f}")
    print(f"Corporation Tax:     £{result['corporation_tax']:>12,.2f}")
    print(f"Net Profit:          £{result['net_profit']:>12,.2f}")
    print(f"\n  (R&D credit significantly reduces taxable profit)")


def example_corp_rd_large():
    """Example: Large company with R&D"""
    print_subsection("Example 13: Large Company with R&D")
    
    result = calculate_corporate_tax(
        gross_profit=1000000,
        allowable_expenses=300000,
        rd_expenditure=100000,
        is_sme=False
    )
    
    print(f"Gross Profit:        £{result['gross_profit']:>12,.2f}")
    print(f"Allowable Expenses:  £{result['allowable_expenses']:>12,.2f}")
    print(f"\nR&D Expenditure:     £{result['rd_expenditure']:>12,.2f}")
    print(f"R&D Tax Credit (13%):£{result['rd_tax_credit']:>12,.2f}")
    print(f"\nTaxable Profit:      £{result['taxable_profit']:>12,.2f}")
    print(f"Corporation Tax:     £{result['corporation_tax']:>12,.2f}")
    print(f"Net Profit:          £{result['net_profit']:>12,.2f}")


def example_corp_losses():
    """Example: Loss carry-forward"""
    print_subsection("Example 14: Corporation Tax with Loss Carry-Forward")
    
    result = calculate_corporate_tax(
        gross_profit=200000,
        allowable_expenses=40000,
        losses_brought_forward=50000
    )
    
    print(f"Gross Profit:        £{result['gross_profit']:>12,.2f}")
    print(f"Allowable Expenses:  £{result['allowable_expenses']:>12,.2f}")
    print(f"Adjusted Profit:     £{result['adjusted_profit']:>12,.2f}")
    print(f"\nLosses B/F:          £{result['losses_brought_forward']:>12,.2f}")
    print(f"Taxable Profit:      £{result['taxable_profit']:>12,.2f}")
    print(f"\nCorporation Tax:     £{result['corporation_tax']:>12,.2f}")
    print(f"Net Profit:          £{result['net_profit']:>12,.2f}")
    print(f"\n  (Previous losses reduce current year's taxable profit)")


def example_validation():
    """Example: Input validation"""
    print_subsection("Example 15: Input Validation Examples")
    
    print("\nTest 1: Negative income")
    try:
        calculate_paye(gross_income=-5000)
        print("  ✗ Should have raised error")
    except ValidationError as e:
        print(f"  ✓ Error caught: {e}")
    
    print("\nTest 2: Excessive deductions")
    try:
        calculate_paye(gross_income=50000, deductions=60000)
        print("  ✗ Should have raised error")
    except ValidationError as e:
        print(f"  ✓ Error caught: {e}")
    
    print("\nTest 3: Empty income sources")
    try:
        calculate_self_assessment([])
        print("  ✗ Should have raised error")
    except ValidationError as e:
        print(f"  ✓ Error caught: {e}")
    
    print("\nTest 4: Invalid deduction type")
    try:
        calculate_self_assessment(
            [{'type': 'employment', 'amount': 50000}],
            {'invalid_type': 1000}
        )
        print("  ✗ Should have raised error")
    except ValidationError as e:
        print(f"  ✓ Error caught: {e}")
    
    print("\n  All validation tests passed!")


def example_comparison():
    """Example: Compare different scenarios"""
    print_subsection("Example 16: Comparing Tax Scenarios")
    
    scenarios = [
        {"name": "Basic earner", "income": 25000},
        {"name": "Mid earner", "income": 40000},
        {"name": "Higher earner", "income": 75000},
        {"name": "High earner", "income": 150000}
    ]
    
    print(f"\n{'Scenario':<20} {'Income':>12} {'Tax':>12} {'Net':>12} {'Effective Rate':>15}")
    print("-" * 80)
    
    for scenario in scenarios:
        result = calculate_paye(scenario['income'])
        eff_rate = (result['total_tax'] / result['gross_income'] * 100) if result['gross_income'] > 0 else 0
        print(f"{scenario['name']:<20} £{result['gross_income']:>10,.0f} "
              f"£{result['total_tax']:>10,.2f} £{result['net_income']:>10,.0f} "
              f"{eff_rate:>13.2f}%")


def main():
    """Run all examples"""
    print_section("UK TAX CALCULATOR - COMPREHENSIVE USAGE EXAMPLES")
    
    # PAYE Examples
    print_section("PAYE (PAY AS YOU EARN) EXAMPLES")
    example_paye_basic()
    example_paye_higher()
    example_paye_additional()
    example_paye_pension()
    example_paye_tapered()
    
    # Self Assessment Examples
    print_section("SELF ASSESSMENT EXAMPLES")
    example_sa_employment_property()
    example_sa_multiple_sources()
    example_sa_portfolio()
    
    # Corporation Tax Examples
    print_section("CORPORATION TAX EXAMPLES")
    example_corp_small()
    example_corp_large()
    example_corp_marginal()
    example_corp_rd_sme()
    example_corp_rd_large()
    example_corp_losses()
    
    # Additional Examples
    print_section("VALIDATION AND COMPARISON EXAMPLES")
    example_validation()
    example_comparison()
    
    print("\n" + "=" * 80)
    print(" All examples completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
