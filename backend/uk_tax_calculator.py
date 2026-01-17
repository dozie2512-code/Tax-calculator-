"""
UK Tax Calculator - 2025/2026 Tax Year (Illustrative)

This module provides comprehensive UK tax calculations including:
- Income Tax (Personal Allowance, Basic, Higher, Additional rates)
- National Insurance Contributions (Employee and Employer)
- Dividend Tax
- Corporation Tax
- Capital Gains Tax

Note: These calculations are illustrative and based on typical 2025/2026 rates.
Always consult with a qualified tax advisor for official tax advice.
"""

from typing import Dict, Any


class UKTaxCalculator:
    """
    UK Tax Calculator for various tax scenarios.
    Implements HMRC tax calculations for 2025/2026 (illustrative).
    """
    
    # Income Tax Rates and Thresholds (2025/2026 illustrative)
    PERSONAL_ALLOWANCE = 12570
    BASIC_RATE_THRESHOLD = 50270
    HIGHER_RATE_THRESHOLD = 150000
    
    BASIC_RATE = 0.20
    HIGHER_RATE = 0.40
    ADDITIONAL_RATE = 0.45
    
    # National Insurance Thresholds and Rates
    NI_PRIMARY_THRESHOLD = 12570
    NI_UPPER_EARNINGS_LIMIT = 50270
    
    NI_EMPLOYEE_RATE_BELOW_UEL = 0.08
    NI_EMPLOYEE_RATE_ABOVE_UEL = 0.02
    NI_EMPLOYER_RATE = 0.138
    NI_EMPLOYER_THRESHOLD = 9100
    
    # Dividend Tax
    DIVIDEND_ALLOWANCE = 500
    DIVIDEND_BASIC_RATE = 0.0875
    DIVIDEND_HIGHER_RATE = 0.3375
    DIVIDEND_ADDITIONAL_RATE = 0.3935
    
    # Corporation Tax
    SMALL_PROFITS_RATE = 0.19
    MAIN_CORP_TAX_RATE = 0.25
    SMALL_PROFITS_LIMIT = 50000
    UPPER_PROFITS_LIMIT = 250000
    
    def __init__(self):
        """Initialize the UK Tax Calculator."""
        pass
    
    def calculate_income_tax(self, gross_income: float) -> Dict[str, float]:
        """
        Calculate income tax on employment income.
        
        Args:
            gross_income: Annual gross employment income
            
        Returns:
            Dictionary containing tax breakdown
        """
        # Adjust personal allowance if income > £100,000
        personal_allowance = self.PERSONAL_ALLOWANCE
        if gross_income > 100000:
            reduction = min(personal_allowance, (gross_income - 100000) / 2)
            personal_allowance -= reduction
        
        taxable_income = max(0, gross_income - personal_allowance)
        
        income_tax = 0
        basic_rate_tax = 0
        higher_rate_tax = 0
        additional_rate_tax = 0
        
        if taxable_income > 0:
            # Basic rate band
            basic_band_income = min(taxable_income, self.BASIC_RATE_THRESHOLD - personal_allowance)
            basic_rate_tax = basic_band_income * self.BASIC_RATE
            income_tax += basic_rate_tax
            
            # Higher rate band
            if taxable_income > (self.BASIC_RATE_THRESHOLD - personal_allowance):
                higher_band_income = min(
                    taxable_income - (self.BASIC_RATE_THRESHOLD - personal_allowance),
                    self.HIGHER_RATE_THRESHOLD - self.BASIC_RATE_THRESHOLD
                )
                higher_rate_tax = higher_band_income * self.HIGHER_RATE
                income_tax += higher_rate_tax
            
            # Additional rate band
            if taxable_income > (self.HIGHER_RATE_THRESHOLD - personal_allowance):
                additional_band_income = taxable_income - (self.HIGHER_RATE_THRESHOLD - personal_allowance)
                additional_rate_tax = additional_band_income * self.ADDITIONAL_RATE
                income_tax += additional_rate_tax
        
        return {
            'gross_income': round(gross_income, 2),
            'personal_allowance': round(personal_allowance, 2),
            'taxable_income': round(taxable_income, 2),
            'basic_rate_tax': round(basic_rate_tax, 2),
            'higher_rate_tax': round(higher_rate_tax, 2),
            'additional_rate_tax': round(additional_rate_tax, 2),
            'total_income_tax': round(income_tax, 2)
        }
    
    def calculate_national_insurance(self, annual_income: float, is_employer: bool = False) -> Dict[str, float]:
        """
        Calculate National Insurance Contributions.
        
        Args:
            annual_income: Annual income subject to NI
            is_employer: If True, calculate employer NI, otherwise employee NI
            
        Returns:
            Dictionary containing NI breakdown
        """
        if is_employer:
            # Employer NI
            ni_liable_income = max(0, annual_income - self.NI_EMPLOYER_THRESHOLD)
            employer_ni = ni_liable_income * self.NI_EMPLOYER_RATE
            
            return {
                'annual_income': round(annual_income, 2),
                'ni_threshold': round(self.NI_EMPLOYER_THRESHOLD, 2),
                'ni_liable_income': round(ni_liable_income, 2),
                'employer_ni': round(employer_ni, 2)
            }
        else:
            # Employee NI
            ni_below_uel = 0
            ni_above_uel = 0
            
            if annual_income > self.NI_PRIMARY_THRESHOLD:
                # NI between primary threshold and upper earnings limit
                income_below_uel = min(annual_income, self.NI_UPPER_EARNINGS_LIMIT) - self.NI_PRIMARY_THRESHOLD
                ni_below_uel = income_below_uel * self.NI_EMPLOYEE_RATE_BELOW_UEL
                
                # NI above upper earnings limit
                if annual_income > self.NI_UPPER_EARNINGS_LIMIT:
                    income_above_uel = annual_income - self.NI_UPPER_EARNINGS_LIMIT
                    ni_above_uel = income_above_uel * self.NI_EMPLOYEE_RATE_ABOVE_UEL
            
            total_ni = ni_below_uel + ni_above_uel
            
            return {
                'annual_income': round(annual_income, 2),
                'primary_threshold': round(self.NI_PRIMARY_THRESHOLD, 2),
                'upper_earnings_limit': round(self.NI_UPPER_EARNINGS_LIMIT, 2),
                'ni_below_uel': round(ni_below_uel, 2),
                'ni_above_uel': round(ni_above_uel, 2),
                'total_employee_ni': round(total_ni, 2)
            }
    
    def calculate_dividend_tax(self, dividend_income: float, other_income: float = 0) -> Dict[str, float]:
        """
        Calculate dividend tax based on total income.
        
        Args:
            dividend_income: Annual dividend income
            other_income: Other taxable income (used to determine tax band)
            
        Returns:
            Dictionary containing dividend tax breakdown
        """
        # Dividend allowance
        taxable_dividends = max(0, dividend_income - self.DIVIDEND_ALLOWANCE)
        
        dividend_tax = 0
        basic_rate_div_tax = 0
        higher_rate_div_tax = 0
        additional_rate_div_tax = 0
        
        if taxable_dividends > 0:
            # Determine which tax bands the dividends fall into
            total_income = other_income + dividend_income
            
            # Calculate how much is in each band
            basic_rate_limit = self.BASIC_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE
            higher_rate_limit = self.HIGHER_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE
            
            # Basic rate dividends
            if other_income < basic_rate_limit:
                basic_rate_dividends = min(taxable_dividends, basic_rate_limit - other_income)
                basic_rate_div_tax = basic_rate_dividends * self.DIVIDEND_BASIC_RATE
                dividend_tax += basic_rate_div_tax
            
            # Higher rate dividends
            if total_income - self.DIVIDEND_ALLOWANCE > basic_rate_limit:
                higher_band_start = max(other_income, basic_rate_limit) - other_income
                higher_rate_dividends = min(
                    taxable_dividends - higher_band_start,
                    higher_rate_limit - max(other_income, basic_rate_limit)
                )
                if higher_rate_dividends > 0:
                    higher_rate_div_tax = higher_rate_dividends * self.DIVIDEND_HIGHER_RATE
                    dividend_tax += higher_rate_div_tax
            
            # Additional rate dividends
            if total_income - self.DIVIDEND_ALLOWANCE > higher_rate_limit:
                additional_band_start = max(0, higher_rate_limit - other_income)
                additional_rate_dividends = taxable_dividends - additional_band_start - (basic_rate_div_tax / self.DIVIDEND_BASIC_RATE if basic_rate_div_tax > 0 else 0) - (higher_rate_div_tax / self.DIVIDEND_HIGHER_RATE if higher_rate_div_tax > 0 else 0)
                if additional_rate_dividends > 0:
                    additional_rate_div_tax = additional_rate_dividends * self.DIVIDEND_ADDITIONAL_RATE
                    dividend_tax += additional_rate_div_tax
        
        return {
            'dividend_income': round(dividend_income, 2),
            'dividend_allowance': round(self.DIVIDEND_ALLOWANCE, 2),
            'taxable_dividends': round(taxable_dividends, 2),
            'basic_rate_div_tax': round(basic_rate_div_tax, 2),
            'higher_rate_div_tax': round(higher_rate_div_tax, 2),
            'additional_rate_div_tax': round(additional_rate_div_tax, 2),
            'total_dividend_tax': round(dividend_tax, 2)
        }
    
    def calculate_corporation_tax(self, company_profit: float) -> Dict[str, float]:
        """
        Calculate corporation tax with marginal relief.
        
        Args:
            company_profit: Annual company profit
            
        Returns:
            Dictionary containing corporation tax breakdown
        """
        corp_tax = 0
        effective_rate = 0
        
        if company_profit <= self.SMALL_PROFITS_LIMIT:
            # Small profits rate
            corp_tax = company_profit * self.SMALL_PROFITS_RATE
            effective_rate = self.SMALL_PROFITS_RATE
        elif company_profit >= self.UPPER_PROFITS_LIMIT:
            # Main rate
            corp_tax = company_profit * self.MAIN_CORP_TAX_RATE
            effective_rate = self.MAIN_CORP_TAX_RATE
        else:
            # Marginal relief zone
            # Marginal relief fraction: 3/200
            marginal_relief_fraction = 3 / 200
            standard_rate_tax = company_profit * self.MAIN_CORP_TAX_RATE
            marginal_relief = (self.UPPER_PROFITS_LIMIT - company_profit) * marginal_relief_fraction
            corp_tax = standard_rate_tax - marginal_relief
            effective_rate = corp_tax / company_profit if company_profit > 0 else 0
        
        return {
            'company_profit': round(company_profit, 2),
            'corporation_tax': round(corp_tax, 2),
            'effective_rate': round(effective_rate * 100, 2),
            'profit_after_tax': round(company_profit - corp_tax, 2)
        }
    
    def calculate_total_tax_liability(self, 
                                     salary: float = 0,
                                     dividends: float = 0,
                                     other_income: float = 0,
                                     company_profit: float = 0) -> Dict[str, Any]:
        """
        Calculate total tax liability for a comprehensive tax scenario.
        
        Args:
            salary: Annual employment salary
            dividends: Annual dividend income
            other_income: Other taxable income
            company_profit: Company profit (for directors/owners)
            
        Returns:
            Dictionary containing comprehensive tax breakdown
        """
        # Calculate each component
        income_tax_calc = self.calculate_income_tax(salary + other_income)
        ni_calc = self.calculate_national_insurance(salary)
        dividend_tax_calc = self.calculate_dividend_tax(dividends, salary + other_income)
        
        total_personal_tax = (income_tax_calc['total_income_tax'] + 
                            ni_calc['total_employee_ni'] + 
                            dividend_tax_calc['total_dividend_tax'])
        
        total_income = salary + dividends + other_income
        net_income = total_income - total_personal_tax
        
        result = {
            'income_breakdown': {
                'salary': round(salary, 2),
                'dividends': round(dividends, 2),
                'other_income': round(other_income, 2),
                'total_income': round(total_income, 2)
            },
            'tax_breakdown': {
                'income_tax': round(income_tax_calc['total_income_tax'], 2),
                'national_insurance': round(ni_calc['total_employee_ni'], 2),
                'dividend_tax': round(dividend_tax_calc['total_dividend_tax'], 2),
                'total_personal_tax': round(total_personal_tax, 2)
            },
            'net_position': {
                'total_income': round(total_income, 2),
                'total_tax': round(total_personal_tax, 2),
                'net_income': round(net_income, 2),
                'effective_tax_rate': round((total_personal_tax / total_income * 100) if total_income > 0 else 0, 2)
            }
        }
        
        # Add company tax if applicable
        if company_profit > 0:
            corp_tax_calc = self.calculate_corporation_tax(company_profit)
            result['company_tax'] = corp_tax_calc
        
        return result


if __name__ == '__main__':
    # Example usage
    calculator = UKTaxCalculator()
    
    # Example 1: Company Director
    print("Example 1: Company Director")
    print("-" * 50)
    result = calculator.calculate_total_tax_liability(
        salary=30000,
        dividends=20000,
        company_profit=60000
    )
    print(f"Total Income: £{result['income_breakdown']['total_income']:,.2f}")
    print(f"Total Tax: £{result['net_position']['total_tax']:,.2f}")
    print(f"Net Income: £{result['net_position']['net_income']:,.2f}")
    print(f"Effective Rate: {result['net_position']['effective_tax_rate']}%")
    print()
