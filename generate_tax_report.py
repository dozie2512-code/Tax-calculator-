"""
Generate comprehensive tax report for users
Creates detailed text-based reports that can be saved or printed
"""

from backend.uk_tax_calculator import UKTaxCalculator, TaxReliefs
from backend.tax_optimization import TaxOptimizationEngine
from datetime import datetime
import json


class TaxReportGenerator:
    """Generate comprehensive tax reports."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.calculator = UKTaxCalculator()
        self.optimizer = TaxOptimizationEngine()
    
    def generate_header(self, user_name: str, user_type: str) -> str:
        """Generate report header."""
        header = []
        header.append("="*80)
        header.append("UK TAX OPTIMIZATION REPORT")
        header.append("="*80)
        header.append(f"Generated: {datetime.now().strftime('%d %B %Y at %H:%M')}")
        header.append(f"Tax Year: 2024/2025")
        header.append(f"Client Name: {user_name}")
        header.append(f"Client Type: {user_type}")
        header.append("="*80)
        header.append("")
        return "\n".join(header)
    
    def generate_section(self, title: str, content: dict) -> str:
        """Generate a report section."""
        section = []
        section.append("")
        section.append("-"*80)
        section.append(f"{title}")
        section.append("-"*80)
        section.append("")
        
        for key, value in content.items():
            if isinstance(value, (int, float)):
                if key.lower().find('rate') != -1 or key.lower().find('percent') != -1:
                    section.append(f"  {key}: {value}%")
                else:
                    section.append(f"  {key}: £{value:,.2f}")
            else:
                section.append(f"  {key}: {value}")
        
        return "\n".join(section)
    
    def generate_recommendations(self, recommendations: list) -> str:
        """Generate recommendations section."""
        section = []
        section.append("")
        section.append("-"*80)
        section.append("TAX-SAVING RECOMMENDATIONS")
        section.append("-"*80)
        section.append("")
        
        for i, rec in enumerate(recommendations, 1):
            section.append(f"{i}. {rec['strategy']}")
            section.append(f"   {rec['description']}")
            
            if isinstance(rec['saving'], (int, float)):
                section.append(f"   Potential Saving: £{rec['saving']:,.2f}")
            else:
                section.append(f"   Benefit: {rec['saving']}")
            section.append("")
        
        return "\n".join(section)
    
    def generate_footer(self) -> str:
        """Generate report footer."""
        footer = []
        footer.append("")
        footer.append("="*80)
        footer.append("IMPORTANT DISCLAIMER")
        footer.append("="*80)
        footer.append("")
        footer.append("This report provides illustrative tax calculations and optimization strategies")
        footer.append("based on HMRC guidelines for the 2024/2025 tax year. The information is for")
        footer.append("informational purposes only and should not be considered as financial or tax")
        footer.append("advice.")
        footer.append("")
        footer.append("Tax situations can be complex and individual circumstances vary. Always consult")
        footer.append("with a qualified tax advisor, accountant, or HMRC directly before making any")
        footer.append("financial decisions or implementing tax strategies.")
        footer.append("")
        footer.append("="*80)
        footer.append("")
        footer.append("For HMRC guidance visit: www.gov.uk/government/organisations/hm-revenue-customs")
        footer.append("For Self Assessment help: www.gov.uk/self-assessment-tax-returns")
        footer.append("")
        footer.append("="*80)
        return "\n".join(footer)
    
    def generate_director_report(self, user_name: str, salary: float, dividends: float,
                                company_profit: float, pension: float = 0) -> str:
        """Generate report for company director."""
        
        report = []
        
        # Header
        report.append(self.generate_header(user_name, "Company Director"))
        
        # Executive Summary
        results = self.optimizer.optimize_for_director(
            salary=salary,
            dividends=dividends,
            company_profit=company_profit,
            pension_contribution=pension
        )
        
        executive = {
            "Current Annual Salary": salary,
            "Current Annual Dividends": dividends,
            "Company Profit": company_profit,
            "Total Current Tax": results['current_position']['total_tax'],
            "Current Net Income": results['current_position']['net_income'],
            "Potential Annual Saving": results['potential_saving']
        }
        report.append(self.generate_section("EXECUTIVE SUMMARY", executive))
        
        # Current Position
        current = {
            "Gross Salary": results['current_position']['salary'],
            "Dividends": results['current_position']['dividends'],
            "Total Tax Liability": results['current_position']['total_tax'],
            "Net Income": results['current_position']['net_income']
        }
        report.append(self.generate_section("CURRENT TAX POSITION", current))
        
        # Detailed Breakdown
        paye = results['detailed_calculations']['paye']
        breakdown = {
            "Income Tax": paye['income_tax'],
            "Employee National Insurance": paye['employee_ni'],
            "Employer National Insurance": paye['employer_ni'],
            "Effective Tax Rate": paye['effective_tax_rate']
        }
        report.append(self.generate_section("PAYE BREAKDOWN", breakdown))
        
        dividend_tax = results['detailed_calculations']['dividend_tax']
        div_breakdown = {
            "Total Dividends": dividend_tax['dividends'],
            "Dividend Allowance": dividend_tax['dividend_allowance'],
            "Taxable Dividends": dividend_tax['taxable_dividends'],
            "Dividend Tax Due": dividend_tax['dividend_tax'],
            "Effective Rate": dividend_tax['effective_rate']
        }
        report.append(self.generate_section("DIVIDEND TAX BREAKDOWN", div_breakdown))
        
        corp = results['detailed_calculations']['corporation_tax']
        corp_breakdown = {
            "Company Taxable Profit": corp['taxable_profit'],
            "Corporation Tax Band": corp['band'],
            "Corporation Tax Due": corp['corporation_tax'],
            "Effective Rate": corp['effective_rate']
        }
        report.append(self.generate_section("CORPORATION TAX BREAKDOWN", corp_breakdown))
        
        # Optimized Position
        optimal = {
            "Optimal Salary": results['optimal_position']['salary'],
            "Optimal Dividends": results['optimal_position']['dividends'],
            "Total Tax Liability": results['optimal_position']['total_tax'],
            "Net Income": results['optimal_position']['net_income']
        }
        report.append(self.generate_section("OPTIMIZED TAX POSITION", optimal))
        
        # Savings Summary
        savings = {
            "Potential Annual Saving": results['potential_saving'],
            "Monthly Saving": results['potential_saving'] / 12,
            "5-Year Saving": results['potential_saving'] * 5
        }
        report.append(self.generate_section("SAVINGS SUMMARY", savings))
        
        # Recommendations
        report.append(self.generate_recommendations(results['recommendations']))
        
        # Footer
        report.append(self.generate_footer())
        
        return "\n".join(report)
    
    def generate_sole_trader_report(self, user_name: str, income: float, expenses: float,
                                   capital_allowances: float, pension: float = 0) -> str:
        """Generate report for sole trader."""
        
        report = []
        
        # Header
        report.append(self.generate_header(user_name, "Sole Trader"))
        
        # Get optimization results
        results = self.optimizer.optimize_for_sole_trader(
            trading_income=income,
            allowable_expenses=expenses,
            capital_allowances=capital_allowances,
            pension_contribution=pension
        )
        
        # Executive Summary
        executive = {
            "Trading Income": income,
            "Allowable Expenses": expenses,
            "Capital Allowances": capital_allowances,
            "Taxable Profit": results['income_analysis']['taxable_profit'],
            "Total Tax Liability": results['tax_position']['total_employee_deductions'],
            "Net Income": results['tax_position']['net_salary']
        }
        report.append(self.generate_section("EXECUTIVE SUMMARY", executive))
        
        # Income Analysis
        analysis = {
            "Trading Income": results['income_analysis']['trading_income'],
            "Allowable Expenses": results['income_analysis']['allowable_expenses'],
            "Capital Allowances": results['income_analysis']['capital_allowances'],
            "Taxable Profit": results['income_analysis']['taxable_profit'],
            "Method Used": results['income_analysis']['method_used']
        }
        report.append(self.generate_section("INCOME ANALYSIS", analysis))
        
        # Tax Position
        tax_pos = results['tax_position']
        tax_breakdown = {
            "Income Tax": tax_pos['income_tax'],
            "National Insurance": tax_pos['employee_ni'],
            "Total Tax": tax_pos['total_employee_deductions'],
            "Net Income": tax_pos['net_salary'],
            "Effective Tax Rate": tax_pos['effective_tax_rate']
        }
        report.append(self.generate_section("TAX POSITION", tax_breakdown))
        
        # Pension Relief (if applicable)
        if results['pension_relief']:
            pension_relief = {
                "Pension Contribution": results['pension_relief']['pension_contribution'],
                "Basic Rate Relief": results['pension_relief']['basic_rate_relief'],
                "Higher Rate Relief": results['pension_relief']['higher_rate_relief'],
                "Total Relief": results['pension_relief']['total_relief']
            }
            report.append(self.generate_section("PENSION RELIEF", pension_relief))
        
        # Recommendations
        report.append(self.generate_recommendations(results['recommendations']))
        
        # Footer
        report.append(self.generate_footer())
        
        return "\n".join(report)
    
    def save_report(self, report: str, filename: str):
        """Save report to file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to: {filename}")


def main():
    """Generate sample reports."""
    generator = TaxReportGenerator()
    
    print("\nGenerating Sample Tax Reports...\n")
    
    # Generate Director Report
    director_report = generator.generate_director_report(
        user_name="Sarah Johnson",
        salary=50000,
        dividends=30000,
        company_profit=100000,
        pension=0
    )
    generator.save_report(director_report, "director_tax_report.txt")
    
    # Generate Sole Trader Report
    trader_report = generator.generate_sole_trader_report(
        user_name="James Smith",
        income=60000,
        expenses=12000,
        capital_allowances=8000,
        pension=5000
    )
    generator.save_report(trader_report, "sole_trader_tax_report.txt")
    
    print("\n✅ Reports generated successfully!")
    print("\nGenerated files:")
    print("  - director_tax_report.txt")
    print("  - sole_trader_tax_report.txt")
    print("\nThese reports can be:")
    print("  • Printed for client meetings")
    print("  • Saved for records")
    print("  • Emailed to clients")
    print("  • Converted to PDF")


if __name__ == '__main__':
    main()
