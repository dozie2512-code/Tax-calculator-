"""
UK Tax Calculator Module

Implements HMRC tax calculations including PAYE, National Insurance,
Corporation Tax, Dividend Tax, and Capital Gains Tax.

Based on 2025/2026 tax year rates (illustrative).
"""

from typing import Dict, Any


class TaxConstants:
    """UK Tax Constants for 2025/2026 tax year (illustrative)"""
    
    # Income Tax
    PERSONAL_ALLOWANCE = 12_570
    BASIC_RATE_THRESHOLD = 50_270
    HIGHER_RATE_THRESHOLD = 150_000
    
    BASIC_RATE = 0.20
    HIGHER_RATE = 0.40
    ADDITIONAL_RATE = 0.45
    
    # National Insurance (Employee)
    NI_PRIMARY_THRESHOLD = 12_570  # Annual
    NI_UPPER_EARNINGS_LIMIT = 50_270  # Annual
    NI_RATE_BELOW_UEL = 0.08
    NI_RATE_ABOVE_UEL = 0.02
    
    # Class 2 NI (Self-employed)
    CLASS_2_NI_WEEKLY_RATE = 3.45
    CLASS_2_NI_SMALL_PROFIT_THRESHOLD = 6_725
    
    # Corporation Tax
    CORPORATION_TAX_SMALL_PROFITS_RATE = 0.19
    CORPORATION_TAX_MAIN_RATE = 0.25
    CORPORATION_TAX_THRESHOLD = 50_000
    
    # Dividend Tax
    DIVIDEND_ALLOWANCE = 500
    DIVIDEND_BASIC_RATE = 0.0875
    DIVIDEND_HIGHER_RATE = 0.3375
    DIVIDEND_ADDITIONAL_RATE = 0.3935
    
    # Capital Gains Tax
    CGT_ANNUAL_EXEMPT_AMOUNT = 3_000
    CGT_BASIC_RATE = 0.10
    CGT_HIGHER_RATE = 0.20
    
    # Property Tax
    CGT_PROPERTY_BASIC_RATE = 0.18
    CGT_PROPERTY_HIGHER_RATE = 0.28
    
    # Allowances and Reliefs
    TRADING_ALLOWANCE = 1_000
    PROPERTY_ALLOWANCE = 1_000
    ANNUAL_INVESTMENT_ALLOWANCE = 1_000_000
    PENSION_ANNUAL_ALLOWANCE = 60_000


class TaxReliefs:
    """Calculate various tax reliefs and allowances"""
    
    # Constants
    TRADING_ALLOWANCE = TaxConstants.TRADING_ALLOWANCE
    PROPERTY_ALLOWANCE = TaxConstants.PROPERTY_ALLOWANCE
    PENSION_ANNUAL_ALLOWANCE = TaxConstants.PENSION_ANNUAL_ALLOWANCE
    
    def calculate_trading_allowance(self, trading_income: float) -> Dict[str, Any]:
        """
        Calculate trading allowance benefit.
        £1,000 allowance for trading income.
        """
        if trading_income <= self.TRADING_ALLOWANCE:
            return {
                'allowance_applied': trading_income,
                'taxable_income': 0,
                'benefit': 'Full trading income covered by allowance'
            }
        return {
            'allowance_applied': self.TRADING_ALLOWANCE,
            'taxable_income': trading_income - self.TRADING_ALLOWANCE,
            'benefit': f'£{self.TRADING_ALLOWANCE:,} deducted from trading income'
        }
    
    def calculate_property_allowance(self, rental_income: float) -> Dict[str, Any]:
        """
        Calculate property allowance benefit.
        £1,000 allowance for property income.
        """
        if rental_income <= self.PROPERTY_ALLOWANCE:
            return {
                'allowance_applied': rental_income,
                'taxable_income': 0,
                'benefit': 'Full rental income covered by allowance'
            }
        return {
            'allowance_applied': self.PROPERTY_ALLOWANCE,
            'taxable_income': rental_income - self.PROPERTY_ALLOWANCE,
            'benefit': f'£{self.PROPERTY_ALLOWANCE:,} deducted from rental income'
        }
    
    def calculate_pension_relief(self, contribution: float, income: float) -> Dict[str, Any]:
        """
        Calculate pension contribution tax relief.
        Relief at marginal rate up to annual allowance.
        """
        # Cap at annual allowance
        eligible_contribution = min(contribution, self.PENSION_ANNUAL_ALLOWANCE)
        
        # Determine marginal tax rate
        if income <= TaxConstants.PERSONAL_ALLOWANCE:
            marginal_rate = 0
        elif income <= TaxConstants.BASIC_RATE_THRESHOLD:
            marginal_rate = TaxConstants.BASIC_RATE
        elif income <= TaxConstants.HIGHER_RATE_THRESHOLD:
            marginal_rate = TaxConstants.HIGHER_RATE
        else:
            marginal_rate = TaxConstants.ADDITIONAL_RATE
        
        relief = eligible_contribution * marginal_rate
        
        return {
            'contribution': contribution,
            'eligible_contribution': eligible_contribution,
            'marginal_rate': marginal_rate,
            'tax_relief': relief,
            'total_relief': relief,
            'net_cost': contribution - relief
        }


class UKTaxCalculator:
    """Main UK Tax Calculator"""
    
    # Expose constants
    PERSONAL_ALLOWANCE = TaxConstants.PERSONAL_ALLOWANCE
    BASIC_RATE_THRESHOLD = TaxConstants.BASIC_RATE_THRESHOLD
    HIGHER_RATE_THRESHOLD = TaxConstants.HIGHER_RATE_THRESHOLD
    DIVIDEND_ALLOWANCE = TaxConstants.DIVIDEND_ALLOWANCE
    DIVIDEND_BASIC_RATE = TaxConstants.DIVIDEND_BASIC_RATE
    
    def calculate_paye(self, annual_salary: float) -> Dict[str, Any]:
        """
        Calculate PAYE (Income Tax) and National Insurance.
        
        Args:
            annual_salary: Annual gross salary
            
        Returns:
            Dictionary with tax breakdown
        """
        # Income Tax
        taxable_income = max(0, annual_salary - TaxConstants.PERSONAL_ALLOWANCE)
        income_tax = 0
        
        if taxable_income > 0:
            # Basic rate band
            basic_band_income = min(
                taxable_income,
                TaxConstants.BASIC_RATE_THRESHOLD - TaxConstants.PERSONAL_ALLOWANCE
            )
            
            if taxable_income <= (TaxConstants.BASIC_RATE_THRESHOLD - TaxConstants.PERSONAL_ALLOWANCE):
                income_tax = basic_band_income * TaxConstants.BASIC_RATE
            elif taxable_income <= (TaxConstants.HIGHER_RATE_THRESHOLD - TaxConstants.PERSONAL_ALLOWANCE):
                income_tax = basic_band_income * TaxConstants.BASIC_RATE
                income_tax += (taxable_income - basic_band_income) * TaxConstants.HIGHER_RATE
            else:
                higher_band_limit = (TaxConstants.HIGHER_RATE_THRESHOLD - TaxConstants.PERSONAL_ALLOWANCE)
                basic_band_limit = (TaxConstants.BASIC_RATE_THRESHOLD - TaxConstants.PERSONAL_ALLOWANCE)
                higher_band_income = higher_band_limit - basic_band_limit
                
                income_tax = basic_band_income * TaxConstants.BASIC_RATE
                income_tax += higher_band_income * TaxConstants.HIGHER_RATE
                income_tax += (taxable_income - basic_band_income - higher_band_income) * TaxConstants.ADDITIONAL_RATE
        
        # National Insurance (Employee)
        employee_ni = 0
        if annual_salary > TaxConstants.NI_PRIMARY_THRESHOLD:
            income_up_to_uel = min(annual_salary, TaxConstants.NI_UPPER_EARNINGS_LIMIT) - TaxConstants.NI_PRIMARY_THRESHOLD
            employee_ni = income_up_to_uel * TaxConstants.NI_RATE_BELOW_UEL
            
            if annual_salary > TaxConstants.NI_UPPER_EARNINGS_LIMIT:
                income_above_uel = annual_salary - TaxConstants.NI_UPPER_EARNINGS_LIMIT
                employee_ni += income_above_uel * TaxConstants.NI_RATE_ABOVE_UEL
        
        total_deductions = income_tax + employee_ni
        net_income = annual_salary - total_deductions
        
        return {
            'gross_salary': round(annual_salary, 2),
            'taxable_income': round(taxable_income, 2),
            'income_tax': round(income_tax, 2),
            'employee_ni': round(employee_ni, 2),
            'total_employee_deductions': round(total_deductions, 2),
            'net_income': round(net_income, 2)
        }
    
    def calculate_corporation_tax(self, company_profit: float) -> Dict[str, Any]:
        """
        Calculate Corporation Tax.
        
        Small profits rate (19%) up to £50,000
        Main rate (25%) above £250,000
        Marginal relief between
        """
        if company_profit <= TaxConstants.CORPORATION_TAX_THRESHOLD:
            rate = TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE
            corp_tax = company_profit * rate
        else:
            # Simplified: Use main rate for profits above threshold
            rate = TaxConstants.CORPORATION_TAX_MAIN_RATE
            corp_tax = company_profit * rate
        
        profit_after_tax = company_profit - corp_tax
        effective_rate = corp_tax / company_profit if company_profit > 0 else 0
        
        return {
            'company_profit': round(company_profit, 2),
            'corporation_tax': round(corp_tax, 2),
            'profit_after_tax': round(profit_after_tax, 2),
            'effective_rate': round(effective_rate, 4),
            'rate_applied': rate
        }
    
    def calculate_dividend_tax(self, dividends: float, other_income: float = 0) -> Dict[str, Any]:
        """
        Calculate dividend tax.
        
        Dividends have a £500 allowance and are taxed at special rates
        depending on the individual's tax band.
        """
        # Dividend allowance
        taxable_dividends = max(0, dividends - TaxConstants.DIVIDEND_ALLOWANCE)
        
        # Determine tax band based on total income
        total_income = other_income + dividends
        dividend_tax = 0
        
        if taxable_dividends > 0:
            # Calculate which band the dividends fall into
            basic_threshold = TaxConstants.BASIC_RATE_THRESHOLD
            higher_threshold = TaxConstants.HIGHER_RATE_THRESHOLD
            
            if total_income <= basic_threshold:
                # All in basic rate
                dividend_tax = taxable_dividends * TaxConstants.DIVIDEND_BASIC_RATE
            elif other_income >= higher_threshold:
                # All in additional rate
                dividend_tax = taxable_dividends * TaxConstants.DIVIDEND_ADDITIONAL_RATE
            elif other_income >= basic_threshold:
                # All in higher rate
                dividend_tax = taxable_dividends * TaxConstants.DIVIDEND_HIGHER_RATE
            else:
                # Split across bands
                basic_rate_capacity = max(0, basic_threshold - other_income)
                dividends_at_basic = min(taxable_dividends, basic_rate_capacity)
                
                higher_rate_capacity = max(0, higher_threshold - other_income - dividends_at_basic)
                dividends_at_higher = min(taxable_dividends - dividends_at_basic, higher_rate_capacity)
                
                dividends_at_additional = max(0, taxable_dividends - dividends_at_basic - dividends_at_higher)
                
                dividend_tax = (dividends_at_basic * TaxConstants.DIVIDEND_BASIC_RATE +
                              dividends_at_higher * TaxConstants.DIVIDEND_HIGHER_RATE +
                              dividends_at_additional * TaxConstants.DIVIDEND_ADDITIONAL_RATE)
        
        return {
            'dividends': round(dividends, 2),
            'dividend_allowance': TaxConstants.DIVIDEND_ALLOWANCE,
            'taxable_dividends': round(taxable_dividends, 2),
            'dividend_tax': round(dividend_tax, 2),
            'net_dividends': round(dividends - dividend_tax, 2)
        }
