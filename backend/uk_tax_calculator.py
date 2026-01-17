"""
UK Tax Calculator Module
Provides comprehensive tax calculation functionality for UK tax system.
Includes PAYE, NI, dividend tax, corporation tax, and various tax reliefs.
"""

from typing import Dict, Any


class TaxConstants:
    """
    UK Tax Constants for 2025/2026 tax year.
    Centralizes all tax thresholds, rates, and allowances.
    """
    
    # Income Tax Allowances and Thresholds
    PERSONAL_ALLOWANCE = 12_570
    BASIC_RATE_THRESHOLD = 50_270
    HIGHER_RATE_THRESHOLD = 150_000
    
    # Income Tax Rates
    BASIC_RATE = 0.20
    HIGHER_RATE = 0.40
    ADDITIONAL_RATE = 0.45
    
    # National Insurance Thresholds (Annual)
    NI_PRIMARY_THRESHOLD = 12_570  # Lower Earnings Limit for Class 1
    NI_UPPER_EARNINGS_LIMIT = 50_270
    
    # National Insurance Rates
    NI_RATE_BELOW_UEL = 0.08  # Employee Class 1 rate below UEL
    NI_RATE_ABOVE_UEL = 0.02  # Employee Class 1 rate above UEL
    
    # Corporation Tax
    CORPORATION_TAX_RATE = 0.19
    CORPORATION_TAX_SMALL_PROFITS_RATE = 0.19
    CORPORATION_TAX_MAIN_RATE = 0.25
    CORPORATION_TAX_THRESHOLD = 50_000
    CORPORATION_TAX_UPPER_LIMIT = 250_000
    
    # Dividend Tax
    DIVIDEND_ALLOWANCE = 500
    DIVIDEND_BASIC_RATE = 0.0875
    DIVIDEND_HIGHER_RATE = 0.3375
    DIVIDEND_ADDITIONAL_RATE = 0.3935
    
    # Capital Gains Tax
    CGT_ANNUAL_ALLOWANCE = 3_000
    CGT_BASIC_RATE = 0.10
    CGT_HIGHER_RATE = 0.20
    
    # Pension Allowances
    PENSION_ANNUAL_ALLOWANCE = 60_000
    PENSION_LIFETIME_ALLOWANCE = 1_073_100
    
    # Business Allowances
    TRADING_ALLOWANCE = 1_000
    PROPERTY_ALLOWANCE = 1_000
    
    # Capital Allowances
    ANNUAL_INVESTMENT_ALLOWANCE = 1_000_000
    FIRST_YEAR_ALLOWANCE_RATE = 1.00  # 100%
    
    # National Insurance Class 2 (Self-Employed)
    CLASS_2_NI_WEEKLY_RATE = 3.45
    CLASS_2_NI_SMALL_PROFITS_THRESHOLD = 6_725


class UKTaxCalculator:
    """
    Main UK Tax Calculator.
    Provides methods for calculating various UK taxes.
    """
    
    def __init__(self):
        """Initialize calculator with current tax constants."""
        self.constants = TaxConstants()
        # Expose commonly used constants as instance attributes for backward compatibility
        self.PERSONAL_ALLOWANCE = TaxConstants.PERSONAL_ALLOWANCE
        self.BASIC_RATE_THRESHOLD = TaxConstants.BASIC_RATE_THRESHOLD
        self.HIGHER_RATE_THRESHOLD = TaxConstants.HIGHER_RATE_THRESHOLD
        self.BASIC_RATE = TaxConstants.BASIC_RATE
        self.HIGHER_RATE = TaxConstants.HIGHER_RATE
        self.ADDITIONAL_RATE = TaxConstants.ADDITIONAL_RATE
        self.DIVIDEND_ALLOWANCE = TaxConstants.DIVIDEND_ALLOWANCE
        self.DIVIDEND_BASIC_RATE = TaxConstants.DIVIDEND_BASIC_RATE
        self.DIVIDEND_HIGHER_RATE = TaxConstants.DIVIDEND_HIGHER_RATE
        self.DIVIDEND_ADDITIONAL_RATE = TaxConstants.DIVIDEND_ADDITIONAL_RATE
    
    def calculate_paye(self, annual_income: float) -> Dict[str, Any]:
        """
        Calculate PAYE (Pay As You Earn) income tax and National Insurance.
        
        Args:
            annual_income: Gross annual income/salary
            
        Returns:
            Dictionary containing:
                - income_tax: Annual income tax
                - employee_ni: Annual employee National Insurance
                - total_employee_deductions: Total tax + NI
                - net_income: Income after deductions
                - taxable_income: Income subject to tax
                - tax_breakdown: Detailed breakdown by band
                
        Raises:
            ValueError: If annual_income is negative
        """
        if annual_income < 0:
            raise ValueError("Annual income cannot be negative")
        
        # Calculate taxable income (after personal allowance)
        taxable_income = max(0, annual_income - self.constants.PERSONAL_ALLOWANCE)
        
        # Calculate income tax by bands
        income_tax = 0
        tax_breakdown = {
            'basic_rate_income': 0,
            'higher_rate_income': 0,
            'additional_rate_income': 0,
            'basic_rate_tax': 0,
            'higher_rate_tax': 0,
            'additional_rate_tax': 0
        }
        
        if taxable_income > 0:
            # Basic rate band (£0 - £37,700 of taxable income)
            basic_band_limit = self.constants.BASIC_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE
            basic_rate_income = min(taxable_income, basic_band_limit)
            basic_rate_tax = basic_rate_income * self.constants.BASIC_RATE
            income_tax += basic_rate_tax
            tax_breakdown['basic_rate_income'] = basic_rate_income
            tax_breakdown['basic_rate_tax'] = basic_rate_tax
            
            # Higher rate band (£37,701 - £125,000 of taxable income)
            if taxable_income > basic_band_limit:
                higher_band_limit = self.constants.HIGHER_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE
                higher_rate_income = min(taxable_income - basic_band_limit, higher_band_limit - basic_band_limit)
                higher_rate_tax = higher_rate_income * self.constants.HIGHER_RATE
                income_tax += higher_rate_tax
                tax_breakdown['higher_rate_income'] = higher_rate_income
                tax_breakdown['higher_rate_tax'] = higher_rate_tax
            
            # Additional rate band (over £125,000 of taxable income)
            if taxable_income > (self.constants.HIGHER_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE):
                additional_rate_income = taxable_income - (self.constants.HIGHER_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE)
                additional_rate_tax = additional_rate_income * self.constants.ADDITIONAL_RATE
                income_tax += additional_rate_tax
                tax_breakdown['additional_rate_income'] = additional_rate_income
                tax_breakdown['additional_rate_tax'] = additional_rate_tax
        
        # Calculate National Insurance (Class 1 Employee)
        employee_ni = self._calculate_employee_ni(annual_income)
        
        # Calculate totals
        total_deductions = income_tax + employee_ni
        net_income = annual_income - total_deductions
        
        return {
            'income_tax': round(income_tax, 2),
            'employee_ni': round(employee_ni, 2),
            'total_employee_deductions': round(total_deductions, 2),
            'net_income': round(net_income, 2),
            'taxable_income': round(taxable_income, 2),
            'gross_income': annual_income,
            'tax_breakdown': tax_breakdown
        }
    
    def _calculate_employee_ni(self, annual_income: float) -> float:
        """
        Calculate employee National Insurance contributions.
        
        Args:
            annual_income: Gross annual income
            
        Returns:
            Annual employee NI contributions
        """
        employee_ni = 0
        
        if annual_income > self.constants.NI_PRIMARY_THRESHOLD:
            # Income between primary threshold and upper earnings limit
            income_below_uel = min(annual_income, self.constants.NI_UPPER_EARNINGS_LIMIT) - self.constants.NI_PRIMARY_THRESHOLD
            if income_below_uel > 0:
                employee_ni += income_below_uel * self.constants.NI_RATE_BELOW_UEL
            
            # Income above upper earnings limit
            if annual_income > self.constants.NI_UPPER_EARNINGS_LIMIT:
                income_above_uel = annual_income - self.constants.NI_UPPER_EARNINGS_LIMIT
                employee_ni += income_above_uel * self.constants.NI_RATE_ABOVE_UEL
        
        return employee_ni
    
    def calculate_dividend_tax(self, dividend_amount: float, other_income: float = 0) -> Dict[str, Any]:
        """
        Calculate dividend tax.
        Dividends are taxed after other income, at special dividend rates.
        
        Args:
            dividend_amount: Total dividend income
            other_income: Other income (salary, etc.) that uses up tax bands first
            
        Returns:
            Dictionary containing:
                - dividend_tax: Total dividend tax
                - taxable_dividends: Dividends above allowance
                - dividend_allowance_used: Amount of dividend allowance used
                - dividend_breakdown: Tax by rate band
                
        Raises:
            ValueError: If dividend_amount or other_income is negative
        """
        if dividend_amount < 0:
            raise ValueError("Dividend amount cannot be negative")
        if other_income < 0:
            raise ValueError("Other income cannot be negative")
        
        # Apply dividend allowance
        dividend_allowance_used = min(dividend_amount, self.constants.DIVIDEND_ALLOWANCE)
        taxable_dividends = max(0, dividend_amount - dividend_allowance_used)
        
        if taxable_dividends == 0:
            return {
                'dividend_tax': 0,
                'taxable_dividends': 0,
                'dividend_allowance_used': dividend_allowance_used,
                'dividend_breakdown': {
                    'basic_rate': 0,
                    'higher_rate': 0,
                    'additional_rate': 0
                }
            }
        
        # Calculate tax based on which bands the dividends fall into
        # Dividends use remaining capacity in each tax band after other income
        dividend_tax = 0
        dividend_breakdown = {
            'basic_rate': 0,
            'higher_rate': 0,
            'additional_rate': 0
        }
        
        # Determine how much of each band is available
        taxable_other_income = max(0, other_income - self.constants.PERSONAL_ALLOWANCE)
        
        # Basic rate band capacity
        basic_band_limit = self.constants.BASIC_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE
        basic_band_used = min(taxable_other_income, basic_band_limit)
        basic_band_available = max(0, basic_band_limit - basic_band_used)
        
        # Dividends in basic rate band
        dividends_at_basic = min(taxable_dividends, basic_band_available)
        if dividends_at_basic > 0:
            dividend_tax += dividends_at_basic * self.constants.DIVIDEND_BASIC_RATE
            dividend_breakdown['basic_rate'] = dividends_at_basic
        
        # Higher rate band capacity
        higher_band_limit = self.constants.HIGHER_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE
        higher_band_used = max(0, min(taxable_other_income, higher_band_limit) - basic_band_limit)
        higher_band_available = max(0, higher_band_limit - basic_band_limit - higher_band_used)
        
        # Dividends in higher rate band
        remaining_dividends = taxable_dividends - dividends_at_basic
        dividends_at_higher = min(remaining_dividends, higher_band_available)
        if dividends_at_higher > 0:
            dividend_tax += dividends_at_higher * self.constants.DIVIDEND_HIGHER_RATE
            dividend_breakdown['higher_rate'] = dividends_at_higher
        
        # Dividends in additional rate band
        dividends_at_additional = remaining_dividends - dividends_at_higher
        if dividends_at_additional > 0:
            dividend_tax += dividends_at_additional * self.constants.DIVIDEND_ADDITIONAL_RATE
            dividend_breakdown['additional_rate'] = dividends_at_additional
        
        return {
            'dividend_tax': round(dividend_tax, 2),
            'taxable_dividends': round(taxable_dividends, 2),
            'dividend_allowance_used': dividend_allowance_used,
            'dividend_breakdown': dividend_breakdown
        }
    
    def calculate_corporation_tax(self, taxable_profit: float) -> Dict[str, Any]:
        """
        Calculate corporation tax.
        Uses marginal relief for profits between £50k and £250k.
        
        Args:
            taxable_profit: Company's taxable profit
            
        Returns:
            Dictionary containing:
                - corporation_tax: Total corporation tax
                - profit_after_tax: Profit remaining after tax
                - effective_rate: Effective tax rate
                - rate_used: Tax rate applied
                
        Raises:
            ValueError: If taxable_profit is negative
        """
        if taxable_profit < 0:
            raise ValueError("Taxable profit cannot be negative")
        
        if taxable_profit == 0:
            return {
                'corporation_tax': 0,
                'profit_after_tax': 0,
                'effective_rate': 0,
                'rate_used': 0
            }
        
        # Determine tax rate and calculate tax
        if taxable_profit <= self.constants.CORPORATION_TAX_THRESHOLD:
            # Small profits rate (19%)
            rate_used = self.constants.CORPORATION_TAX_SMALL_PROFITS_RATE
            corporation_tax = taxable_profit * rate_used
        elif taxable_profit >= self.constants.CORPORATION_TAX_UPPER_LIMIT:
            # Main rate (25%)
            rate_used = self.constants.CORPORATION_TAX_MAIN_RATE
            corporation_tax = taxable_profit * rate_used
        else:
            # Marginal relief applies (between £50k and £250k)
            # Effective rate gradually increases from 19% to 25%
            main_rate_tax = taxable_profit * self.constants.CORPORATION_TAX_MAIN_RATE
            
            # Marginal relief calculation
            # Relief = (Upper Limit - Profit) × (Profit ÷ Profit) × Marginal Relief Fraction
            # Marginal Relief Fraction = 3/200 = 0.015
            marginal_relief_fraction = 0.015
            marginal_relief = (self.constants.CORPORATION_TAX_UPPER_LIMIT - taxable_profit) * marginal_relief_fraction
            
            corporation_tax = main_rate_tax - marginal_relief
            rate_used = corporation_tax / taxable_profit
        
        profit_after_tax = taxable_profit - corporation_tax
        effective_rate = (corporation_tax / taxable_profit) if taxable_profit > 0 else 0
        
        return {
            'corporation_tax': round(corporation_tax, 2),
            'profit_after_tax': round(profit_after_tax, 2),
            'effective_rate': round(effective_rate, 4),
            'rate_used': round(rate_used, 4)
        }


class TaxReliefs:
    """
    UK Tax Reliefs and Allowances.
    Provides calculations for various tax reliefs available in the UK.
    """
    
    def __init__(self):
        """Initialize with current tax relief constants."""
        self.constants = TaxConstants()
        # Expose commonly used constants as instance attributes for backward compatibility
        self.PENSION_ANNUAL_ALLOWANCE = TaxConstants.PENSION_ANNUAL_ALLOWANCE
        self.TRADING_ALLOWANCE = TaxConstants.TRADING_ALLOWANCE
        self.PROPERTY_ALLOWANCE = TaxConstants.PROPERTY_ALLOWANCE
    
    def calculate_pension_relief(self, contribution: float, income: float) -> Dict[str, Any]:
        """
        Calculate pension contribution tax relief.
        
        Args:
            contribution: Pension contribution amount
            income: Annual income
            
        Returns:
            Dictionary containing:
                - basic_rate_relief: 20% relief (paid automatically)
                - higher_rate_relief: Additional relief for higher rate taxpayers
                - additional_rate_relief: Additional relief for additional rate taxpayers
                - total_relief: Total tax relief
                - effective_contribution: Net cost after relief
                
        Raises:
            ValueError: If contribution or income is negative
            ValueError: If contribution exceeds annual allowance
        """
        if contribution < 0:
            raise ValueError("Pension contribution cannot be negative")
        if income < 0:
            raise ValueError("Income cannot be negative")
        if contribution > self.constants.PENSION_ANNUAL_ALLOWANCE:
            raise ValueError(f"Contribution exceeds annual allowance of £{self.constants.PENSION_ANNUAL_ALLOWANCE:,}")
        
        # Basic rate relief (20%) - automatically added by pension provider
        basic_rate_relief = contribution * self.constants.BASIC_RATE
        
        # Calculate taxable income
        taxable_income = max(0, income - self.constants.PERSONAL_ALLOWANCE)
        
        # Higher rate relief (additional 20% for 40% taxpayers)
        higher_rate_relief = 0
        basic_band_limit = self.constants.BASIC_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE
        if taxable_income > basic_band_limit:
            # Income in higher rate band
            higher_rate_income = min(taxable_income - basic_band_limit, 
                                    self.constants.HIGHER_RATE_THRESHOLD - self.constants.BASIC_RATE_THRESHOLD)
            # Relief on contribution that would have been taxed at higher rate
            contribution_at_higher = min(contribution, higher_rate_income)
            higher_rate_relief = contribution_at_higher * (self.constants.HIGHER_RATE - self.constants.BASIC_RATE)
        
        # Additional rate relief (additional 25% for 45% taxpayers)
        additional_rate_relief = 0
        if taxable_income > (self.constants.HIGHER_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE):
            # Income in additional rate band
            additional_rate_income = taxable_income - (self.constants.HIGHER_RATE_THRESHOLD - self.constants.PERSONAL_ALLOWANCE)
            # Relief on contribution that would have been taxed at additional rate
            contribution_at_additional = min(contribution, additional_rate_income)
            additional_rate_relief = contribution_at_additional * (self.constants.ADDITIONAL_RATE - self.constants.BASIC_RATE)
        
        total_relief = basic_rate_relief + higher_rate_relief + additional_rate_relief
        effective_contribution = contribution - total_relief
        
        return {
            'basic_rate_relief': round(basic_rate_relief, 2),
            'higher_rate_relief': round(higher_rate_relief, 2),
            'additional_rate_relief': round(additional_rate_relief, 2),
            'total_relief': round(total_relief, 2),
            'effective_contribution': round(effective_contribution, 2),
            'gross_contribution': contribution
        }
    
    def calculate_trading_allowance(self, trading_income: float) -> Dict[str, Any]:
        """
        Calculate trading allowance benefit.
        Trading allowance allows £1,000 tax-free trading income.
        
        Args:
            trading_income: Gross trading income
            
        Returns:
            Dictionary containing:
                - allowance_available: Trading allowance amount
                - taxable_income: Income after allowance
                - benefit: Tax saved vs no allowance
                
        Raises:
            ValueError: If trading_income is negative
        """
        if trading_income < 0:
            raise ValueError("Trading income cannot be negative")
        
        allowance_available = min(trading_income, self.constants.TRADING_ALLOWANCE)
        taxable_income = max(0, trading_income - allowance_available)
        
        # Benefit is the tax saved on the allowance (at basic rate minimum)
        benefit = allowance_available * self.constants.BASIC_RATE
        
        return {
            'allowance_available': allowance_available,
            'taxable_income': round(taxable_income, 2),
            'benefit': round(benefit, 2),
            'allowance_limit': self.constants.TRADING_ALLOWANCE
        }
    
    def calculate_property_allowance(self, rental_income: float) -> Dict[str, Any]:
        """
        Calculate property allowance benefit.
        Property allowance allows £1,000 tax-free rental income.
        
        Args:
            rental_income: Gross rental income
            
        Returns:
            Dictionary containing:
                - allowance_available: Property allowance amount
                - taxable_income: Income after allowance
                - benefit: Tax saved vs no allowance
                
        Raises:
            ValueError: If rental_income is negative
        """
        if rental_income < 0:
            raise ValueError("Rental income cannot be negative")
        
        allowance_available = min(rental_income, self.constants.PROPERTY_ALLOWANCE)
        taxable_income = max(0, rental_income - allowance_available)
        
        # Benefit is the tax saved on the allowance (at basic rate minimum)
        benefit = allowance_available * self.constants.BASIC_RATE
        
        return {
            'allowance_available': allowance_available,
            'taxable_income': round(taxable_income, 2),
            'benefit': round(benefit, 2),
            'allowance_limit': self.constants.PROPERTY_ALLOWANCE
        }
