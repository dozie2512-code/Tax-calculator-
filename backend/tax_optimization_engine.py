"""
Tax Optimization Engine

This module provides optimization strategies for different types of taxpayers:
- Company Directors
- Sole Traders
- Company Owners
- Landlords

Each optimization strategy analyzes the current tax position and recommends
improvements to minimize tax liability while remaining compliant.
"""

from typing import Dict, Any, List
from backend.uk_tax_calculator import UKTaxCalculator


class TaxOptimizationEngine:
    """
    Provides tax optimization recommendations for different user types.
    """
    
    def __init__(self):
        """Initialize the optimization engine with a tax calculator."""
        self.calculator = UKTaxCalculator()
    
    def optimize_director(self, data: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize tax position for a company director.
        
        Strategy:
        - Minimize salary to personal allowance or NI threshold
        - Maximize dividend extraction
        - Consider pension contributions
        - Balance corporation tax vs personal tax
        
        Args:
            data: Dictionary containing:
                - salary: Current annual salary
                - dividends: Current dividend income
                - company_profit: Company profit before salary
                - pension_contribution: Annual pension contribution
                
        Returns:
            Dictionary with current position, optimal position, and recommendations
        """
        salary = data.get('salary', 0)
        dividends = data.get('dividends', 0)
        company_profit = data.get('company_profit', 0)
        pension = data.get('pension_contribution', 0)
        
        # Calculate current position
        current = self.calculator.calculate_total_tax_liability(
            salary=salary,
            dividends=dividends,
            company_profit=company_profit
        )
        
        # Optimal strategy: Salary at NI threshold, maximize dividends
        optimal_salary = self.calculator.NI_PRIMARY_THRESHOLD
        
        # Adjust company profit for optimal salary and pension
        adjusted_profit = company_profit - optimal_salary - pension
        
        # Calculate corporation tax on adjusted profit
        corp_tax_result = self.calculator.calculate_corporation_tax(adjusted_profit)
        profit_after_corp_tax = corp_tax_result['profit_after_tax']
        
        # Optimal dividends = profit after corporation tax
        optimal_dividends = profit_after_corp_tax
        
        # Calculate optimal position
        optimal = self.calculator.calculate_total_tax_liability(
            salary=optimal_salary,
            dividends=optimal_dividends,
            company_profit=company_profit
        )
        
        # Calculate savings
        current_total_tax = current['net_position']['total_tax']
        if 'company_tax' in current:
            current_total_tax += current['company_tax']['corporation_tax']
        
        optimal_total_tax = optimal['net_position']['total_tax']
        if 'company_tax' in optimal:
            optimal_total_tax += optimal['company_tax']['corporation_tax']
        
        potential_saving = current_total_tax - optimal_total_tax
        
        # Generate recommendations
        recommendations = []
        
        if salary > optimal_salary:
            recommendations.append({
                'priority': 'high',
                'title': 'Optimize Salary/Dividend Split',
                'description': f'Reduce salary to £{optimal_salary:,.2f} (NI threshold) and take remaining income as dividends to minimize NI contributions.',
                'potential_saving': round(abs(salary - optimal_salary) * 0.08, 2)
            })
        
        if pension < 10000 and company_profit > 50000:
            recommendations.append({
                'priority': 'medium',
                'title': 'Increase Pension Contributions',
                'description': 'Consider increasing pension contributions through the company for corporation tax relief and personal tax benefits.',
                'potential_saving': round((10000 - pension) * 0.19, 2)
            })
        
        if dividends > 0:
            recommendations.append({
                'priority': 'low',
                'title': 'Dividend Timing',
                'description': 'Consider timing dividend payments across tax years to maximize use of dividend allowances.',
                'potential_saving': 0
            })
        
        recommendations.append({
            'priority': 'medium',
            'title': 'Review Expenses',
            'description': 'Ensure all business expenses are claimed through the company to reduce corporation tax liability.',
            'potential_saving': 0
        })
        
        return {
            'user_type': 'Company Director',
            'current_position': {
                'salary': round(salary, 2),
                'dividends': round(dividends, 2),
                'pension': round(pension, 2),
                'total_income': round(salary + dividends, 2),
                'income_tax': round(current['tax_breakdown']['income_tax'], 2),
                'national_insurance': round(current['tax_breakdown']['national_insurance'], 2),
                'dividend_tax': round(current['tax_breakdown']['dividend_tax'], 2),
                'total_personal_tax': round(current['net_position']['total_tax'], 2),
                'corporation_tax': round(current.get('company_tax', {}).get('corporation_tax', 0), 2),
                'total_tax': round(current_total_tax, 2),
                'net_income': round(current['net_position']['net_income'], 2)
            },
            'optimal_position': {
                'salary': round(optimal_salary, 2),
                'dividends': round(optimal_dividends, 2),
                'pension': round(pension, 2),
                'total_income': round(optimal_salary + optimal_dividends, 2),
                'income_tax': round(optimal['tax_breakdown']['income_tax'], 2),
                'national_insurance': round(optimal['tax_breakdown']['national_insurance'], 2),
                'dividend_tax': round(optimal['tax_breakdown']['dividend_tax'], 2),
                'total_personal_tax': round(optimal['net_position']['total_tax'], 2),
                'corporation_tax': round(optimal.get('company_tax', {}).get('corporation_tax', 0), 2),
                'total_tax': round(optimal_total_tax, 2),
                'net_income': round(optimal['net_position']['net_income'], 2)
            },
            'potential_saving': round(potential_saving, 2),
            'recommendations': recommendations
        }
    
    def optimize_sole_trader(self, data: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize tax position for a sole trader.
        
        Strategy:
        - Maximize allowable expense claims
        - Utilize capital allowances
        - Consider pension contributions for tax relief
        - Evaluate incorporation benefits
        
        Args:
            data: Dictionary containing:
                - trading_income: Annual trading income
                - allowable_expenses: Current allowable expenses
                - pension_contribution: Annual pension contribution
                - capital_allowances: Capital allowances claimed
                
        Returns:
            Dictionary with current position, optimal position, and recommendations
        """
        trading_income = data.get('trading_income', 0)
        expenses = data.get('allowable_expenses', 0)
        pension = data.get('pension_contribution', 0)
        capital_allowances = data.get('capital_allowances', 0)
        
        # Calculate current taxable profit
        current_profit = trading_income - expenses - capital_allowances
        
        # Calculate current tax position
        current = self.calculator.calculate_total_tax_liability(salary=current_profit)
        
        # Optimal strategy: Maximize pension to reduce taxable income
        optimal_pension = min(pension + 5000, current_profit * 0.25)  # Up to 25% of profit
        optimal_capital_allowances = capital_allowances + 2000  # Assume additional equipment
        
        optimal_profit = trading_income - expenses - optimal_capital_allowances
        
        # Calculate optimal position (considering pension relief)
        optimal_taxable_income = max(0, optimal_profit - optimal_pension)
        optimal = self.calculator.calculate_total_tax_liability(salary=optimal_taxable_income)
        
        # Calculate savings
        potential_saving = current['net_position']['total_tax'] - optimal['net_position']['total_tax']
        
        # Generate recommendations
        recommendations = []
        
        if expenses < trading_income * 0.3:
            recommendations.append({
                'priority': 'high',
                'title': 'Review Allowable Expenses',
                'description': 'Ensure all business expenses are claimed including home office, travel, professional subscriptions, and business use of phone/internet.',
                'potential_saving': round((trading_income * 0.3 - expenses) * 0.20, 2)
            })
        
        if capital_allowances < 5000 and trading_income > 30000:
            recommendations.append({
                'priority': 'high',
                'title': 'Claim Annual Investment Allowance',
                'description': 'Consider purchasing business equipment or vehicles to claim Annual Investment Allowance (AIA) up to £1 million.',
                'potential_saving': round(2000 * 0.20, 2)
            })
        
        if pension < trading_income * 0.15:
            recommendations.append({
                'priority': 'medium',
                'title': 'Increase Pension Contributions',
                'description': 'Pension contributions provide tax relief at your marginal rate and reduce taxable profit.',
                'potential_saving': round(5000 * 0.20, 2)
            })
        
        if trading_income > 50000:
            recommendations.append({
                'priority': 'medium',
                'title': 'Consider Incorporation',
                'description': 'If profit exceeds £50,000, incorporating as a limited company could provide significant tax savings through lower corporation tax rates.',
                'potential_saving': round((trading_income - 50000) * 0.06, 2)
            })
        
        recommendations.append({
            'priority': 'low',
            'title': 'VAT Registration',
            'description': 'If turnover exceeds £85,000, consider VAT registration benefits and flat rate scheme.',
            'potential_saving': 0
        })
        
        return {
            'user_type': 'Sole Trader',
            'current_position': {
                'trading_income': round(trading_income, 2),
                'expenses': round(expenses, 2),
                'capital_allowances': round(capital_allowances, 2),
                'taxable_profit': round(current_profit, 2),
                'income_tax': round(current['tax_breakdown']['income_tax'], 2),
                'national_insurance': round(current['tax_breakdown']['national_insurance'], 2),
                'total_tax': round(current['net_position']['total_tax'], 2),
                'net_income': round(current['net_position']['net_income'], 2)
            },
            'optimal_position': {
                'trading_income': round(trading_income, 2),
                'expenses': round(expenses, 2),
                'capital_allowances': round(optimal_capital_allowances, 2),
                'pension': round(optimal_pension, 2),
                'taxable_profit': round(optimal_taxable_income, 2),
                'income_tax': round(optimal['tax_breakdown']['income_tax'], 2),
                'national_insurance': round(optimal['tax_breakdown']['national_insurance'], 2),
                'total_tax': round(optimal['net_position']['total_tax'], 2),
                'net_income': round(optimal['net_position']['net_income'], 2)
            },
            'potential_saving': round(potential_saving, 2),
            'recommendations': recommendations
        }
    
    def optimize_company_owner(self, data: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize tax position for a company owner.
        
        Strategy:
        - Optimize profit extraction (salary vs dividends)
        - Utilize R&D tax credits
        - Maximize capital allowances
        - Consider timing of profit extraction
        
        Args:
            data: Dictionary containing:
                - company_profit: Annual company profit
                - salary: Current salary drawn
                - dividends: Current dividends taken
                - r_and_d_expenditure: R&D expenditure
                - capital_investment: Capital investments made
                
        Returns:
            Dictionary with current position, optimal position, and recommendations
        """
        company_profit = data.get('company_profit', 0)
        salary = data.get('salary', 0)
        dividends = data.get('dividends', 0)
        r_and_d = data.get('r_and_d_expenditure', 0)
        capital_investment = data.get('capital_investment', 0)
        
        # Calculate current position
        current = self.calculator.calculate_total_tax_liability(
            salary=salary,
            dividends=dividends,
            company_profit=company_profit
        )
        
        # Optimal strategy incorporating R&D relief and capital allowances
        # R&D relief: 186% deduction for SMEs
        r_and_d_relief = r_and_d * 0.86 if r_and_d > 0 else 0
        
        # Optimal salary at NI threshold
        optimal_salary = self.calculator.NI_PRIMARY_THRESHOLD
        
        # Adjust profit for reliefs
        adjusted_profit = company_profit - optimal_salary - r_and_d_relief - capital_investment
        
        # Corporation tax
        corp_tax_result = self.calculator.calculate_corporation_tax(adjusted_profit)
        optimal_dividends = corp_tax_result['profit_after_tax']
        
        # Calculate optimal position
        optimal = self.calculator.calculate_total_tax_liability(
            salary=optimal_salary,
            dividends=optimal_dividends,
            company_profit=company_profit
        )
        
        # Calculate total tax
        current_total_tax = current['net_position']['total_tax']
        if 'company_tax' in current:
            current_total_tax += current['company_tax']['corporation_tax']
        
        optimal_total_tax = optimal['net_position']['total_tax']
        if 'company_tax' in optimal:
            optimal_total_tax += optimal['company_tax']['corporation_tax']
        
        potential_saving = current_total_tax - optimal_total_tax
        
        # Generate recommendations
        recommendations = []
        
        if r_and_d > 0:
            recommendations.append({
                'priority': 'high',
                'title': 'Claim R&D Tax Credits',
                'description': f'Your R&D expenditure of £{r_and_d:,.2f} qualifies for enhanced relief. SMEs can deduct 186% of qualifying expenditure.',
                'potential_saving': round(r_and_d_relief * 0.19, 2)
            })
        
        if capital_investment > 0:
            recommendations.append({
                'priority': 'high',
                'title': 'Claim Capital Allowances',
                'description': 'Claim Annual Investment Allowance on qualifying capital expenditure for immediate tax relief.',
                'potential_saving': round(capital_investment * 0.19, 2)
            })
        
        if salary > optimal_salary:
            recommendations.append({
                'priority': 'high',
                'title': 'Optimize Salary/Dividend Ratio',
                'description': f'Reduce salary to £{optimal_salary:,.2f} and extract remaining profit as dividends to minimize NI.',
                'potential_saving': round((salary - optimal_salary) * 0.08, 2)
            })
        
        if company_profit > 100000:
            recommendations.append({
                'priority': 'medium',
                'title': 'Pension Contributions',
                'description': 'Consider employer pension contributions for corporation tax relief at 19-25%.',
                'potential_saving': round(10000 * 0.19, 2)
            })
        
        recommendations.append({
            'priority': 'low',
            'title': 'Timing of Dividend Payments',
            'description': 'Plan dividend payments across tax years to maximize use of annual dividend allowances.',
            'potential_saving': 0
        })
        
        return {
            'user_type': 'Company Owner',
            'current_position': {
                'company_profit': round(company_profit, 2),
                'salary': round(salary, 2),
                'dividends': round(dividends, 2),
                'total_income': round(salary + dividends, 2),
                'total_tax': round(current_total_tax, 2),
                'net_income': round(current['net_position']['net_income'], 2)
            },
            'optimal_position': {
                'company_profit': round(company_profit, 2),
                'salary': round(optimal_salary, 2),
                'dividends': round(optimal_dividends, 2),
                'r_and_d_relief': round(r_and_d_relief, 2),
                'capital_allowances': round(capital_investment, 2),
                'total_income': round(optimal_salary + optimal_dividends, 2),
                'total_tax': round(optimal_total_tax, 2),
                'net_income': round(optimal['net_position']['net_income'], 2)
            },
            'potential_saving': round(potential_saving, 2),
            'recommendations': recommendations
        }
    
    def optimize_landlord(self, data: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize tax position for a landlord.
        
        Strategy:
        - Maximize allowable expense deductions
        - Utilize property allowance
        - Consider mortgage interest relief (20% tax reduction)
        - Evaluate incorporation benefits
        - Joint ownership with spouse
        
        Args:
            data: Dictionary containing:
                - rental_income: Annual rental income
                - mortgage_interest: Annual mortgage interest
                - other_expenses: Other property expenses
                - is_furnished: Whether properties are furnished
                - number_of_properties: Number of rental properties
                
        Returns:
            Dictionary with current position, optimal position, and recommendations
        """
        rental_income = data.get('rental_income', 0)
        mortgage_interest = data.get('mortgage_interest', 0)
        other_expenses = data.get('other_expenses', 0)
        is_furnished = data.get('is_furnished', False)
        num_properties = data.get('number_of_properties', 1)
        
        # Property allowance
        property_allowance = 1000
        
        # Current position: mortgage interest gets 20% tax reduction, not deduction
        current_expenses = other_expenses
        current_taxable_income = rental_income - current_expenses
        
        # Calculate tax on rental income
        current = self.calculator.calculate_total_tax_liability(salary=current_taxable_income)
        
        # Mortgage interest relief (20% of interest)
        mortgage_relief = mortgage_interest * 0.20
        current_tax = max(0, current['net_position']['total_tax'] - mortgage_relief)
        
        # Optimal strategy
        optimal_expenses = other_expenses
        
        # Furnished property relief if applicable
        furnished_relief = 0
        if is_furnished:
            # Replacement of domestic items relief
            furnished_relief = min(rental_income * 0.10, 2000 * num_properties)
            optimal_expenses += furnished_relief
        
        # Use property allowance if beneficial
        if rental_income < 2500:
            optimal_taxable_income = max(0, rental_income - property_allowance)
        else:
            optimal_taxable_income = rental_income - optimal_expenses
        
        # Calculate optimal position
        optimal = self.calculator.calculate_total_tax_liability(salary=optimal_taxable_income)
        optimal_tax = max(0, optimal['net_position']['total_tax'] - mortgage_relief)
        
        potential_saving = current_tax - optimal_tax
        
        # Generate recommendations
        recommendations = []
        
        if is_furnished:
            recommendations.append({
                'priority': 'high',
                'title': 'Claim Replacement of Domestic Items Relief',
                'description': 'For furnished properties, claim relief on replacing furniture, appliances, and furnishings.',
                'potential_saving': round(furnished_relief * 0.20, 2)
            })
        
        if mortgage_interest > 0:
            recommendations.append({
                'priority': 'high',
                'title': 'Mortgage Interest Relief',
                'description': 'Claim 20% tax reduction on mortgage interest. Note: This is a tax credit, not a deduction.',
                'potential_saving': round(mortgage_relief, 2)
            })
        
        if rental_income > 50000 or num_properties > 3:
            recommendations.append({
                'priority': 'medium',
                'title': 'Consider Incorporation',
                'description': 'For larger portfolios, a property company could provide corporation tax benefits and full mortgage interest deductibility.',
                'potential_saving': round((rental_income - other_expenses) * 0.06, 2)
            })
        
        recommendations.append({
            'priority': 'medium',
            'title': 'Joint Ownership with Spouse',
            'description': 'If your spouse is a lower rate taxpayer, joint ownership can reduce overall tax liability by utilizing their lower tax bands.',
            'potential_saving': round(rental_income * 0.10, 2)
        })
        
        recommendations.append({
            'priority': 'low',
            'title': 'Maximize Expense Claims',
            'description': 'Ensure all allowable expenses are claimed: repairs, insurance, agent fees, legal fees, accountancy fees.',
            'potential_saving': 0
        })
        
        if rental_income < 2500:
            recommendations.append({
                'priority': 'low',
                'title': 'Property Allowance',
                'description': 'With income under £2,500, consider using the £1,000 property allowance instead of claiming expenses.',
                'potential_saving': 0
            })
        
        return {
            'user_type': 'Landlord',
            'current_position': {
                'rental_income': round(rental_income, 2),
                'mortgage_interest': round(mortgage_interest, 2),
                'other_expenses': round(other_expenses, 2),
                'taxable_income': round(current_taxable_income, 2),
                'tax_before_relief': round(current['net_position']['total_tax'], 2),
                'mortgage_relief': round(mortgage_relief, 2),
                'total_tax': round(current_tax, 2),
                'net_income': round(rental_income - other_expenses - mortgage_interest - current_tax, 2)
            },
            'optimal_position': {
                'rental_income': round(rental_income, 2),
                'mortgage_interest': round(mortgage_interest, 2),
                'other_expenses': round(optimal_expenses, 2),
                'furnished_relief': round(furnished_relief, 2),
                'taxable_income': round(optimal_taxable_income, 2),
                'tax_before_relief': round(optimal['net_position']['total_tax'], 2),
                'mortgage_relief': round(mortgage_relief, 2),
                'total_tax': round(optimal_tax, 2),
                'net_income': round(rental_income - optimal_expenses - mortgage_interest - optimal_tax, 2)
            },
            'potential_saving': round(potential_saving, 2),
            'recommendations': recommendations
        }


if __name__ == '__main__':
    # Example usage
    engine = TaxOptimizationEngine()
    
    # Test director optimization
    print("Company Director Optimization")
    print("=" * 60)
    result = engine.optimize_director({
        'salary': 30000,
        'dividends': 20000,
        'company_profit': 60000,
        'pension_contribution': 0
    })
    print(f"Current Tax: £{result['current_position']['total_tax']:,.2f}")
    print(f"Optimal Tax: £{result['optimal_position']['total_tax']:,.2f}")
    print(f"Potential Saving: £{result['potential_saving']:,.2f}")
    print()
