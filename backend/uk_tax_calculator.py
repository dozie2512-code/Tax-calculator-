"""
UK Tax Calculator - Comprehensive HMRC-compliant calculations
Covers PAYE, CGT, Company Tax, Withholding Tax, VAT, and various reliefs
Tax year 2024/2025
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime


class UKTaxCalculator:
    """
    Comprehensive UK tax calculator based on HMRC guidelines.
    Tax year 2024/2025 rates and thresholds.
    """
    
    # PAYE - Income Tax Rates and Thresholds (2024/2025)
    PERSONAL_ALLOWANCE = 12_570
    BASIC_RATE_THRESHOLD = 50_270
    HIGHER_RATE_THRESHOLD = 125_140
    
    BASIC_RATE = 0.20
    HIGHER_RATE = 0.40
    ADDITIONAL_RATE = 0.45
    
    # National Insurance Contributions (2024/2025)
    NI_PRIMARY_THRESHOLD = 12_570  # Annual
    NI_UPPER_EARNINGS_LIMIT = 50_270  # Annual
    NI_EMPLOYEE_RATE_STANDARD = 0.08  # Between PT and UEL
    NI_EMPLOYEE_RATE_ABOVE_UEL = 0.02  # Above UEL
    
    NI_EMPLOYER_THRESHOLD = 9_100  # Annual
    NI_EMPLOYER_RATE = 0.138
    
    # Capital Gains Tax (2024/2025)
    CGT_ANNUAL_EXEMPTION = 3_000
    CGT_BASIC_RATE = 0.10  # For gains within basic rate band
    CGT_HIGHER_RATE = 0.20  # For gains above basic rate band
    CGT_PROPERTY_BASIC_RATE = 0.18  # Residential property
    CGT_PROPERTY_HIGHER_RATE = 0.28  # Residential property
    
    # Corporation Tax (2024/2025)
    CORPORATION_TAX_SMALL_PROFITS_RATE = 0.19  # Up to £50,000
    CORPORATION_TAX_MAIN_RATE = 0.25  # Over £250,000
    CORPORATION_TAX_LOWER_LIMIT = 50_000
    CORPORATION_TAX_UPPER_LIMIT = 250_000
    
    # VAT (2024/2025)
    VAT_STANDARD_RATE = 0.20
    VAT_REDUCED_RATE = 0.05
    VAT_REGISTRATION_THRESHOLD = 90_000
    VAT_DEREGISTRATION_THRESHOLD = 88_000
    
    # Dividend Tax (2024/2025)
    DIVIDEND_ALLOWANCE = 500
    DIVIDEND_BASIC_RATE = 0.0875
    DIVIDEND_HIGHER_RATE = 0.3375
    DIVIDEND_ADDITIONAL_RATE = 0.3935
    
    def __init__(self):
        """Initialize the tax calculator."""
        self.tax_year = "2024/2025"
    
    def calculate_paye(self, annual_salary: float, 
                       include_ni: bool = True,
                       ni_category: str = 'A') -> Dict[str, Any]:
        """
        Calculate PAYE (Pay As You Earn) income tax and National Insurance.
        
        Args:
            annual_salary: Gross annual salary
            include_ni: Whether to include NI calculations
            ni_category: NI category (A, B, C, etc.)
            
        Returns:
            Dictionary with tax breakdown
        """
        # Calculate taxable income
        taxable_income = max(0, annual_salary - self.PERSONAL_ALLOWANCE)
        
        # Calculate income tax
        income_tax = 0
        
        if taxable_income > 0:
            # Basic rate band
            basic_band_income = min(taxable_income, 
                                   self.BASIC_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE)
            income_tax += basic_band_income * self.BASIC_RATE
            
            # Higher rate band
            if taxable_income > (self.BASIC_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE):
                higher_band_income = min(
                    taxable_income - basic_band_income,
                    self.HIGHER_RATE_THRESHOLD - self.BASIC_RATE_THRESHOLD
                )
                income_tax += higher_band_income * self.HIGHER_RATE
                
                # Additional rate band
                if taxable_income > (self.HIGHER_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE):
                    additional_band_income = taxable_income - basic_band_income - higher_band_income
                    income_tax += additional_band_income * self.ADDITIONAL_RATE
        
        # Calculate National Insurance
        employee_ni = 0
        employer_ni = 0
        
        if include_ni:
            # Employee NI
            if annual_salary > self.NI_PRIMARY_THRESHOLD:
                ni_between = min(annual_salary, self.NI_UPPER_EARNINGS_LIMIT) - self.NI_PRIMARY_THRESHOLD
                employee_ni += ni_between * self.NI_EMPLOYEE_RATE_STANDARD
                
                if annual_salary > self.NI_UPPER_EARNINGS_LIMIT:
                    ni_above = annual_salary - self.NI_UPPER_EARNINGS_LIMIT
                    employee_ni += ni_above * self.NI_EMPLOYEE_RATE_ABOVE_UEL
            
            # Employer NI
            if annual_salary > self.NI_EMPLOYER_THRESHOLD:
                employer_ni = (annual_salary - self.NI_EMPLOYER_THRESHOLD) * self.NI_EMPLOYER_RATE
        
        total_employee_deductions = income_tax + employee_ni
        net_salary = annual_salary - total_employee_deductions
        
        return {
            'gross_salary': annual_salary,
            'personal_allowance': self.PERSONAL_ALLOWANCE,
            'taxable_income': taxable_income,
            'income_tax': round(income_tax, 2),
            'employee_ni': round(employee_ni, 2),
            'employer_ni': round(employer_ni, 2),
            'total_employee_deductions': round(total_employee_deductions, 2),
            'net_salary': round(net_salary, 2),
            'effective_tax_rate': round((total_employee_deductions / annual_salary * 100), 2) if annual_salary > 0 else 0,
            'monthly_gross': round(annual_salary / 12, 2),
            'monthly_net': round(net_salary / 12, 2)
        }
    
    def calculate_cgt(self, capital_gains: float, 
                      annual_income: float,
                      is_property: bool = False) -> Dict[str, Any]:
        """
        Calculate Capital Gains Tax.
        
        Args:
            capital_gains: Total capital gains for the year
            annual_income: Annual income (to determine rate band)
            is_property: Whether gains are from residential property
            
        Returns:
            Dictionary with CGT breakdown
        """
        # Apply annual exemption
        taxable_gains = max(0, capital_gains - self.CGT_ANNUAL_EXEMPTION)
        
        if taxable_gains == 0:
            return {
                'capital_gains': capital_gains,
                'annual_exemption': self.CGT_ANNUAL_EXEMPTION,
                'taxable_gains': 0,
                'cgt_due': 0,
                'effective_rate': 0
            }
        
        # Determine which rate band to use
        remaining_basic_rate = max(0, self.BASIC_RATE_THRESHOLD - annual_income)
        
        cgt_due = 0
        
        if is_property:
            # Residential property rates
            if remaining_basic_rate > 0:
                gains_at_basic_rate = min(taxable_gains, remaining_basic_rate)
                cgt_due += gains_at_basic_rate * self.CGT_PROPERTY_BASIC_RATE
                
                if taxable_gains > remaining_basic_rate:
                    gains_at_higher_rate = taxable_gains - remaining_basic_rate
                    cgt_due += gains_at_higher_rate * self.CGT_PROPERTY_HIGHER_RATE
            else:
                cgt_due = taxable_gains * self.CGT_PROPERTY_HIGHER_RATE
        else:
            # Other assets rates
            if remaining_basic_rate > 0:
                gains_at_basic_rate = min(taxable_gains, remaining_basic_rate)
                cgt_due += gains_at_basic_rate * self.CGT_BASIC_RATE
                
                if taxable_gains > remaining_basic_rate:
                    gains_at_higher_rate = taxable_gains - remaining_basic_rate
                    cgt_due += gains_at_higher_rate * self.CGT_HIGHER_RATE
            else:
                cgt_due = taxable_gains * self.CGT_HIGHER_RATE
        
        return {
            'capital_gains': capital_gains,
            'annual_exemption': self.CGT_ANNUAL_EXEMPTION,
            'taxable_gains': taxable_gains,
            'cgt_due': round(cgt_due, 2),
            'effective_rate': round((cgt_due / capital_gains * 100), 2) if capital_gains > 0 else 0,
            'is_property': is_property
        }
    
    def calculate_corporation_tax(self, profit: float, 
                                   associated_companies: int = 0) -> Dict[str, Any]:
        """
        Calculate Corporation Tax for companies.
        
        Args:
            profit: Taxable profit for the year
            associated_companies: Number of associated companies (affects limits)
            
        Returns:
            Dictionary with corporation tax breakdown
        """
        # Adjust limits for associated companies
        divisor = associated_companies + 1
        lower_limit = self.CORPORATION_TAX_LOWER_LIMIT / divisor
        upper_limit = self.CORPORATION_TAX_UPPER_LIMIT / divisor
        
        if profit <= lower_limit:
            # Small profits rate
            corporation_tax = profit * self.CORPORATION_TAX_SMALL_PROFITS_RATE
            effective_rate = self.CORPORATION_TAX_SMALL_PROFITS_RATE * 100
            band = "Small Profits Rate"
        elif profit >= upper_limit:
            # Main rate
            corporation_tax = profit * self.CORPORATION_TAX_MAIN_RATE
            effective_rate = self.CORPORATION_TAX_MAIN_RATE * 100
            band = "Main Rate"
        else:
            # Marginal relief (tapered rate between limits)
            main_rate_tax = profit * self.CORPORATION_TAX_MAIN_RATE
            marginal_relief_fraction = 0.015  # Standard fraction
            marginal_relief = (upper_limit - profit) * marginal_relief_fraction * (profit / profit)
            corporation_tax = main_rate_tax - marginal_relief
            effective_rate = (corporation_tax / profit * 100) if profit > 0 else 0
            band = "Marginal Relief"
        
        return {
            'taxable_profit': profit,
            'associated_companies': associated_companies,
            'lower_limit': lower_limit,
            'upper_limit': upper_limit,
            'corporation_tax': round(corporation_tax, 2),
            'effective_rate': round(effective_rate, 2),
            'band': band,
            'profit_after_tax': round(profit - corporation_tax, 2)
        }
    
    def calculate_dividend_tax(self, dividends: float, 
                               other_income: float = 0) -> Dict[str, Any]:
        """
        Calculate dividend tax.
        
        Args:
            dividends: Dividend income for the year
            other_income: Other taxable income (to determine rate band)
            
        Returns:
            Dictionary with dividend tax breakdown
        """
        # Apply dividend allowance
        taxable_dividends = max(0, dividends - self.DIVIDEND_ALLOWANCE)
        
        if taxable_dividends == 0:
            return {
                'dividends': dividends,
                'dividend_allowance': self.DIVIDEND_ALLOWANCE,
                'taxable_dividends': 0,
                'dividend_tax': 0,
                'effective_rate': 0
            }
        
        # Calculate tax based on income bands
        total_income = other_income + dividends
        dividend_tax = 0
        
        # Determine which bands the dividends fall into
        basic_rate_remaining = max(0, self.BASIC_RATE_THRESHOLD - other_income)
        higher_rate_remaining = max(0, self.HIGHER_RATE_THRESHOLD - max(other_income, self.BASIC_RATE_THRESHOLD))
        
        dividends_to_tax = taxable_dividends
        
        # Basic rate band
        if basic_rate_remaining > 0 and dividends_to_tax > 0:
            basic_rate_dividends = min(dividends_to_tax, basic_rate_remaining)
            dividend_tax += basic_rate_dividends * self.DIVIDEND_BASIC_RATE
            dividends_to_tax -= basic_rate_dividends
        
        # Higher rate band
        if higher_rate_remaining > 0 and dividends_to_tax > 0:
            higher_rate_dividends = min(dividends_to_tax, higher_rate_remaining)
            dividend_tax += higher_rate_dividends * self.DIVIDEND_HIGHER_RATE
            dividends_to_tax -= higher_rate_dividends
        
        # Additional rate band
        if dividends_to_tax > 0:
            dividend_tax += dividends_to_tax * self.DIVIDEND_ADDITIONAL_RATE
        
        return {
            'dividends': dividends,
            'dividend_allowance': self.DIVIDEND_ALLOWANCE,
            'taxable_dividends': taxable_dividends,
            'dividend_tax': round(dividend_tax, 2),
            'effective_rate': round((dividend_tax / dividends * 100), 2) if dividends > 0 else 0
        }
    
    def calculate_vat(self, turnover: float, 
                      expenses: float = 0,
                      scheme: str = 'standard') -> Dict[str, Any]:
        """
        Calculate VAT liability.
        
        Args:
            turnover: Total turnover including VAT
            expenses: Total expenses including VAT
            scheme: VAT scheme ('standard', 'flat_rate', 'cash_accounting')
            
        Returns:
            Dictionary with VAT breakdown
        """
        # Check if VAT registration is required
        vat_registered = turnover >= self.VAT_REGISTRATION_THRESHOLD
        
        if not vat_registered:
            return {
                'turnover': turnover,
                'vat_registered': False,
                'vat_threshold': self.VAT_REGISTRATION_THRESHOLD,
                'vat_due': 0,
                'message': 'Below VAT registration threshold'
            }
        
        # Calculate VAT under standard accounting
        turnover_ex_vat = turnover / (1 + self.VAT_STANDARD_RATE)
        expenses_ex_vat = expenses / (1 + self.VAT_STANDARD_RATE)
        
        output_vat = turnover_ex_vat * self.VAT_STANDARD_RATE
        input_vat = expenses_ex_vat * self.VAT_STANDARD_RATE
        vat_due = output_vat - input_vat
        
        return {
            'turnover': turnover,
            'turnover_ex_vat': round(turnover_ex_vat, 2),
            'expenses': expenses,
            'expenses_ex_vat': round(expenses_ex_vat, 2),
            'output_vat': round(output_vat, 2),
            'input_vat': round(input_vat, 2),
            'vat_due': round(vat_due, 2),
            'vat_rate': self.VAT_STANDARD_RATE * 100,
            'scheme': scheme,
            'vat_registered': vat_registered
        }


class TaxReliefs:
    """
    Calculate various UK tax reliefs and allowances.
    """
    
    # Trading Allowance
    TRADING_ALLOWANCE = 1_000
    
    # Property Allowance
    PROPERTY_ALLOWANCE = 1_000
    
    # Marriage Allowance
    MARRIAGE_ALLOWANCE_TRANSFER = 1_260
    
    # Pension Contributions (annual allowance)
    PENSION_ANNUAL_ALLOWANCE = 60_000
    
    # Gift Aid
    GIFT_AID_RATE = 0.25  # 25% relief
    
    def calculate_pension_relief(self, pension_contribution: float,
                                  annual_income: float) -> Dict[str, Any]:
        """
        Calculate pension contribution tax relief.
        
        Args:
            pension_contribution: Annual pension contribution
            annual_income: Annual income
            
        Returns:
            Dictionary with pension relief breakdown
        """
        # Check against annual allowance
        contribution_within_allowance = min(pension_contribution, self.PENSION_ANNUAL_ALLOWANCE)
        
        # Basic rate relief (20%) is usually claimed at source
        basic_rate_relief = contribution_within_allowance * 0.20
        
        # Higher/additional rate relief can be claimed through tax return
        higher_rate_relief = 0
        if annual_income > 50_270:
            if annual_income <= 125_140:
                # Higher rate taxpayer
                higher_rate_relief = contribution_within_allowance * 0.20  # Additional 20%
            else:
                # Additional rate taxpayer
                higher_rate_relief = contribution_within_allowance * 0.25  # Additional 25%
        
        total_relief = basic_rate_relief + higher_rate_relief
        
        return {
            'pension_contribution': pension_contribution,
            'contribution_within_allowance': contribution_within_allowance,
            'basic_rate_relief': round(basic_rate_relief, 2),
            'higher_rate_relief': round(higher_rate_relief, 2),
            'total_relief': round(total_relief, 2),
            'annual_allowance': self.PENSION_ANNUAL_ALLOWANCE
        }
    
    def calculate_gift_aid_relief(self, donation: float) -> Dict[str, Any]:
        """
        Calculate Gift Aid relief.
        
        Args:
            donation: Donation amount
            
        Returns:
            Dictionary with Gift Aid breakdown
        """
        # Charity receives 25% on top
        gift_aid_value = donation * self.GIFT_AID_RATE
        total_to_charity = donation + gift_aid_value
        
        return {
            'donation': donation,
            'gift_aid_value': round(gift_aid_value, 2),
            'total_to_charity': round(total_to_charity, 2),
            'relief_rate': self.GIFT_AID_RATE * 100
        }
    
    def calculate_trading_allowance(self, trading_income: float) -> Dict[str, Any]:
        """
        Calculate trading allowance.
        
        Args:
            trading_income: Trading income
            
        Returns:
            Dictionary with trading allowance
        """
        allowance_used = min(trading_income, self.TRADING_ALLOWANCE)
        taxable_income = max(0, trading_income - allowance_used)
        
        return {
            'trading_income': trading_income,
            'allowance_used': allowance_used,
            'taxable_income': taxable_income,
            'trading_allowance': self.TRADING_ALLOWANCE
        }
    
    def calculate_property_allowance(self, property_income: float) -> Dict[str, Any]:
        """
        Calculate property allowance.
        
        Args:
            property_income: Property rental income
            
        Returns:
            Dictionary with property allowance
        """
        allowance_used = min(property_income, self.PROPERTY_ALLOWANCE)
        taxable_income = max(0, property_income - allowance_used)
        
        return {
            'property_income': property_income,
            'allowance_used': allowance_used,
            'taxable_income': taxable_income,
            'property_allowance': self.PROPERTY_ALLOWANCE
        }
