"""
UK Tax Calculator Module

This module provides comprehensive UK tax calculations for:
1. PAYE (Pay As You Earn) - Employee income tax
2. Self Assessment - Self-employed and multiple income sources
3. Corporate Tax - Business tax calculations

All calculations use current UK tax rates and thresholds.
"""

from typing import Dict, List, Any, Optional
from decimal import Decimal, ROUND_HALF_UP


class ValidationError(Exception):
    """Custom exception for input validation errors"""
    pass


class PAYECalculator:
    """
    Calculate PAYE (Pay As You Earn) income tax for UK employees.
    
    Uses 2024/25 tax year rates:
    - Personal Allowance: £12,570
    - Basic Rate (20%): £12,571 to £50,270
    - Higher Rate (40%): £50,271 to £150,000
    - Additional Rate (45%): over £150,000
    """
    
    # Tax year 2024/25 constants
    PERSONAL_ALLOWANCE = Decimal('12570')
    BASIC_RATE_THRESHOLD = Decimal('50270')
    HIGHER_RATE_THRESHOLD = Decimal('150000')
    
    BASIC_RATE = Decimal('0.20')
    HIGHER_RATE = Decimal('0.40')
    ADDITIONAL_RATE = Decimal('0.45')
    
    def __init__(self):
        """Initialize PAYE calculator"""
        pass
    
    def validate_inputs(self, gross_income: float, deductions: float = 0) -> None:
        """
        Validate input values for PAYE calculation.
        
        Args:
            gross_income: Annual gross income
            deductions: Additional deductions (pension contributions, etc.)
            
        Raises:
            ValidationError: If inputs are invalid
        """
        if gross_income < 0:
            raise ValidationError("Gross income cannot be negative")
        if deductions < 0:
            raise ValidationError("Deductions cannot be negative")
        if deductions > gross_income:
            raise ValidationError("Deductions cannot exceed gross income")
    
    def calculate(self, gross_income: float, deductions: float = 0) -> Dict[str, Any]:
        """
        Calculate PAYE income tax.
        
        Args:
            gross_income: Annual gross income in GBP
            deductions: Additional deductions (e.g., pension contributions) in GBP
            
        Returns:
            Dictionary containing:
                - gross_income: Original gross income
                - deductions: Applied deductions
                - taxable_income: Income after deductions and personal allowance
                - personal_allowance: Personal allowance amount
                - tax_breakdown: Tax by band (basic, higher, additional)
                - total_tax: Total PAYE tax
                - net_income: Income after tax
                
        Raises:
            ValidationError: If inputs are invalid
        """
        # Validate inputs
        self.validate_inputs(gross_income, deductions)
        
        # Convert to Decimal for precise calculations
        gross = Decimal(str(gross_income))
        deduct = Decimal(str(deductions))
        
        # Calculate adjusted income (after deductions but before personal allowance)
        adjusted_income = gross - deduct
        
        # Personal allowance tapers off for high earners (£1 for every £2 over £100,000)
        personal_allowance = self.PERSONAL_ALLOWANCE
        if adjusted_income > Decimal('100000'):
            reduction = (adjusted_income - Decimal('100000')) / 2
            personal_allowance = max(Decimal('0'), personal_allowance - reduction)
        
        # Calculate taxable income
        taxable_income = max(Decimal('0'), adjusted_income - personal_allowance)
        
        # Calculate tax by bands
        tax_breakdown = {
            'basic_rate': Decimal('0'),
            'higher_rate': Decimal('0'),
            'additional_rate': Decimal('0')
        }
        
        total_tax = Decimal('0')
        
        if taxable_income > 0:
            # Basic rate band
            basic_band_limit = self.BASIC_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE
            basic_taxable = min(taxable_income, basic_band_limit)
            if basic_taxable > 0:
                tax_breakdown['basic_rate'] = (basic_taxable * self.BASIC_RATE).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
                total_tax += tax_breakdown['basic_rate']
            
            # Higher rate band
            if taxable_income > basic_band_limit:
                higher_band_limit = self.HIGHER_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE
                higher_taxable = min(taxable_income - basic_band_limit, higher_band_limit - basic_band_limit)
                if higher_taxable > 0:
                    tax_breakdown['higher_rate'] = (higher_taxable * self.HIGHER_RATE).quantize(
                        Decimal('0.01'), rounding=ROUND_HALF_UP
                    )
                    total_tax += tax_breakdown['higher_rate']
            
            # Additional rate band
            if taxable_income > (self.HIGHER_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE):
                additional_taxable = taxable_income - (self.HIGHER_RATE_THRESHOLD - self.PERSONAL_ALLOWANCE)
                tax_breakdown['additional_rate'] = (additional_taxable * self.ADDITIONAL_RATE).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
                total_tax += tax_breakdown['additional_rate']
        
        net_income = gross - total_tax
        
        return {
            'gross_income': float(gross),
            'deductions': float(deduct),
            'personal_allowance': float(personal_allowance),
            'taxable_income': float(taxable_income),
            'tax_breakdown': {
                'basic_rate': float(tax_breakdown['basic_rate']),
                'higher_rate': float(tax_breakdown['higher_rate']),
                'additional_rate': float(tax_breakdown['additional_rate'])
            },
            'total_tax': float(total_tax),
            'net_income': float(net_income)
        }


class SelfAssessmentCalculator:
    """
    Calculate Self Assessment tax for self-employed individuals and those with
    multiple income sources.
    
    Handles:
    - Employment income (PAYE)
    - Self-employment income
    - Property/rental income
    - Investment income
    - Pension contributions
    - Charitable donations
    """
    
    def __init__(self):
        """Initialize Self Assessment calculator"""
        self.paye_calculator = PAYECalculator()
    
    def validate_inputs(self, income_sources: List[Dict[str, float]], 
                       deductions: Dict[str, float]) -> None:
        """
        Validate input values for Self Assessment calculation.
        
        Args:
            income_sources: List of income source dictionaries
            deductions: Dictionary of deductions
            
        Raises:
            ValidationError: If inputs are invalid
        """
        if not income_sources:
            raise ValidationError("At least one income source must be provided")
        
        for source in income_sources:
            if 'type' not in source or 'amount' not in source:
                raise ValidationError("Each income source must have 'type' and 'amount' keys")
            if source['amount'] < 0:
                raise ValidationError(f"Income amount cannot be negative for {source['type']}")
        
        valid_deduction_types = ['pension', 'charity', 'trading_losses', 'other']
        for deduction_type, amount in deductions.items():
            if deduction_type not in valid_deduction_types:
                raise ValidationError(f"Invalid deduction type: {deduction_type}")
            if amount < 0:
                raise ValidationError(f"Deduction amount cannot be negative for {deduction_type}")
    
    def calculate(self, income_sources: List[Dict[str, float]], 
                 deductions: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Calculate Self Assessment tax with multiple income sources.
        
        Args:
            income_sources: List of dictionaries with 'type' and 'amount' keys
                          Types: 'employment', 'self_employment', 'property', 'investment'
            deductions: Dictionary of deductions with keys:
                       'pension', 'charity', 'trading_losses', 'other'
        
        Returns:
            Dictionary containing:
                - total_income: Sum of all income sources
                - income_breakdown: Breakdown by income type
                - total_deductions: Sum of all deductions
                - deductions_breakdown: Breakdown by deduction type
                - taxable_income: Total taxable income
                - tax_calculation: Detailed tax calculation
                - total_tax: Total tax liability
                - net_income: Income after tax
                
        Raises:
            ValidationError: If inputs are invalid
        """
        if deductions is None:
            deductions = {}
        
        # Validate inputs
        self.validate_inputs(income_sources, deductions)
        
        # Calculate total income
        income_breakdown = {}
        total_income = Decimal('0')
        
        for source in income_sources:
            income_type = source['type']
            amount = Decimal(str(source['amount']))
            
            if income_type not in income_breakdown:
                income_breakdown[income_type] = Decimal('0')
            
            income_breakdown[income_type] += amount
            total_income += amount
        
        # Calculate total deductions
        deductions_breakdown = {}
        total_deductions = Decimal('0')
        
        for deduction_type, amount in deductions.items():
            deduction_amount = Decimal(str(amount))
            deductions_breakdown[deduction_type] = deduction_amount
            total_deductions += deduction_amount
        
        # Use PAYE calculator for tax calculation
        tax_result = self.paye_calculator.calculate(
            float(total_income),
            float(total_deductions)
        )
        
        return {
            'total_income': float(total_income),
            'income_breakdown': {k: float(v) for k, v in income_breakdown.items()},
            'total_deductions': float(total_deductions),
            'deductions_breakdown': {k: float(v) for k, v in deductions_breakdown.items()},
            'taxable_income': tax_result['taxable_income'],
            'personal_allowance': tax_result['personal_allowance'],
            'tax_calculation': tax_result['tax_breakdown'],
            'total_tax': tax_result['total_tax'],
            'net_income': tax_result['net_income']
        }


class CorporateTaxCalculator:
    """
    Calculate UK Corporation Tax for businesses.
    
    Features:
    - Current UK corporation tax rate (19% for 2024)
    - Small Profits Rate (19% for profits up to £50,000)
    - Main Rate (25% for profits over £250,000)
    - Marginal Relief for profits between £50,000 and £250,000
    - Allowable expense deductions
    - R&D tax credits
    - Loss carry-forward rules
    """
    
    # Tax year 2024 constants
    SMALL_PROFITS_RATE = Decimal('0.19')
    MAIN_RATE = Decimal('0.25')
    SMALL_PROFITS_THRESHOLD = Decimal('50000')
    MAIN_RATE_THRESHOLD = Decimal('250000')
    
    # R&D tax credit rates
    RD_SME_CREDIT_RATE = Decimal('0.86')  # 86% enhancement for SMEs
    RD_LARGE_CREDIT_RATE = Decimal('0.13')  # 13% credit for large companies
    
    def __init__(self):
        """Initialize Corporate Tax calculator"""
        pass
    
    def validate_inputs(self, gross_profit: float, allowable_expenses: float = 0,
                       rd_expenditure: float = 0, losses_brought_forward: float = 0) -> None:
        """
        Validate input values for corporate tax calculation.
        
        Args:
            gross_profit: Company's gross profit
            allowable_expenses: Allowable business expenses
            rd_expenditure: Research & Development expenditure
            losses_brought_forward: Losses from previous years
            
        Raises:
            ValidationError: If inputs are invalid
        """
        if gross_profit < 0:
            raise ValidationError("Gross profit cannot be negative")
        if allowable_expenses < 0:
            raise ValidationError("Allowable expenses cannot be negative")
        if rd_expenditure < 0:
            raise ValidationError("R&D expenditure cannot be negative")
        if losses_brought_forward < 0:
            raise ValidationError("Losses brought forward cannot be negative")
    
    def calculate_marginal_relief(self, taxable_profit: Decimal) -> Decimal:
        """
        Calculate marginal relief for profits between thresholds.
        
        Args:
            taxable_profit: The taxable profit amount
            
        Returns:
            Marginal relief amount
        """
        if taxable_profit <= self.SMALL_PROFITS_THRESHOLD:
            return Decimal('0')
        if taxable_profit >= self.MAIN_RATE_THRESHOLD:
            return Decimal('0')
        
        # Marginal relief formula
        upper_limit = self.MAIN_RATE_THRESHOLD
        standard_fraction = Decimal('0.015')  # 3/200
        
        marginal_relief = ((upper_limit - taxable_profit) * standard_fraction * 
                          (taxable_profit / taxable_profit))
        
        return marginal_relief.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def calculate(self, gross_profit: float, allowable_expenses: float = 0,
                 rd_expenditure: float = 0, losses_brought_forward: float = 0,
                 is_sme: bool = True) -> Dict[str, Any]:
        """
        Calculate UK Corporation Tax.
        
        Args:
            gross_profit: Company's gross profit in GBP
            allowable_expenses: Allowable business expenses in GBP
            rd_expenditure: Research & Development expenditure in GBP
            losses_brought_forward: Losses from previous years in GBP
            is_sme: Whether company qualifies as SME for R&D credits
            
        Returns:
            Dictionary containing:
                - gross_profit: Original gross profit
                - allowable_expenses: Applied expenses
                - adjusted_profit: Profit after expenses
                - rd_expenditure: R&D expenditure
                - rd_tax_credit: R&D tax credit amount
                - losses_brought_forward: Losses applied
                - taxable_profit: Final taxable profit
                - applicable_rate: Tax rate applied
                - marginal_relief: Marginal relief (if applicable)
                - corporation_tax: Total corporation tax
                - effective_rate: Effective tax rate percentage
                - net_profit: Profit after tax
                
        Raises:
            ValidationError: If inputs are invalid
        """
        # Validate inputs
        self.validate_inputs(gross_profit, allowable_expenses, rd_expenditure, losses_brought_forward)
        
        # Convert to Decimal
        gross = Decimal(str(gross_profit))
        expenses = Decimal(str(allowable_expenses))
        rd_spend = Decimal(str(rd_expenditure))
        losses = Decimal(str(losses_brought_forward))
        
        # Calculate adjusted profit after expenses
        adjusted_profit = gross - expenses
        
        # Calculate R&D tax credit
        if rd_spend > 0:
            if is_sme:
                # SME R&D tax credit - 86% enhancement
                rd_tax_credit = (rd_spend * self.RD_SME_CREDIT_RATE).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
            else:
                # Large company R&D credit - 13%
                rd_tax_credit = (rd_spend * self.RD_LARGE_CREDIT_RATE).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
        else:
            rd_tax_credit = Decimal('0')
        
        # Apply R&D credit to reduce profit
        profit_after_rd = adjusted_profit - rd_tax_credit
        
        # Apply losses brought forward
        taxable_profit = max(Decimal('0'), profit_after_rd - losses)
        
        # Determine applicable tax rate and calculate tax
        if taxable_profit <= self.SMALL_PROFITS_THRESHOLD:
            applicable_rate = self.SMALL_PROFITS_RATE
            corporation_tax = (taxable_profit * applicable_rate).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            marginal_relief = Decimal('0')
        elif taxable_profit >= self.MAIN_RATE_THRESHOLD:
            applicable_rate = self.MAIN_RATE
            corporation_tax = (taxable_profit * applicable_rate).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            marginal_relief = Decimal('0')
        else:
            # Marginal relief applies
            applicable_rate = self.MAIN_RATE
            tax_at_main_rate = (taxable_profit * self.MAIN_RATE).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            marginal_relief = self.calculate_marginal_relief(taxable_profit)
            corporation_tax = tax_at_main_rate - marginal_relief
        
        # Calculate effective rate
        if taxable_profit > 0:
            effective_rate = (corporation_tax / taxable_profit * 100).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        else:
            effective_rate = Decimal('0')
        
        # Calculate net profit
        net_profit = gross - expenses - corporation_tax
        
        return {
            'gross_profit': float(gross),
            'allowable_expenses': float(expenses),
            'adjusted_profit': float(adjusted_profit),
            'rd_expenditure': float(rd_spend),
            'rd_tax_credit': float(rd_tax_credit),
            'losses_brought_forward': float(losses),
            'taxable_profit': float(taxable_profit),
            'applicable_rate': float(applicable_rate),
            'marginal_relief': float(marginal_relief),
            'corporation_tax': float(corporation_tax),
            'effective_rate': float(effective_rate),
            'net_profit': float(net_profit)
        }


# Convenience functions for easy access
def calculate_paye(gross_income: float, deductions: float = 0) -> Dict[str, Any]:
    """
    Convenience function to calculate PAYE tax.
    
    Args:
        gross_income: Annual gross income
        deductions: Additional deductions
        
    Returns:
        PAYE calculation result dictionary
    """
    calculator = PAYECalculator()
    return calculator.calculate(gross_income, deductions)


def calculate_self_assessment(income_sources: List[Dict[str, float]],
                              deductions: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Convenience function to calculate Self Assessment tax.
    
    Args:
        income_sources: List of income source dictionaries
        deductions: Dictionary of deductions
        
    Returns:
        Self Assessment calculation result dictionary
    """
    calculator = SelfAssessmentCalculator()
    return calculator.calculate(income_sources, deductions)


def calculate_corporate_tax(gross_profit: float, allowable_expenses: float = 0,
                           rd_expenditure: float = 0, losses_brought_forward: float = 0,
                           is_sme: bool = True) -> Dict[str, Any]:
    """
    Convenience function to calculate Corporation Tax.
    
    Args:
        gross_profit: Company's gross profit
        allowable_expenses: Allowable business expenses
        rd_expenditure: R&D expenditure
        losses_brought_forward: Losses from previous years
        is_sme: Whether company is SME
        
    Returns:
        Corporation Tax calculation result dictionary
    """
    calculator = CorporateTaxCalculator()
    return calculator.calculate(gross_profit, allowable_expenses, rd_expenditure,
                               losses_brought_forward, is_sme)


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("UK TAX CALCULATOR - EXAMPLES")
    print("=" * 70)
    
    # Example 1: PAYE Calculation
    print("\n1. PAYE CALCULATION EXAMPLE")
    print("-" * 70)
    paye_result = calculate_paye(gross_income=45000, deductions=3000)
    print(f"Gross Income: £{paye_result['gross_income']:,.2f}")
    print(f"Deductions: £{paye_result['deductions']:,.2f}")
    print(f"Personal Allowance: £{paye_result['personal_allowance']:,.2f}")
    print(f"Taxable Income: £{paye_result['taxable_income']:,.2f}")
    print(f"\nTax Breakdown:")
    print(f"  Basic Rate (20%): £{paye_result['tax_breakdown']['basic_rate']:,.2f}")
    print(f"  Higher Rate (40%): £{paye_result['tax_breakdown']['higher_rate']:,.2f}")
    print(f"  Additional Rate (45%): £{paye_result['tax_breakdown']['additional_rate']:,.2f}")
    print(f"\nTotal Tax: £{paye_result['total_tax']:,.2f}")
    print(f"Net Income: £{paye_result['net_income']:,.2f}")
    
    # Example 2: Self Assessment with Multiple Income Sources
    print("\n\n2. SELF ASSESSMENT CALCULATION EXAMPLE")
    print("-" * 70)
    income_sources = [
        {'type': 'employment', 'amount': 35000},
        {'type': 'self_employment', 'amount': 20000},
        {'type': 'property', 'amount': 12000}
    ]
    deductions = {
        'pension': 4000,
        'charity': 500
    }
    sa_result = calculate_self_assessment(income_sources, deductions)
    print(f"Total Income: £{sa_result['total_income']:,.2f}")
    print(f"  Employment: £{sa_result['income_breakdown'].get('employment', 0):,.2f}")
    print(f"  Self-Employment: £{sa_result['income_breakdown'].get('self_employment', 0):,.2f}")
    print(f"  Property: £{sa_result['income_breakdown'].get('property', 0):,.2f}")
    print(f"\nTotal Deductions: £{sa_result['total_deductions']:,.2f}")
    print(f"  Pension: £{sa_result['deductions_breakdown'].get('pension', 0):,.2f}")
    print(f"  Charity: £{sa_result['deductions_breakdown'].get('charity', 0):,.2f}")
    print(f"\nTaxable Income: £{sa_result['taxable_income']:,.2f}")
    print(f"Total Tax: £{sa_result['total_tax']:,.2f}")
    print(f"Net Income: £{sa_result['net_income']:,.2f}")
    
    # Example 3: Corporation Tax
    print("\n\n3. CORPORATION TAX CALCULATION EXAMPLE")
    print("-" * 70)
    corp_result = calculate_corporate_tax(
        gross_profit=300000,
        allowable_expenses=80000,
        rd_expenditure=25000,
        losses_brought_forward=10000,
        is_sme=True
    )
    print(f"Gross Profit: £{corp_result['gross_profit']:,.2f}")
    print(f"Allowable Expenses: £{corp_result['allowable_expenses']:,.2f}")
    print(f"Adjusted Profit: £{corp_result['adjusted_profit']:,.2f}")
    print(f"\nR&D Expenditure: £{corp_result['rd_expenditure']:,.2f}")
    print(f"R&D Tax Credit: £{corp_result['rd_tax_credit']:,.2f}")
    print(f"Losses Brought Forward: £{corp_result['losses_brought_forward']:,.2f}")
    print(f"\nTaxable Profit: £{corp_result['taxable_profit']:,.2f}")
    print(f"Applicable Rate: {corp_result['applicable_rate'] * 100:.1f}%")
    print(f"Marginal Relief: £{corp_result['marginal_relief']:,.2f}")
    print(f"\nCorporation Tax: £{corp_result['corporation_tax']:,.2f}")
    print(f"Effective Rate: {corp_result['effective_rate']:.2f}%")
    print(f"Net Profit: £{corp_result['net_profit']:,.2f}")
    
    print("\n" + "=" * 70)
