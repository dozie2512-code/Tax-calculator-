"""
Sample Scenarios for UK Tax Calculator
Demonstrates realistic use cases for each user type
"""

from backend.uk_tax_calculator import UKTaxCalculator, TaxReliefs
from backend.tax_optimization import TaxOptimizationEngine
import json


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*80 + "\n")


def print_results(title, results):
    """Pretty print results."""
    print(f"\n{title}")
    print("-" * len(title))
    print(json.dumps(results, indent=2))


def scenario_1_company_director():
    """
    Scenario 1: Company Director
    Sarah runs a successful consulting company and takes both salary and dividends.
    She wants to optimize her tax position.
    """
    print_separator()
    print("SCENARIO 1: COMPANY DIRECTOR - Sarah's Consulting Business")
    print_separator()
    
    print("Background:")
    print("- Sarah owns a consulting company with £100,000 annual profit")
    print("- Currently pays herself £50,000 salary and £30,000 dividends")
    print("- Wants to minimize tax while maintaining good pension contributions")
    
    optimizer = TaxOptimizationEngine()
    
    # Current situation
    results = optimizer.optimize_for_director(
        salary=50000,
        dividends=30000,
        company_profit=100000,
        pension_contribution=0
    )
    
    print_results("Sarah's Tax Analysis", results)
    
    # Calculate potential savings
    saving = results['potential_saving']
    print(f"\n💰 Potential Annual Saving: £{saving:,.2f}")
    
    print("\nKey Recommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec['strategy']}")
        print(f"   → {rec['description']}")
        print(f"   💵 Saving: {rec['saving']}")


def scenario_2_sole_trader():
    """
    Scenario 2: Sole Trader
    James is a freelance web developer tracking his income and expenses.
    """
    print_separator()
    print("SCENARIO 2: SOLE TRADER - James the Freelance Developer")
    print_separator()
    
    print("Background:")
    print("- James earned £60,000 from freelance web development")
    print("- Claimed £12,000 in expenses (equipment, software, travel)")
    print("- Purchased £8,000 of new equipment (capital allowances)")
    print("- Wants to maximize deductions and plan pension contributions")
    
    optimizer = TaxOptimizationEngine()
    
    results = optimizer.optimize_for_sole_trader(
        trading_income=60000,
        allowable_expenses=12000,
        capital_allowances=8000,
        pension_contribution=5000
    )
    
    print_results("James's Tax Analysis", results)
    
    print("\nKey Recommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec['strategy']}")
        print(f"   → {rec['description']}")
        print(f"   💵 Saving: {rec['saving']}")


def scenario_3_company_owner():
    """
    Scenario 3: Company Owner with R&D
    TechStart Ltd develops innovative software and qualifies for R&D relief.
    """
    print_separator()
    print("SCENARIO 3: COMPANY OWNER - TechStart Ltd Software Development")
    print_separator()
    
    print("Background:")
    print("- TechStart Ltd has £200,000 taxable profit")
    print("- Spent £50,000 on qualifying R&D activities")
    print("- Invested £30,000 in new equipment")
    print("- Director takes £50,000 salary and £50,000 dividends")
    
    optimizer = TaxOptimizationEngine()
    
    results = optimizer.optimize_for_company_owner(
        company_profit=200000,
        salary=50000,
        dividends=50000,
        r_and_d_expenditure=50000,
        capital_investment=30000
    )
    
    print_results("TechStart Ltd Tax Analysis", results)
    
    total_relief = results['reliefs_claimed']['total_relief']
    print(f"\n💰 Total Tax Relief Claimed: £{total_relief:,.2f}")
    
    print("\nKey Recommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec['strategy']}")
        print(f"   → {rec['description']}")
        if isinstance(rec['saving'], (int, float)):
            print(f"   💵 Saving: £{rec['saving']:,.2f}")
        else:
            print(f"   💵 Saving: {rec['saving']}")


def scenario_4_landlord():
    """
    Scenario 4: Landlord with Multiple Properties
    Emma owns 3 rental properties and is considering incorporation.
    """
    print_separator()
    print("SCENARIO 4: LANDLORD - Emma's Property Portfolio")
    print_separator()
    
    print("Background:")
    print("- Emma owns 3 rental properties generating £45,000 annual rent")
    print("- Mortgage interest: £15,000 per year")
    print("- Other expenses (repairs, insurance, agent fees): £8,000")
    print("- All properties are furnished")
    print("- Considering whether to incorporate")
    
    optimizer = TaxOptimizationEngine()
    
    results = optimizer.optimize_for_landlord(
        rental_income=45000,
        mortgage_interest=15000,
        other_expenses=8000,
        is_furnished=True,
        number_of_properties=3
    )
    
    print_results("Emma's Property Tax Analysis", results)
    
    incorporation = results['incorporation_analysis']
    print(f"\n🏢 Incorporation Analysis:")
    print(f"   Current Tax (Individual): £{incorporation['current_tax']:,.2f}")
    print(f"   Corporation Tax (If Incorporated): £{incorporation['corporation_tax_if_incorporated']:,.2f}")
    print(f"   Potential Saving: £{incorporation['potential_saving']:,.2f}")
    print(f"   Recommended: {'YES ✓' if incorporation['recommended'] else 'NO ✗'}")
    
    print("\nKey Recommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec['strategy']}")
        print(f"   → {rec['description']}")
        print(f"   💵 Saving: {rec['saving']}")


def scenario_5_high_earner():
    """
    Scenario 5: High Earning Director
    Michael is a director with high income and needs advanced tax planning.
    """
    print_separator()
    print("SCENARIO 5: HIGH EARNER - Michael's Advanced Tax Planning")
    print_separator()
    
    print("Background:")
    print("- Michael's company generates £500,000 profit")
    print("- Currently takes £100,000 salary and £150,000 dividends")
    print("- Wants to maximize pension contributions")
    print("- Looking for all available tax-saving strategies")
    
    calculator = UKTaxCalculator()
    
    # Current position
    paye = calculator.calculate_paye(100000)
    dividend_tax = calculator.calculate_dividend_tax(150000, 100000)
    corp_tax = calculator.calculate_corporation_tax(500000)
    
    print("\nCurrent Tax Position:")
    print(f"  Salary: £100,000")
    print(f"    → Income Tax & NI: £{paye['total_employee_deductions']:,.2f}")
    print(f"  Dividends: £150,000")
    print(f"    → Dividend Tax: £{dividend_tax['dividend_tax']:,.2f}")
    print(f"  Company Profit: £500,000")
    print(f"    → Corporation Tax: £{corp_tax['corporation_tax']:,.2f}")
    print(f"  TOTAL TAX: £{paye['total_employee_deductions'] + dividend_tax['dividend_tax'] + corp_tax['corporation_tax']:,.2f}")
    
    # Optimal with pension
    optimal_salary = 12570
    pension_contribution = 60000  # Maximum annual allowance
    
    adjusted_profit = 500000 - optimal_salary - pension_contribution
    optimal_corp_tax = calculator.calculate_corporation_tax(adjusted_profit)
    profit_after_tax = adjusted_profit - optimal_corp_tax['corporation_tax']
    
    optimal_paye = calculator.calculate_paye(optimal_salary)
    optimal_dividend_tax = calculator.calculate_dividend_tax(profit_after_tax, optimal_salary)
    
    reliefs = TaxReliefs()
    pension_relief = reliefs.calculate_pension_relief(pension_contribution, optimal_salary)
    
    print("\nOptimized Tax Position:")
    print(f"  Salary: £{optimal_salary:,}")
    print(f"    → Income Tax & NI: £{optimal_paye['total_employee_deductions']:,.2f}")
    print(f"  Employer Pension: £{pension_contribution:,}")
    print(f"    → Corporation Tax Relief: £{pension_contribution * 0.25:,.2f}")
    print(f"  Dividends: £{profit_after_tax:,.2f}")
    print(f"    → Dividend Tax: £{optimal_dividend_tax['dividend_tax']:,.2f}")
    print(f"  Company Profit: £{adjusted_profit:,.2f}")
    print(f"    → Corporation Tax: £{optimal_corp_tax['corporation_tax']:,.2f}")
    
    total_optimal = optimal_paye['total_employee_deductions'] + optimal_dividend_tax['dividend_tax'] + optimal_corp_tax['corporation_tax']
    total_current = paye['total_employee_deductions'] + dividend_tax['dividend_tax'] + corp_tax['corporation_tax']
    
    print(f"  TOTAL TAX: £{total_optimal:,.2f}")
    print(f"\n💰 TOTAL ANNUAL SAVING: £{total_current - total_optimal:,.2f}")
    
    print("\nKey Strategies Applied:")
    print("1. Reduced salary to personal allowance (£12,570)")
    print("2. Maximized employer pension contribution (£60,000)")
    print("3. Extracted remaining profit as dividends")
    print("4. Total benefit: Lower income tax, no NI, corporation tax relief")


def scenario_6_capital_gains():
    """
    Scenario 6: Capital Gains Tax Planning
    David sold shares and property, needs to optimize CGT.
    """
    print_separator()
    print("SCENARIO 6: CAPITAL GAINS - David's Investment Sales")
    print_separator()
    
    print("Background:")
    print("- David sold shares generating £50,000 capital gain")
    print("- Sold a rental property with £80,000 capital gain")
    print("- Annual income: £40,000 (salary)")
    print("- Wants to understand CGT liability and planning options")
    
    calculator = UKTaxCalculator()
    
    # Shares CGT
    shares_cgt = calculator.calculate_cgt(
        capital_gains=50000,
        annual_income=40000,
        is_property=False
    )
    
    # Property CGT
    property_cgt = calculator.calculate_cgt(
        capital_gains=80000,
        annual_income=40000,
        is_property=True
    )
    
    print("\nShares Capital Gains:")
    print(f"  Gains: £{shares_cgt['capital_gains']:,}")
    print(f"  Annual Exemption: £{shares_cgt['annual_exemption']:,}")
    print(f"  Taxable Gains: £{shares_cgt['taxable_gains']:,}")
    print(f"  CGT Due: £{shares_cgt['cgt_due']:,.2f}")
    print(f"  Effective Rate: {shares_cgt['effective_rate']}%")
    
    print("\nProperty Capital Gains:")
    print(f"  Gains: £{property_cgt['capital_gains']:,}")
    print(f"  Taxable Gains: £{property_cgt['taxable_gains']:,}")
    print(f"  CGT Due: £{property_cgt['cgt_due']:,.2f}")
    print(f"  Effective Rate: {property_cgt['effective_rate']}%")
    
    total_cgt = shares_cgt['cgt_due'] + property_cgt['cgt_due']
    print(f"\n💰 Total CGT Due: £{total_cgt:,.2f}")
    
    print("\nTax Planning Strategies:")
    print("1. Split sales across tax years to use exemption twice")
    print(f"   → Save up to £{calculator.CGT_ANNUAL_EXEMPTION * 0.20:,.2f} per year")
    print("2. Transfer assets to spouse to use their exemption")
    print(f"   → Save up to £{calculator.CGT_ANNUAL_EXEMPTION * 0.20:,.2f}")
    print("3. Time sales when income is lower (use basic rate band)")
    print("4. Consider Business Asset Disposal Relief for qualifying business")
    print("   → 10% rate on up to £1,000,000 lifetime allowance")


def scenario_7_vat_planning():
    """
    Scenario 7: VAT Registration and Planning
    A growing business approaching VAT threshold.
    """
    print_separator()
    print("SCENARIO 7: VAT PLANNING - Growing Business Considerations")
    print_separator()
    
    print("Background:")
    print("- Business turnover: £95,000 (above VAT threshold)")
    print("- Business expenses: £30,000")
    print("- Must register for VAT")
    print("- Wants to understand impact")
    
    calculator = UKTaxCalculator()
    
    vat_calc = calculator.calculate_vat(
        turnover=95000,
        expenses=30000,
        scheme='standard'
    )
    
    print("\nVAT Calculation:")
    print(f"  Turnover (inc VAT): £{vat_calc['turnover']:,}")
    print(f"  Turnover (ex VAT): £{vat_calc['turnover_ex_vat']:,.2f}")
    print(f"  Output VAT: £{vat_calc['output_vat']:,.2f}")
    print(f"  Input VAT (on expenses): £{vat_calc['input_vat']:,.2f}")
    print(f"  Net VAT Due: £{vat_calc['vat_due']:,.2f}")
    print(f"  VAT Rate: {vat_calc['vat_rate']}%")
    
    print("\nVAT Scheme Options:")
    print("\n1. Standard VAT Accounting")
    print("   - Charge 20% VAT on sales")
    print("   - Reclaim VAT on purchases")
    print("   - Quarterly returns")
    
    print("\n2. Flat Rate Scheme")
    print("   - Pay flat % of gross turnover")
    print("   - Simpler accounting")
    print("   - Rate depends on business type")
    
    print("\n3. Cash Accounting Scheme")
    print("   - Pay VAT when customers pay you")
    print("   - Better for cash flow")
    print("   - Only if turnover under £1.35m")
    
    print("\nVAT Planning Tips:")
    print("- Register voluntarily before threshold to reclaim VAT on startup costs")
    print("- Time large purchases before VAT registration")
    print("- Consider timing of VAT registration (can backdate up to 4 years)")
    print("- Keep detailed VAT records for HMRC inspections")


def run_all_scenarios():
    """Run all demonstration scenarios."""
    print("\n" + "="*80)
    print("UK TAX CALCULATOR - COMPREHENSIVE SCENARIO DEMONSTRATIONS")
    print("Tax Year: 2024/2025")
    print("="*80)
    
    scenario_1_company_director()
    scenario_2_sole_trader()
    scenario_3_company_owner()
    scenario_4_landlord()
    scenario_5_high_earner()
    scenario_6_capital_gains()
    scenario_7_vat_planning()
    
    print_separator()
    print("END OF SCENARIOS")
    print("\nNote: These scenarios are illustrative. Always consult a qualified")
    print("tax advisor for personalized advice based on your specific circumstances.")
    print_separator()


if __name__ == '__main__':
    run_all_scenarios()
