"""
Tax Optimization Module

This module provides advanced tax computation and optimization strategies
based on UK HMRC rules for different entity types.

Author: Tax Calculator System
Date: 2024
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
    """Enumeration of supported entity types"""
    SOLE_TRADER = "sole_trader"
    COMPANY = "company"
    LANDLORD = "landlord"
    EMPLOYEE = "employee"


@dataclass
class TaxRules:
    """UK HMRC Tax Rules for 2024/25"""
    
    # Income Tax
    personal_allowance: float = 12570
    personal_allowance_taper_threshold: float = 100000
    basic_rate_limit: float = 50270
    higher_rate_limit: float = 125140
    basic_rate: float = 0.20
    higher_rate: float = 0.40
    additional_rate: float = 0.45
    
    # National Insurance
    ni_class1_rate: float = 0.12
    ni_class1_reduced_rate: float = 0.02
    ni_class2_weekly: float = 3.45
    ni_class2_threshold: float = 6725
    ni_class4_rate: float = 0.09
    ni_class4_reduced_rate: float = 0.02
    
    # Corporation Tax
    corporation_small_rate: float = 0.19
    corporation_main_rate: float = 0.25
    corporation_small_threshold: float = 50000
    corporation_main_threshold: float = 250000
    
    # Capital Gains Tax
    cgt_annual_exemption: float = 3000
    cgt_basic_rate: float = 0.10
    cgt_higher_rate: float = 0.20
    cgt_property_basic_rate: float = 0.18
    cgt_property_higher_rate: float = 0.24
    
    # Allowances
    trading_allowance: float = 1000
    property_allowance: float = 1000
    dividend_allowance: float = 500
    savings_allowance_basic: float = 1000
    savings_allowance_higher: float = 500
    marriage_allowance: float = 1260
    pension_annual_allowance: float = 60000
    
    # Dividend Tax
    dividend_basic_rate: float = 0.0875
    dividend_higher_rate: float = 0.3375
    dividend_additional_rate: float = 0.3938
    
    # VAT
    vat_standard_rate: float = 0.20
    vat_threshold: float = 90000


class AllowableExpenses:
    """
    Defines allowable expenses for different entity types
    based on HMRC rules
    """
    
    @staticmethod
    def get_sole_trader_expenses() -> List[Dict[str, Any]]:
        """
        Get list of allowable expenses for sole traders
        
        Returns:
            List of expense categories with descriptions
        """
        return [
            {
                'category': 'Office Costs',
                'items': ['Stationery', 'Phone/Internet', 'Software subscriptions'],
                'fully_deductible': True,
                'notes': 'Business use only'
            },
            {
                'category': 'Travel',
                'items': ['Business mileage', 'Public transport', 'Hotel accommodation'],
                'fully_deductible': True,
                'notes': 'Not home to work travel'
            },
            {
                'category': 'Marketing',
                'items': ['Advertising', 'Website costs', 'Business cards'],
                'fully_deductible': True,
                'notes': 'Must be wholly for business'
            },
            {
                'category': 'Professional Fees',
                'items': ['Accountancy', 'Legal fees', 'Professional subscriptions'],
                'fully_deductible': True,
                'notes': 'Must be business related'
            },
            {
                'category': 'Stock/Materials',
                'items': ['Raw materials', 'Goods for resale'],
                'fully_deductible': True,
                'notes': 'Cost of goods sold'
            },
            {
                'category': 'Equipment',
                'items': ['Computers', 'Tools', 'Machinery'],
                'fully_deductible': False,
                'notes': 'Capital allowances apply - use Annual Investment Allowance'
            },
            {
                'category': 'Home Office',
                'items': ['Proportion of rent', 'Utilities', 'Council tax'],
                'fully_deductible': False,
                'notes': 'Use simplified expenses: £10-26/month based on hours'
            }
        ]
    
    @staticmethod
    def get_company_expenses() -> List[Dict[str, Any]]:
        """
        Get list of allowable expenses for limited companies
        
        Returns:
            List of expense categories with descriptions
        """
        return [
            {
                'category': 'Salaries',
                'items': ['Director salary', 'Employee wages', 'Employer NI'],
                'fully_deductible': True,
                'notes': 'Must be reasonable and paid'
            },
            {
                'category': 'Pensions',
                'items': ['Employer pension contributions'],
                'fully_deductible': True,
                'notes': 'No NI on employer contributions'
            },
            {
                'category': 'Office Costs',
                'items': ['Rent', 'Utilities', 'Equipment'],
                'fully_deductible': True,
                'notes': 'Must be wholly for business'
            },
            {
                'category': 'Professional Services',
                'items': ['Accountancy', 'Legal fees', 'Consultancy'],
                'fully_deductible': True,
                'notes': 'Must be business related'
            },
            {
                'category': 'Marketing',
                'items': ['Advertising', 'PR', 'Website'],
                'fully_deductible': True,
                'notes': 'Revenue expenditure only'
            },
            {
                'category': 'Travel & Subsistence',
                'items': ['Business travel', 'Hotels', 'Meals on business trips'],
                'fully_deductible': True,
                'notes': 'Must be wholly, exclusively, necessarily for business'
            }
        ]
    
    @staticmethod
    def get_landlord_expenses() -> List[Dict[str, Any]]:
        """
        Get list of allowable expenses for landlords
        
        Returns:
            List of expense categories with descriptions
        """
        return [
            {
                'category': 'Maintenance & Repairs',
                'items': ['Repairs', 'Redecorating', 'Maintenance'],
                'fully_deductible': True,
                'notes': 'Not improvements - just maintenance'
            },
            {
                'category': 'Mortgage Interest',
                'items': ['Interest on property loans'],
                'fully_deductible': False,
                'notes': '20% tax credit only (not full deduction)'
            },
            {
                'category': 'Property Management',
                'items': ['Agent fees', 'Legal fees', 'Advertising'],
                'fully_deductible': True,
                'notes': 'For letting the property'
            },
            {
                'category': 'Utilities',
                'items': ['Water', 'Gas', 'Electricity', 'Council tax'],
                'fully_deductible': True,
                'notes': 'Only if you pay (not tenant)'
            },
            {
                'category': 'Insurance',
                'items': ['Buildings insurance', 'Contents insurance', 'Landlord insurance'],
                'fully_deductible': True,
                'notes': 'Must be for rental property'
            },
            {
                'category': 'Services',
                'items': ['Ground rent', 'Service charges', 'Gardening'],
                'fully_deductible': True,
                'notes': 'If you pay these costs'
            }
        ]
    
    @staticmethod
    def get_employee_expenses() -> List[Dict[str, Any]]:
        """
        Get list of allowable expenses for employees
        
        Returns:
            List of expense categories with descriptions
        """
        return [
            {
                'category': 'Travel',
                'items': ['Business travel', 'Mileage (45p/25p)'],
                'fully_deductible': True,
                'notes': 'Not home to work - must be temporary workplace'
            },
            {
                'category': 'Professional Fees',
                'items': ['Professional subscriptions', 'Union fees'],
                'fully_deductible': True,
                'notes': 'Must be on HMRC approved list'
            },
            {
                'category': 'Uniform',
                'items': ['Uniform cleaning', 'Protective clothing'],
                'fully_deductible': True,
                'notes': 'Flat rate or actual costs'
            },
            {
                'category': 'Working from Home',
                'items': ['Home office allowance'],
                'fully_deductible': True,
                'notes': '£6/week tax-free or claim actual costs'
            }
        ]


class TaxOptimizer:
    """
    Provides tax optimization strategies for different entity types
    """
    
    def __init__(self, tax_rules: TaxRules = None):
        """
        Initialize tax optimizer
        
        Args:
            tax_rules: TaxRules instance (uses default if not provided)
        """
        self.rules = tax_rules or TaxRules()
    
    def calculate_personal_allowance(self, adjusted_income: float) -> float:
        """
        Calculate personal allowance with tapering
        
        Args:
            adjusted_income: Income after pension contributions
            
        Returns:
            Personal allowance amount
        """
        if adjusted_income <= self.rules.personal_allowance_taper_threshold:
            return self.rules.personal_allowance
        
        # Taper: reduce by £1 for every £2 over £100,000
        excess = adjusted_income - self.rules.personal_allowance_taper_threshold
        reduction = excess / 2
        allowance = max(0, self.rules.personal_allowance - reduction)
        
        return allowance
    
    def optimize_sole_trader(self, income: float, expenses: float) -> Dict[str, Any]:
        """
        Optimize tax for sole traders
        
        Args:
            income: Gross income
            expenses: Total allowable expenses
            
        Returns:
            Dict with optimization suggestions
        """
        profit = income - expenses
        
        suggestions = []
        savings_opportunities = []
        
        # Check trading allowance
        if expenses < self.rules.trading_allowance:
            potential_saving = (self.rules.trading_allowance - expenses) * 0.20
            suggestions.append({
                'title': 'Use Trading Allowance',
                'description': f'Consider using £{self.rules.trading_allowance} trading allowance instead of actual expenses',
                'potential_saving': potential_saving,
                'priority': 'HIGH'
            })
        
        # Pension optimization
        if profit > self.rules.basic_rate_limit:
            excess = profit - self.rules.basic_rate_limit
            max_pension = min(excess, self.rules.pension_annual_allowance)
            potential_saving = max_pension * 0.40  # Higher rate tax relief
            suggestions.append({
                'title': 'Increase Pension Contributions',
                'description': f'Contributing £{max_pension:.2f} to pension could save £{potential_saving:.2f} in tax',
                'potential_saving': potential_saving,
                'priority': 'HIGH'
            })
        
        # VAT threshold check
        if income > self.rules.vat_threshold * 0.85:
            suggestions.append({
                'title': 'VAT Registration Planning',
                'description': 'You\'re approaching VAT threshold. Plan for registration or manage turnover',
                'potential_saving': 0,
                'priority': 'MEDIUM'
            })
        
        # Incorporation threshold
        if profit > 50000:
            suggestions.append({
                'title': 'Consider Incorporation',
                'description': 'With profits over £50,000, incorporation might be tax-efficient',
                'potential_saving': 0,
                'priority': 'MEDIUM'
            })
        
        return {
            'entity_type': 'Sole Trader',
            'current_profit': profit,
            'suggestions': suggestions,
            'allowable_expenses': AllowableExpenses.get_sole_trader_expenses()
        }
    
    def optimize_company(self, profit: float, salary: float, dividends: float) -> Dict[str, Any]:
        """
        Optimize tax for limited companies
        
        Args:
            profit: Company profit before tax
            salary: Director's salary
            dividends: Dividends paid
            
        Returns:
            Dict with optimization suggestions
        """
        suggestions = []
        
        # Optimal salary recommendation
        optimal_salary = self.rules.personal_allowance
        if salary < optimal_salary:
            ni_saving = (optimal_salary - salary) * 0.138  # Employer NI saving
            suggestions.append({
                'title': 'Optimize Director Salary',
                'description': f'Consider increasing salary to £{optimal_salary} (personal allowance)',
                'potential_saving': ni_saving,
                'priority': 'HIGH'
            })
        elif salary > optimal_salary + 1000:
            excess_ni = (salary - optimal_salary) * (0.12 + 0.138)  # Employee + Employer NI
            suggestions.append({
                'title': 'Review Salary Level',
                'description': 'High salary attracts NI. Consider salary/dividend balance',
                'potential_saving': excess_ni,
                'priority': 'MEDIUM'
            })
        
        # Dividend allowance
        if dividends > self.rules.dividend_allowance:
            suggestions.append({
                'title': 'Dividend Timing',
                'description': 'Consider timing dividend payments across tax years',
                'potential_saving': 0,
                'priority': 'LOW'
            })
        
        # Pension contributions
        pension_space = self.rules.pension_annual_allowance
        if profit > self.rules.corporation_small_threshold:
            potential_pension = min(pension_space, profit * 0.15)
            corp_tax_saving = potential_pension * self.rules.corporation_small_rate
            suggestions.append({
                'title': 'Employer Pension Contributions',
                'description': f'£{potential_pension:.2f} employer pension saves £{corp_tax_saving:.2f} corporation tax',
                'potential_saving': corp_tax_saving,
                'priority': 'HIGH'
            })
        
        # Corporation tax optimization
        if profit > self.rules.corporation_main_threshold:
            suggestions.append({
                'title': 'Review Profit Levels',
                'description': 'Profits over £250k attract 25% corporation tax',
                'potential_saving': 0,
                'priority': 'MEDIUM'
            })
        
        return {
            'entity_type': 'Limited Company',
            'company_profit': profit,
            'director_salary': salary,
            'dividends': dividends,
            'suggestions': suggestions,
            'allowable_expenses': AllowableExpenses.get_company_expenses()
        }
    
    def optimize_landlord(self, rental_income: float, expenses: float, 
                         mortgage_interest: float = 0) -> Dict[str, Any]:
        """
        Optimize tax for landlords
        
        Args:
            rental_income: Total rental income
            expenses: Property expenses (excluding mortgage interest)
            mortgage_interest: Mortgage interest paid
            
        Returns:
            Dict with optimization suggestions
        """
        suggestions = []
        
        # Property allowance
        if expenses < self.rules.property_allowance:
            potential_saving = (self.rules.property_allowance - expenses) * 0.20
            suggestions.append({
                'title': 'Use Property Allowance',
                'description': f'Consider using £{self.rules.property_allowance} property allowance',
                'potential_saving': potential_saving,
                'priority': 'HIGH'
            })
        
        # Mortgage interest restriction
        if mortgage_interest > 0:
            # Only 20% tax credit available
            tax_credit = mortgage_interest * 0.20
            suggestions.append({
                'title': 'Mortgage Interest Restriction',
                'description': f'You get 20% tax credit (£{tax_credit:.2f}) on £{mortgage_interest:.2f} interest',
                'potential_saving': 0,
                'priority': 'INFO'
            })
        
        # Consider incorporation
        if rental_income > 50000:
            suggestions.append({
                'title': 'Consider Property Company',
                'description': 'High rental income might benefit from incorporation',
                'potential_saving': 0,
                'priority': 'MEDIUM'
            })
        
        # Capital gains tax planning
        suggestions.append({
            'title': 'CGT Annual Exemption',
            'description': f'Use £{self.rules.cgt_annual_exemption} annual exemption if selling property',
            'potential_saving': 0,
            'priority': 'LOW'
        })
        
        return {
            'entity_type': 'Landlord',
            'rental_income': rental_income,
            'expenses': expenses,
            'mortgage_interest': mortgage_interest,
            'suggestions': suggestions,
            'allowable_expenses': AllowableExpenses.get_landlord_expenses()
        }
    
    def optimize_employee(self, salary: float, bonus: float = 0, 
                         other_income: float = 0) -> Dict[str, Any]:
        """
        Optimize tax for employees
        
        Args:
            salary: Annual gross salary
            bonus: Bonus/commission
            other_income: Other taxable income
            
        Returns:
            Dict with optimization suggestions
        """
        total_income = salary + bonus + other_income
        suggestions = []
        
        # Salary sacrifice
        if total_income > self.rules.basic_rate_limit:
            excess = total_income - self.rules.basic_rate_limit
            pension_opportunity = min(excess, self.rules.pension_annual_allowance * 0.5)
            tax_saving = pension_opportunity * 0.40
            ni_saving = pension_opportunity * 0.02
            total_saving = tax_saving + ni_saving
            
            suggestions.append({
                'title': 'Salary Sacrifice Pension',
                'description': f'£{pension_opportunity:.2f} salary sacrifice saves £{total_saving:.2f}',
                'potential_saving': total_saving,
                'priority': 'HIGH'
            })
        
        # Marriage allowance
        suggestions.append({
            'title': 'Marriage Allowance',
            'description': f'Transfer £{self.rules.marriage_allowance} allowance to spouse (if eligible)',
            'potential_saving': self.rules.marriage_allowance * 0.20,
            'priority': 'LOW'
        })
        
        # High income child benefit charge
        if total_income > 50000:
            suggestions.append({
                'title': 'Child Benefit Charge',
                'description': 'Income over £50k triggers High Income Child Benefit Charge',
                'potential_saving': 0,
                'priority': 'MEDIUM'
            })
        
        # Personal allowance tapering
        if total_income > self.rules.personal_allowance_taper_threshold:
            suggestions.append({
                'title': 'Personal Allowance Tapering',
                'description': 'Effective 60% tax rate between £100k-£125k',
                'potential_saving': 0,
                'priority': 'HIGH'
            })
        
        return {
            'entity_type': 'Employee',
            'total_income': total_income,
            'suggestions': suggestions,
            'allowable_expenses': AllowableExpenses.get_employee_expenses()
        }


def main():
    """Test tax optimizer functionality"""
    print("=" * 60)
    print("Tax Optimization Module Test")
    print("=" * 60)
    
    optimizer = TaxOptimizer()
    
    # Test sole trader optimization
    print("\n1. Sole Trader Optimization")
    print("-" * 60)
    result = optimizer.optimize_sole_trader(income=60000, expenses=8000)
    print(f"   Entity: {result['entity_type']}")
    print(f"   Profit: £{result['current_profit']:.2f}")
    print(f"   Suggestions: {len(result['suggestions'])}")
    for suggestion in result['suggestions']:
        print(f"   - {suggestion['title']}: {suggestion['description']}")
    
    # Test company optimization
    print("\n2. Limited Company Optimization")
    print("-" * 60)
    result = optimizer.optimize_company(profit=100000, salary=10000, dividends=40000)
    print(f"   Entity: {result['entity_type']}")
    print(f"   Company Profit: £{result['company_profit']:.2f}")
    print(f"   Suggestions: {len(result['suggestions'])}")
    for suggestion in result['suggestions']:
        print(f"   - {suggestion['title']}")
    
    print("\n" + "=" * 60)
    print("✓ Tax optimization test completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
