"""
Tax Optimization Strategies for Different User Types
Provides tailored tax-saving recommendations based on HMRC guidelines.

This module implements tax optimization strategies for:
- Company Directors: Salary vs dividends, pension optimization
- Sole Traders: Expense tracking, capital allowances, pension relief
- Company Owners: Corporation tax planning, R&D relief, profit extraction
- Landlords: Property allowances, mortgage interest relief, incorporation analysis
"""

from typing import Dict, Any, List
from backend.uk_tax_calculator import UKTaxCalculator, TaxReliefs, TaxConstants


class TaxOptimizationEngine:
    """
    Provides tax optimization strategies for different user types.
    
    All monetary amounts should be in GBP.
    All methods include comprehensive input validation and error handling.
    """
    
    # Optimization Constants
    # Optimal salary for directors: Use full personal allowance to minimize NI
    OPTIMAL_DIRECTOR_SALARY = TaxConstants.PERSONAL_ALLOWANCE
    
    # Thresholds for incorporation recommendations
    INCORPORATION_SAVINGS_THRESHOLD = 1_000  # Minimum saving to recommend incorporation
    INCORPORATION_PROPERTIES_THRESHOLD = 3  # Minimum properties to consider incorporation
    
    def __init__(self):
        """Initialize the optimization engine with calculator and reliefs modules."""
        self.calculator = UKTaxCalculator()
        self.reliefs = TaxReliefs()
    
    def _validate_positive_amount(self, value: float, field_name: str) -> None:
        """
        Validate that a monetary value is positive.
        
        Args:
            value: The value to validate
            field_name: Name of the field for error messages
            
        Raises:
            ValueError: If value is negative or not a valid number
        """
        if not isinstance(value, (int, float)):
            raise ValueError(f"{field_name} must be a number, got {type(value).__name__}")
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative, got {value}")
    
    def _validate_required_fields(self, **kwargs) -> None:
        """
        Validate that required fields are provided and valid.
        
        Args:
            **kwargs: Dictionary of field_name: value pairs to validate
            
        Raises:
            ValueError: If any field is missing or invalid
        """
        for field_name, value in kwargs.items():
            if value is None:
                raise ValueError(f"Required field '{field_name}' is missing")
            self._validate_positive_amount(value, field_name)
    
    def optimize_for_director(self, 
                             salary: float,
                             dividends: float,
                             company_profit: float,
                             pension_contribution: float = 0) -> Dict[str, Any]:
        """
        Optimize tax position for company directors.
        
        Args:
            salary: Current annual salary
            dividends: Proposed dividend amount
            company_profit: Company's taxable profit
            pension_contribution: Pension contribution amount
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Validate inputs
        try:
            self._validate_required_fields(
                salary=salary,
                dividends=dividends,
                company_profit=company_profit
            )
            self._validate_positive_amount(pension_contribution, 'pension_contribution')
        except ValueError as e:
            raise ValueError(f"Invalid input for director optimization: {e}")
        
        # Calculate current position
        paye = self.calculator.calculate_paye(salary)
        dividend_tax = self.calculator.calculate_dividend_tax(dividends, salary)
        corp_tax = self.calculator.calculate_corporation_tax(company_profit)
        
        # Calculate pension relief if applicable
        pension_relief = None
        if pension_contribution > 0:
            pension_relief = self.reliefs.calculate_pension_relief(pension_contribution, salary)
        
        # Optimal salary strategy
        optimal_salary = self.OPTIMAL_DIRECTOR_SALARY
        optimal_paye = self.calculator.calculate_paye(optimal_salary)
        
        # Calculate remaining profit
        remaining_profit = company_profit - optimal_salary
        optimal_corp_tax = self.calculator.calculate_corporation_tax(remaining_profit)
        
        # Maximum dividend that can be paid
        profit_after_corp_tax = remaining_profit - optimal_corp_tax['corporation_tax']
        
        # Calculate dividend tax
        optimal_dividend_tax = self.calculator.calculate_dividend_tax(
            profit_after_corp_tax, optimal_salary
        )
        
        # Total tax calculations
        optimal_total_tax = (optimal_paye['total_employee_deductions'] + 
                           optimal_corp_tax['corporation_tax'] + 
                           optimal_dividend_tax['dividend_tax'])
        
        current_total_tax = (paye['total_employee_deductions'] + 
                           corp_tax['corporation_tax'] + 
                           dividend_tax['dividend_tax'])
        
        potential_saving = current_total_tax - optimal_total_tax
        
        recommendations = [
            {
                'strategy': 'Optimal Salary Level',
                'description': f'Set salary at £{optimal_salary:,.2f} (personal allowance) to minimize NI',
                'saving': round(paye['employee_ni'] - optimal_paye['employee_ni'], 2)
            },
            {
                'strategy': 'Dividend Strategy',
                'description': f'Extract remaining profits (£{profit_after_corp_tax:,.2f}) as dividends',
                'saving': 'Lower tax rate than salary'
            }
        ]
        
        if pension_contribution == 0:
            recommendations.append({
                'strategy': 'Pension Contributions',
                'description': 'Consider employer pension contributions (corporation tax deductible, no NI)',
                'saving': 'Up to 45% tax relief + NI savings'
            })
        
        recommendations.append({
            'strategy': 'Dividend Timing',
            'description': 'Split dividend payments across tax years to maximize allowance',
            'saving': round(self.calculator.DIVIDEND_ALLOWANCE * self.calculator.DIVIDEND_BASIC_RATE, 2)
        })
        
        return {
            'user_type': 'Company Director',
            'current_position': {
                'salary': salary,
                'dividends': dividends,
                'total_tax': round(current_total_tax, 2),
                'net_income': round(salary + dividends - current_total_tax, 2)
            },
            'optimal_position': {
                'salary': optimal_salary,
                'dividends': round(profit_after_corp_tax, 2),
                'total_tax': round(optimal_total_tax, 2),
                'net_income': round(optimal_salary + profit_after_corp_tax - optimal_total_tax, 2)
            },
            'potential_saving': round(potential_saving, 2),
            'recommendations': recommendations
        }
    
    def optimize_for_sole_trader(self,
                                 trading_income: float,
                                 allowable_expenses: float,
                                 pension_contribution: float = 0,
                                 capital_allowances: float = 0) -> Dict[str, Any]:
        """
        Optimize tax position for sole traders.
        
        Args:
            trading_income: Gross trading income
            allowable_expenses: Claimed business expenses
            pension_contribution: Pension contribution amount
            capital_allowances: Capital allowances claimed
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Validate inputs
        try:
            self._validate_required_fields(
                trading_income=trading_income,
                allowable_expenses=allowable_expenses
            )
            self._validate_positive_amount(pension_contribution, 'pension_contribution')
            self._validate_positive_amount(capital_allowances, 'capital_allowances')
        except ValueError as e:
            raise ValueError(f"Invalid input for sole trader optimization: {e}")
        
        # Calculate taxable profit
        taxable_profit = max(0, trading_income - allowable_expenses - capital_allowances)
        
        # Apply trading allowance if beneficial
        trading_allowance = self.reliefs.calculate_trading_allowance(trading_income)
        profit_with_allowance = max(0, trading_income - self.reliefs.TRADING_ALLOWANCE)
        
        # Use allowance if beneficial
        use_allowance = (trading_income <= self.reliefs.TRADING_ALLOWANCE or 
                        (allowable_expenses + capital_allowances == 0 and 
                         profit_with_allowance < taxable_profit))
        
        final_taxable_profit = profit_with_allowance if use_allowance else taxable_profit
        
        # Calculate tax
        paye = self.calculator.calculate_paye(final_taxable_profit)
        
        # Calculate pension relief
        pension_relief = None
        if pension_contribution > 0:
            pension_relief = self.reliefs.calculate_pension_relief(
                pension_contribution, final_taxable_profit
            )
            adjusted_profit = max(0, final_taxable_profit - pension_contribution)
            adjusted_paye = self.calculator.calculate_paye(adjusted_profit)
        else:
            adjusted_paye = paye
        
        # Generate recommendations
        recommendations = []
        
        if allowable_expenses < trading_income * 0.20:
            recommendations.append({
                'strategy': 'Enhance Expense Tracking',
                'description': 'Review and claim all allowable business expenses (travel, equipment, home office)',
                'saving': f'Up to {int(TaxConstants.ADDITIONAL_RATE * 100)}% tax relief on expenses'
            })
        
        recommendations.append({
            'strategy': 'Annual Investment Allowance (AIA)',
            'description': f'Claim 100% first-year allowance on equipment up to £{TaxConstants.ANNUAL_INVESTMENT_ALLOWANCE:,}',
            'saving': 'Immediate tax relief on capital investments'
        })
        
        if pension_contribution == 0:
            recommendations.append({
                'strategy': 'Pension Contributions',
                'description': 'Make personal pension contributions for tax relief',
                'saving': f'Up to 45% tax relief (£{self.reliefs.PENSION_ANNUAL_ALLOWANCE:,} annual allowance)'
            })
        
        if not use_allowance and trading_income <= TaxConstants.TRADING_ALLOWANCE:
            recommendations.append({
                'strategy': 'Trading Allowance',
                'description': f'Consider using £{self.reliefs.TRADING_ALLOWANCE:,} trading allowance instead of expenses',
                'saving': 'Simplified reporting'
            })
        
        recommendations.append({
            'strategy': 'Income Splitting',
            'description': 'Consider employing spouse/partner if they have lower income',
            'saving': 'Utilize their personal allowance and lower tax bands'
        })
        
        return {
            'user_type': 'Sole Trader',
            'income_analysis': {
                'trading_income': trading_income,
                'allowable_expenses': allowable_expenses,
                'capital_allowances': capital_allowances,
                'taxable_profit': round(final_taxable_profit, 2),
                'method_used': 'Trading Allowance' if use_allowance else 'Expenses'
            },
            'tax_position': adjusted_paye,
            'pension_relief': pension_relief,
            'recommendations': recommendations
        }
    
    def optimize_for_company_owner(self,
                                   company_profit: float,
                                   salary: float,
                                   dividends: float,
                                   r_and_d_expenditure: float = 0,
                                   capital_investment: float = 0) -> Dict[str, Any]:
        """
        Optimize tax position for company owners.
        
        Args:
            company_profit: Company's taxable profit
            salary: Director's salary
            dividends: Dividends paid
            r_and_d_expenditure: Research & Development costs
            capital_investment: Capital investment in qualifying assets
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Validate inputs
        try:
            self._validate_required_fields(
                company_profit=company_profit,
                salary=salary,
                dividends=dividends
            )
            self._validate_positive_amount(r_and_d_expenditure, 'r_and_d_expenditure')
            self._validate_positive_amount(capital_investment, 'capital_investment')
        except ValueError as e:
            raise ValueError(f"Invalid input for company owner optimization: {e}")
        
        # Calculate current corporation tax
        corp_tax = self.calculator.calculate_corporation_tax(company_profit)
        
        # Calculate R&D relief (SME scheme: 130% enhancement)
        r_and_d_relief = 0
        if r_and_d_expenditure > 0:
            r_and_d_enhancement_rate = 1.30
            r_and_d_enhanced_deduction = r_and_d_expenditure * r_and_d_enhancement_rate
            r_and_d_relief = r_and_d_enhanced_deduction * TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE
        
        # Calculate capital allowances benefit
        capital_allowance_relief = 0
        if capital_investment > 0:
            aia_qualifying_amount = min(capital_investment, TaxConstants.ANNUAL_INVESTMENT_ALLOWANCE)
            capital_allowance_relief = aia_qualifying_amount * TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE
        
        # Optimal profit extraction strategy
        optimal_salary = self.OPTIMAL_DIRECTOR_SALARY
        remaining_profit = company_profit - optimal_salary - r_and_d_expenditure
        
        optimal_corp_tax = self.calculator.calculate_corporation_tax(remaining_profit)
        profit_after_tax = remaining_profit - optimal_corp_tax['corporation_tax']
        
        recommendations = [
            {
                'strategy': 'Salary Optimization',
                'description': f'Set salary at personal allowance (£{optimal_salary:,})',
                'saving': 'Minimize NI while using personal allowance'
            },
            {
                'strategy': 'Dividend Planning',
                'description': 'Extract profits as dividends rather than salary',
                'saving': 'Lower tax rate and no NI on dividends'
            }
        ]
        
        if r_and_d_expenditure == 0:
            recommendations.append({
                'strategy': 'R&D Tax Relief',
                'description': 'Claim R&D tax relief for qualifying development activities',
                'saving': 'Up to 230% tax deduction (SME scheme)'
            })
        else:
            recommendations.append({
                'strategy': 'R&D Relief Claimed',
                'description': f'R&D relief of £{r_and_d_relief:,.2f} on £{r_and_d_expenditure:,} expenditure',
                'saving': round(r_and_d_relief, 2)
            })
        
        total_reliefs = r_and_d_relief + capital_allowance_relief
        
        return {
            'user_type': 'Company Owner',
            'company_analysis': {
                'profit': company_profit,
                'corporation_tax': corp_tax['corporation_tax'],
                'profit_after_tax': corp_tax['profit_after_tax'],
                'effective_rate': corp_tax['effective_rate']
            },
            'reliefs_claimed': {
                'r_and_d_relief': round(r_and_d_relief, 2),
                'capital_allowance_relief': round(capital_allowance_relief, 2),
                'total_relief': round(total_reliefs, 2)
            },
            'optimal_extraction': {
                'salary': optimal_salary,
                'maximum_dividend': round(profit_after_tax, 2),
                'total_available': round(optimal_salary + profit_after_tax, 2)
            },
            'recommendations': recommendations
        }
    
    def optimize_for_landlord(self,
                            rental_income: float,
                            mortgage_interest: float,
                            other_expenses: float,
                            is_furnished: bool = False,
                            number_of_properties: int = 1) -> Dict[str, Any]:
        """
        Optimize tax position for landlords.
        
        Args:
            rental_income: Gross rental income
            mortgage_interest: Mortgage interest payments
            other_expenses: Other allowable expenses
            is_furnished: Whether properties are furnished
            number_of_properties: Number of rental properties
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Validate inputs
        try:
            self._validate_required_fields(
                rental_income=rental_income,
                mortgage_interest=mortgage_interest,
                other_expenses=other_expenses
            )
            if not isinstance(number_of_properties, int) or number_of_properties < 1:
                raise ValueError(f"number_of_properties must be a positive integer")
            if not isinstance(is_furnished, bool):
                raise ValueError(f"is_furnished must be a boolean")
        except ValueError as e:
            raise ValueError(f"Invalid input for landlord optimization: {e}")
        
        # Apply property allowance if beneficial
        property_allowance = self.reliefs.calculate_property_allowance(rental_income)
        
        use_property_allowance = (rental_income <= self.reliefs.PROPERTY_ALLOWANCE and 
                                 other_expenses + mortgage_interest < self.reliefs.PROPERTY_ALLOWANCE)
        
        if use_property_allowance:
            taxable_income = property_allowance['taxable_income']
            method = 'Property Allowance'
            finance_cost_relief = 0
        else:
            # Post-2017 rules: mortgage interest as basic rate tax reducer
            profit_before_finance_costs = rental_income - other_expenses
            finance_cost_relief = mortgage_interest * TaxConstants.BASIC_RATE
            taxable_income = max(0, profit_before_finance_costs)
            method = 'Expenses + Finance Cost Restriction'
        
        # Calculate tax
        paye = self.calculator.calculate_paye(taxable_income)
        
        # Apply finance cost relief
        if not use_property_allowance and mortgage_interest > 0:
            tax_after_relief = max(0, paye['income_tax'] - finance_cost_relief)
            actual_tax = tax_after_relief + paye['employee_ni']
        else:
            actual_tax = paye['total_employee_deductions']
        
        # Calculate if incorporation would be beneficial
        corp_tax_calc = self.calculator.calculate_corporation_tax(
            rental_income - other_expenses - mortgage_interest
        )
        
        incorporation_saving = actual_tax - corp_tax_calc['corporation_tax']
        
        recommendations = []
        
        if not use_property_allowance and rental_income <= self.reliefs.PROPERTY_ALLOWANCE:
            recommendations.append({
                'strategy': 'Property Allowance',
                'description': f'Consider using £{self.reliefs.PROPERTY_ALLOWANCE:,} property allowance',
                'saving': 'Simplified reporting'
            })
        
        if is_furnished:
            recommendations.append({
                'strategy': 'Replacement of Domestic Items Relief',
                'description': 'Claim relief on replacing furniture and appliances',
                'saving': 'Tax relief on full replacement cost'
            })
        
        if (incorporation_saving > self.INCORPORATION_SAVINGS_THRESHOLD and 
            number_of_properties >= self.INCORPORATION_PROPERTIES_THRESHOLD):
            recommendations.append({
                'strategy': 'Consider Incorporation',
                'description': f'Moving to limited company could save £{incorporation_saving:,.2f}',
                'saving': round(incorporation_saving, 2)
            })
        
        recommendations.append({
            'strategy': 'Joint Ownership',
            'description': 'Consider joint ownership with spouse/partner',
            'saving': 'Utilize lower tax bands and personal allowances'
        })
        
        return {
            'user_type': 'Landlord',
            'property_details': {
                'rental_income': rental_income,
                'mortgage_interest': mortgage_interest,
                'other_expenses': other_expenses,
                'number_of_properties': number_of_properties,
                'is_furnished': is_furnished
            },
            'tax_calculation': {
                'method_used': method,
                'taxable_income': round(taxable_income, 2),
                'income_tax': round(actual_tax, 2),
                'finance_cost_relief': round(finance_cost_relief, 2)
            },
            'incorporation_analysis': {
                'current_tax': round(actual_tax, 2),
                'corporation_tax_if_incorporated': round(corp_tax_calc['corporation_tax'], 2),
                'potential_saving': round(incorporation_saving, 2),
                'recommended': (incorporation_saving > self.INCORPORATION_SAVINGS_THRESHOLD and 
                               number_of_properties >= self.INCORPORATION_PROPERTIES_THRESHOLD)
            },
            'recommendations': recommendations
        }
