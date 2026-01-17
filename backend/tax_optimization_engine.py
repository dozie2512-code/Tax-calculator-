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
    
    def _calculate_tax_position(self, income: float, description: str = "income") -> Dict[str, Any]:
        """
        Helper method to calculate comprehensive tax position for a given income.
        Reduces repetitive calculations across different user types.
        
        Args:
            income: Total income amount
            description: Description of income type for reporting
            
        Returns:
            Dictionary with tax calculations
        """
        paye = self.calculator.calculate_paye(income)
        return {
            'income': income,
            'description': description,
            'paye': paye,
            'net_income': paye['net_income'],
            'total_tax': paye['total_employee_deductions']
        }
    
    def optimize_for_director(self, 
                             salary: float,
                             dividends: float,
                             company_profit: float,
                             pension_contribution: float = 0) -> Dict[str, Any]:
        """
        Optimize tax position for company directors.
        
        Directors can optimize by balancing salary vs dividends,
        maximizing pension contributions, and efficient profit extraction.
        
        Strategy:
        1. Set salary at personal allowance (£12,570) to minimize NI while using allowance
        2. Extract remaining profits as dividends (lower tax rate, no NI)
        3. Consider employer pension contributions (corporation tax deductible, no NI)
        4. Split dividend payments across tax years to maximize dividend allowance
        
        Args:
            salary: Current annual salary (must be non-negative)
            dividends: Proposed dividend amount (must be non-negative)
            company_profit: Company's taxable profit (must be non-negative)
            pension_contribution: Pension contribution amount (default: 0, must be non-negative)
            
        Returns:
            Dictionary with optimization analysis and recommendations including:
                - current_position: Current tax situation
                - optimal_position: Recommended optimal structure
                - potential_saving: Tax savings from optimization
                - recommendations: List of actionable strategies
                
        Raises:
            ValueError: If any required field is missing, negative, or invalid
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
        
        # Optimal salary strategy: Use full personal allowance to minimize NI
        optimal_salary = self.OPTIMAL_DIRECTOR_SALARY
        optimal_paye = self.calculator.calculate_paye(optimal_salary)
        
        # Calculate remaining profit after salary and corporation tax
        remaining_profit = company_profit - optimal_salary
        optimal_corp_tax = self.calculator.calculate_corporation_tax(remaining_profit)
        
        # Maximum dividend that can be paid
        profit_after_corp_tax = remaining_profit - optimal_corp_tax['corporation_tax']
        
        # Calculate dividend tax on this amount
        optimal_dividend_tax = self.calculator.calculate_dividend_tax(
            profit_after_corp_tax, optimal_salary
        )
        
        # Total tax under optimal strategy
        optimal_total_tax = (optimal_paye['total_employee_deductions'] + 
                           optimal_corp_tax['corporation_tax'] + 
                           optimal_dividend_tax['dividend_tax'])
        
        # Current total tax
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
            'recommendations': recommendations,
            'detailed_calculations': {
                'paye': paye,
                'dividend_tax': dividend_tax,
                'corporation_tax': corp_tax,
                'optimal_paye': optimal_paye,
                'optimal_dividend_tax': optimal_dividend_tax,
                'optimal_corporation_tax': optimal_corp_tax
            }
        }
    
    def optimize_for_sole_trader(self,
                                 trading_income: float,
                                 allowable_expenses: float,
                                 pension_contribution: float = 0,
                                 capital_allowances: float = 0) -> Dict[str, Any]:
        """
        Optimize tax position for sole traders.
        
        Sole traders can optimize through expense claims, pension contributions,
        capital allowances, and using available reliefs.
        
        Strategy:
        1. Track all allowable business expenses (20-45% tax relief)
        2. Claim Annual Investment Allowance (100% first-year relief on equipment)
        3. Make pension contributions for tax relief (up to 45%)
        4. Consider trading allowance (£1,000) vs expense claims
        5. Income splitting with spouse/partner for additional tax efficiency
        
        Args:
            trading_income: Gross trading income (must be non-negative)
            allowable_expenses: Claimed business expenses (must be non-negative)
            pension_contribution: Pension contribution amount (default: 0, must be non-negative)
            capital_allowances: Capital allowances claimed (default: 0, must be non-negative)
            
        Returns:
            Dictionary with optimization analysis and recommendations including:
                - income_analysis: Breakdown of income and expenses
                - tax_position: Current tax calculations
                - recommendations: List of tax-saving strategies
                
        Raises:
            ValueError: If any required field is missing, negative, or invalid
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
        taxable_profit = trading_income - allowable_expenses - capital_allowances
        
        # Apply trading allowance if beneficial
        trading_allowance = self.reliefs.calculate_trading_allowance(trading_income)
        
        # Compare: expenses vs trading allowance
        profit_with_expenses = taxable_profit
        profit_with_allowance = trading_income - self.reliefs.TRADING_ALLOWANCE
        
        # Use trading allowance only if income is under the limit OR if it results in lower taxable profit
        use_allowance = (trading_income <= self.reliefs.TRADING_ALLOWANCE) or (profit_with_allowance < profit_with_expenses and allowable_expenses + capital_allowances == 0)
        
        final_taxable_profit = profit_with_allowance if use_allowance else profit_with_expenses
        
        # Calculate tax on profit
        paye = self.calculator.calculate_paye(final_taxable_profit)
        
        # Calculate pension relief
        pension_relief = None
        if pension_contribution > 0:
            pension_relief = self.reliefs.calculate_pension_relief(
                pension_contribution, final_taxable_profit
            )
            # Reduce taxable income by pension contribution
            adjusted_profit = max(0, final_taxable_profit - pension_contribution)
            adjusted_paye = self.calculator.calculate_paye(adjusted_profit)
        else:
            adjusted_paye = paye
        
        # Generate recommendations
        recommendations = []
        
        # Expense tracking recommendation - suggest if expenses seem low (< 20% of income)
        expense_ratio_threshold = 0.20
        if allowable_expenses < trading_income * expense_ratio_threshold:
            recommendations.append({
                'strategy': 'Enhance Expense Tracking',
                'description': 'Review and claim all allowable business expenses (travel, equipment, home office)',
                'saving': f'Up to {int(TaxConstants.ADDITIONAL_RATE * 100)}% tax relief on expenses'
            })
        
        # Capital allowances - use constant for AIA limit
        recommendations.append({
            'strategy': 'Annual Investment Allowance (AIA)',
            'description': f'Claim 100% first-year allowance on equipment up to £{TaxConstants.ANNUAL_INVESTMENT_ALLOWANCE:,}',
            'saving': 'Immediate tax relief on capital investments'
        })
        
        # Pension contributions
        if pension_contribution == 0:
            recommendations.append({
                'strategy': 'Pension Contributions',
                'description': 'Make personal pension contributions for tax relief',
                'saving': f'Up to 45% tax relief (£{self.reliefs.PENSION_ANNUAL_ALLOWANCE:,} annual allowance)'
            })
        
        # Trading allowance
        if not use_allowance and trading_income <= 1000:
            recommendations.append({
                'strategy': 'Trading Allowance',
                'description': f'Consider using £{self.reliefs.TRADING_ALLOWANCE:,} trading allowance instead of expenses',
                'saving': 'Simplified reporting'
            })
        
        # Income splitting
        recommendations.append({
            'strategy': 'Income Splitting',
            'description': 'Consider employing spouse/partner if they have lower income',
            'saving': 'Utilize their personal allowance and lower tax bands'
        })
        
        # Class 2 NI voluntary contributions - use constant for personal allowance
        if final_taxable_profit < TaxConstants.PERSONAL_ALLOWANCE:
            # Class 2 NI weekly rate (approximate)
            class_2_weekly_rate = 3.45
            class_2_annual_cost = class_2_weekly_rate * 52
            recommendations.append({
                'strategy': 'Class 2 NI Contributions',
                'description': f'Make voluntary Class 2 NI contributions (£{class_2_weekly_rate}/week) to protect state pension',
                'saving': f'Pension protection for £{class_2_annual_cost:.2f}/year'
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
            'recommendations': recommendations,
            'potential_savings': {
                'pension_relief': pension_relief['total_relief'] if pension_relief else 0,
                'trading_allowance_benefit': round(abs(profit_with_expenses - profit_with_allowance) * 0.20, 2) if use_allowance else 0
            }
        }
    
    def optimize_for_company_owner(self,
                                   company_profit: float,
                                   salary: float,
                                   dividends: float,
                                   r_and_d_expenditure: float = 0,
                                   capital_investment: float = 0) -> Dict[str, Any]:
        """
        Optimize tax position for company owners.
        
        Focuses on corporation tax planning, R&D relief, capital allowances,
        and efficient profit extraction strategies.
        
        Strategy:
        1. Set director salary at personal allowance level
        2. Extract profits as dividends (lower tax, no NI)
        3. Claim R&D tax relief (up to 230% deduction for SMEs)
        4. Utilize Annual Investment Allowance (100% first-year relief)
        5. Consider Entrepreneur's Relief and Patent Box
        6. Make employer pension contributions (corporation tax deductible)
        
        Args:
            company_profit: Company's taxable profit (must be non-negative)
            salary: Director's salary (must be non-negative)
            dividends: Dividends paid (must be non-negative)
            r_and_d_expenditure: Research & Development costs (default: 0, must be non-negative)
            capital_investment: Capital investment in qualifying assets (default: 0, must be non-negative)
            
        Returns:
            Dictionary with optimization analysis and recommendations including:
                - company_analysis: Corporation tax details
                - reliefs_claimed: R&D and capital allowance benefits
                - optimal_extraction: Recommended profit extraction strategy
                
        Raises:
            ValueError: If any required field is missing, negative, or invalid
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
        
        # Calculate R&D relief (SME scheme: 130% enhancement on expenditure = 230% total deduction)
        r_and_d_relief = 0
        if r_and_d_expenditure > 0:
            r_and_d_enhancement_rate = 1.30  # 130% enhancement
            r_and_d_enhanced_deduction = r_and_d_expenditure * r_and_d_enhancement_rate
            r_and_d_relief = r_and_d_enhanced_deduction * TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE
        
        # Calculate capital allowances benefit using AIA
        capital_allowance_relief = 0
        if capital_investment > 0:
            # Annual Investment Allowance (AIA) - 100% first year
            aia_qualifying_amount = min(capital_investment, TaxConstants.ANNUAL_INVESTMENT_ALLOWANCE)
            capital_allowance_relief = aia_qualifying_amount * TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE
        
        # Optimal profit extraction strategy
        optimal_salary = self.OPTIMAL_DIRECTOR_SALARY
        remaining_profit = company_profit - optimal_salary - r_and_d_expenditure
        
        # Calculate tax under optimal structure
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
                'saving': 'Up to 230% tax deduction (SME scheme) or 13% tax credit'
            })
        else:
            recommendations.append({
                'strategy': 'R&D Relief Claimed',
                'description': f'R&D relief of £{r_and_d_relief:,.2f} on £{r_and_d_expenditure:,} expenditure',
                'saving': round(r_and_d_relief, 2)
            })
        
        if capital_investment == 0:
            recommendations.append({
                'strategy': 'Annual Investment Allowance',
                'description': 'Invest in qualifying equipment for 100% first-year allowance',
                'saving': f'Up to £{TaxConstants.ANNUAL_INVESTMENT_ALLOWANCE:,} at {int(TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE * 100)}-{int(TaxConstants.CORPORATION_TAX_MAIN_RATE * 100)}% tax relief'
            })
        else:
            recommendations.append({
                'strategy': 'Capital Allowances Claimed',
                'description': f'£{capital_allowance_relief:,.2f} relief on £{capital_investment:,} investment',
                'saving': round(capital_allowance_relief, 2)
            })
        
        recommendations.extend([
            {
                'strategy': 'Entrepreneur\'s Relief',
                'description': 'When selling business, claim Business Asset Disposal Relief (10% CGT)',
                'saving': f'Up to £1M lifetime allowance at reduced {int(TaxConstants.CGT_BASIC_RATE * 100)}% rate'
            },
            {
                'strategy': 'Patent Box',
                'description': 'If holding patents, apply reduced 10% corporation tax rate on patent income',
                'saving': f'Up to {int((TaxConstants.CORPORATION_TAX_MAIN_RATE - 0.10) * 100)}% tax reduction on patent profits'
            },
            {
                'strategy': 'Employer Pension Contributions',
                'description': 'Make employer pension contributions (corporation tax deductible)',
                'saving': f'{int(TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE * 100)}-{int(TaxConstants.CORPORATION_TAX_MAIN_RATE * 100)}% corporation tax relief + no NI'
            }
        ])
        
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
        
        Focuses on property allowances, mortgage interest relief,
        capital allowances, and incorporation considerations.
        
        Strategy:
        1. Consider property allowance (£1,000) vs expense claims
        2. Utilize mortgage interest tax reducer (20% relief post-2017 rules)
        3. Claim Replacement of Domestic Items Relief for furnished properties
        4. Maximize allowable expenses (repairs, insurance, agent fees)
        5. Consider incorporation for portfolio landlords (3+ properties)
        6. Use joint ownership for income splitting
        
        Args:
            rental_income: Gross rental income (must be non-negative)
            mortgage_interest: Mortgage interest payments (must be non-negative)
            other_expenses: Other allowable expenses (must be non-negative)
            is_furnished: Whether properties are furnished (default: False)
            number_of_properties: Number of rental properties (default: 1, must be positive)
            
        Returns:
            Dictionary with optimization analysis and recommendations including:
                - property_details: Property portfolio information
                - tax_calculation: Current tax position
                - incorporation_analysis: Should you incorporate?
                
        Raises:
            ValueError: If any required field is missing, negative, or invalid
        """
        # Validate inputs
        try:
            self._validate_required_fields(
                rental_income=rental_income,
                mortgage_interest=mortgage_interest,
                other_expenses=other_expenses
            )
            if not isinstance(number_of_properties, int) or number_of_properties < 1:
                raise ValueError(f"number_of_properties must be a positive integer, got {number_of_properties}")
            if not isinstance(is_furnished, bool):
                raise ValueError(f"is_furnished must be a boolean, got {type(is_furnished).__name__}")
        except ValueError as e:
            raise ValueError(f"Invalid input for landlord optimization: {e}")
        # Apply property allowance if beneficial
        property_allowance = self.reliefs.calculate_property_allowance(rental_income)
        
        # Check if property allowance is better than claiming expenses
        use_property_allowance = (rental_income <= self.reliefs.PROPERTY_ALLOWANCE and 
                                 other_expenses + mortgage_interest < self.reliefs.PROPERTY_ALLOWANCE)
        
        if use_property_allowance:
            taxable_income = property_allowance['taxable_income']
            method = 'Property Allowance'
        else:
            # Post-2017 rules: mortgage interest as basic rate tax reducer (20% credit)
            profit_before_finance_costs = rental_income - other_expenses
            
            # Finance cost restriction: mortgage interest only gets 20% tax credit
            finance_cost_relief = mortgage_interest * TaxConstants.BASIC_RATE
            
            taxable_income = max(0, profit_before_finance_costs)
            method = 'Expenses + Finance Cost Restriction'
        
        # Calculate tax
        paye = self.calculator.calculate_paye(taxable_income)
        
        # Apply finance cost relief as tax reducer
        if not use_property_allowance and mortgage_interest > 0:
            tax_after_relief = max(0, paye['income_tax'] - finance_cost_relief)
            actual_tax = tax_after_relief + paye['employee_ni']
        else:
            actual_tax = paye['total_employee_deductions']
        
        # Calculate if incorporation would be beneficial
        # Company would pay corporation tax instead
        corp_tax_calc = self.calculator.calculate_corporation_tax(
            rental_income - other_expenses - mortgage_interest
        )
        
        incorporation_saving = actual_tax - corp_tax_calc['corporation_tax']
        
        recommendations = []
        
        # Property allowance
        if not use_property_allowance and rental_income <= self.reliefs.PROPERTY_ALLOWANCE:
            recommendations.append({
                'strategy': 'Property Allowance',
                'description': f'Consider using £{self.reliefs.PROPERTY_ALLOWANCE:,} property allowance',
                'saving': 'Simplified reporting, no need to track expenses'
            })
        
        # Furnished property relief
        if is_furnished:
            recommendations.append({
                'strategy': 'Replacement of Domestic Items Relief',
                'description': 'Claim relief on replacing furniture, appliances, and kitchenware',
                'saving': 'Tax relief on full replacement cost'
            })
        else:
            recommendations.append({
                'strategy': 'Consider Furnished Lettings',
                'description': 'Furnished properties can claim replacement relief',
                'saving': 'Additional tax deductions'
            })
        
        # Wear and tear allowance (for furnished properties)
        if is_furnished:
            recommendations.append({
                'strategy': 'Wear and Tear Allowance',
                'description': 'If fully furnished, claim replacement relief',
                'saving': 'Tax deductible furniture replacements'
            })
        
        # Capital allowances
        recommendations.append({
            'strategy': 'Capital Allowances',
            'description': 'Claim capital allowances on fixtures (heating, built-in furniture)',
            'saving': 'Tax relief on qualifying fixtures'
        })
        
        # Incorporation consideration - use constants for thresholds
        if (incorporation_saving > self.INCORPORATION_SAVINGS_THRESHOLD and 
            number_of_properties >= self.INCORPORATION_PROPERTIES_THRESHOLD):
            recommendations.append({
                'strategy': 'Consider Incorporation',
                'description': f'Moving to limited company structure could save £{incorporation_saving:,.2f}',
                'saving': round(incorporation_saving, 2),
                'notes': 'Lower tax rate but stamp duty and CGT on transfer'
            })
        
        # Expense optimization - suggest if savings potential exists
        recommendations.append({
            'strategy': 'Maximize Allowable Expenses',
            'description': 'Claim all allowable expenses: repairs, insurance, agent fees, travel',
            'saving': f'Tax relief at marginal rate ({int(TaxConstants.BASIC_RATE * 100)}-{int(TaxConstants.ADDITIONAL_RATE * 100)}%)'
        })
        
        # Property business election
        if number_of_properties > 1:
            recommendations.append({
                'strategy': 'Property Business Election',
                'description': 'Treat all properties as a single business for loss relief',
                'saving': 'Offset losses between properties'
            })
        
        # Spouse/partner income splitting
        recommendations.append({
            'strategy': 'Joint Ownership',
            'description': 'Consider joint ownership with spouse/partner in optimal ratio',
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
                'finance_cost_relief': round(finance_cost_relief, 2) if not use_property_allowance else 0
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
    
    def comprehensive_tax_plan(self,
                              user_type: str,
                              **kwargs) -> Dict[str, Any]:
        """
        Generate comprehensive tax plan for any user type.
        
        Routes the request to the appropriate optimization method based on user type.
        Includes error handling for unknown user types and missing parameters.
        
        Args:
            user_type: Type of user ('director', 'sole_trader', 'company_owner', 'landlord')
            **kwargs: User-specific parameters required by the optimization method
            
        Returns:
            Comprehensive tax optimization plan
            
        Raises:
            ValueError: If user_type is unknown or required parameters are missing
        """
        valid_types = ['director', 'sole_trader', 'company_owner', 'landlord']
        
        if not user_type:
            raise ValueError("user_type is required")
        
        if user_type not in valid_types:
            raise ValueError(
                f"Unknown user type: '{user_type}'. "
                f"Valid types are: {', '.join(valid_types)}"
            )
        
        try:
            if user_type == 'director':
                return self.optimize_for_director(**kwargs)
            elif user_type == 'sole_trader':
                return self.optimize_for_sole_trader(**kwargs)
            elif user_type == 'company_owner':
                return self.optimize_for_company_owner(**kwargs)
            elif user_type == 'landlord':
                return self.optimize_for_landlord(**kwargs)
        except TypeError as e:
            # Handle missing required parameters
            raise ValueError(
                f"Missing required parameters for {user_type} optimization. "
                f"Error: {e}"
            )
        except ValueError as e:
            # Re-raise ValueError with context
            raise ValueError(
                f"Error in {user_type} optimization: {e}"
            )
