"""
Tax Optimization Strategies for Different User Types
Provides tailored tax-saving recommendations based on HMRC guidelines
"""

from typing import Dict, Any, List
from backend.uk_tax_calculator import UKTaxCalculator, TaxReliefs


class TaxOptimizationEngine:
    """
    Provides tax optimization strategies for different user types.
    """
    
    def __init__(self):
        """Initialize the optimization engine."""
        self.calculator = UKTaxCalculator()
        self.reliefs = TaxReliefs()
    
    def optimize_for_director(self, 
                             salary: float,
                             dividends: float,
                             company_profit: float,
                             pension_contribution: float = 0) -> Dict[str, Any]:
        """
        Optimize tax position for company directors.
        
        Directors can optimize by balancing salary vs dividends,
        maximizing pension contributions, and efficient profit extraction.
        
        Args:
            salary: Current annual salary
            dividends: Proposed dividend amount
            company_profit: Company's taxable profit
            pension_contribution: Pension contribution amount
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Calculate current position
        paye = self.calculator.calculate_paye(salary)
        dividend_tax = self.calculator.calculate_dividend_tax(dividends, salary)
        corp_tax = self.calculator.calculate_corporation_tax(company_profit)
        
        # Calculate pension relief if applicable
        pension_relief = None
        if pension_contribution > 0:
            pension_relief = self.reliefs.calculate_pension_relief(pension_contribution, salary)
        
        # Optimal salary strategy: NI threshold (£9,100) or personal allowance (£12,570)
        optimal_salary = 12_570  # Use full personal allowance
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
        
        Args:
            trading_income: Gross trading income
            allowable_expenses: Claimed business expenses
            pension_contribution: Pension contribution amount
            capital_allowances: Capital allowances claimed
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Calculate taxable profit
        taxable_profit = trading_income - allowable_expenses - capital_allowances
        
        # Apply trading allowance if beneficial
        trading_allowance = self.reliefs.calculate_trading_allowance(trading_income)
        
        # Compare: expenses vs trading allowance
        profit_with_expenses = taxable_profit
        profit_with_allowance = trading_income - self.reliefs.TRADING_ALLOWANCE
        
        # Use trading allowance only if income is under £1,000 OR if it results in lower taxable profit
        use_allowance = (trading_income <= 1000) or (profit_with_allowance < profit_with_expenses and allowable_expenses + capital_allowances == 0)
        
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
        
        # Expense tracking recommendation
        if allowable_expenses < trading_income * 0.2:
            recommendations.append({
                'strategy': 'Enhance Expense Tracking',
                'description': 'Review and claim all allowable business expenses (travel, equipment, home office)',
                'saving': 'Up to 45% tax relief on expenses'
            })
        
        # Capital allowances
        recommendations.append({
            'strategy': 'Annual Investment Allowance (AIA)',
            'description': f'Claim 100% first-year allowance on equipment up to £1,000,000',
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
        
        # Class 2 NI voluntary contributions
        if final_taxable_profit < 12_570:
            recommendations.append({
                'strategy': 'Class 2 NI Contributions',
                'description': 'Make voluntary Class 2 NI contributions (£3.45/week) to protect state pension',
                'saving': 'Pension protection for £179.40/year'
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
        
        Args:
            company_profit: Company's taxable profit
            salary: Director's salary
            dividends: Dividends paid
            r_and_d_expenditure: Research & Development costs
            capital_investment: Capital investment in qualifying assets
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Calculate current corporation tax
        corp_tax = self.calculator.calculate_corporation_tax(company_profit)
        
        # Calculate R&D relief (SME scheme: 130% deduction = 230% total)
        r_and_d_relief = 0
        if r_and_d_expenditure > 0:
            r_and_d_enhanced_deduction = r_and_d_expenditure * 1.30  # 130% enhancement
            r_and_d_relief = r_and_d_enhanced_deduction * 0.19  # Tax saving at 19%
        
        # Calculate capital allowances benefit
        capital_allowance_relief = 0
        if capital_investment > 0:
            # Annual Investment Allowance (AIA) - 100% first year
            capital_allowance_relief = min(capital_investment, 1_000_000) * 0.19
        
        # Optimal profit extraction
        optimal_salary = 12_570  # Personal allowance
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
                'saving': 'Up to £1,000,000 at 19-25% tax relief'
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
                'saving': 'Up to £1M lifetime allowance at reduced 10% rate'
            },
            {
                'strategy': 'Patent Box',
                'description': 'If holding patents, apply reduced 10% corporation tax rate on patent income',
                'saving': 'Up to 15% tax reduction on patent profits'
            },
            {
                'strategy': 'Employer Pension Contributions',
                'description': 'Make employer pension contributions (corporation tax deductible)',
                'saving': '19-25% corporation tax relief + no NI'
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
        
        Args:
            rental_income: Gross rental income
            mortgage_interest: Mortgage interest payments
            other_expenses: Other allowable expenses
            is_furnished: Whether properties are furnished
            number_of_properties: Number of rental properties
            
        Returns:
            Dictionary with optimization analysis and recommendations
        """
        # Apply property allowance if beneficial
        property_allowance = self.reliefs.calculate_property_allowance(rental_income)
        
        # Check if property allowance is better than claiming expenses
        use_property_allowance = (rental_income <= self.reliefs.PROPERTY_ALLOWANCE and 
                                 other_expenses + mortgage_interest < self.reliefs.PROPERTY_ALLOWANCE)
        
        if use_property_allowance:
            taxable_income = property_allowance['taxable_income']
            method = 'Property Allowance'
        else:
            # Post-2017 rules: mortgage interest as basic rate tax reducer (20%)
            profit_before_finance_costs = rental_income - other_expenses
            
            # Finance cost restriction (mortgage interest)
            finance_cost_relief = mortgage_interest * 0.20  # Only 20% credit
            
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
        
        # Incorporation consideration
        if incorporation_saving > 1000 and number_of_properties >= 3:
            recommendations.append({
                'strategy': 'Consider Incorporation',
                'description': f'Moving to limited company structure could save £{incorporation_saving:,.2f}',
                'saving': round(incorporation_saving, 2),
                'notes': 'Lower tax rate but stamp duty and CGT on transfer'
            })
        
        # Expense optimization
        recommendations.append({
            'strategy': 'Maximize Allowable Expenses',
            'description': 'Claim all allowable expenses: repairs, insurance, agent fees, travel',
            'saving': 'Tax relief at marginal rate (20-45%)'
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
                'recommended': incorporation_saving > 1000 and number_of_properties >= 3
            },
            'recommendations': recommendations
        }
    
    def comprehensive_tax_plan(self,
                              user_type: str,
                              **kwargs) -> Dict[str, Any]:
        """
        Generate comprehensive tax plan for any user type.
        
        Args:
            user_type: Type of user ('director', 'sole_trader', 'company_owner', 'landlord')
            **kwargs: User-specific parameters
            
        Returns:
            Comprehensive tax optimization plan
        """
        if user_type == 'director':
            return self.optimize_for_director(**kwargs)
        elif user_type == 'sole_trader':
            return self.optimize_for_sole_trader(**kwargs)
        elif user_type == 'company_owner':
            return self.optimize_for_company_owner(**kwargs)
        elif user_type == 'landlord':
            return self.optimize_for_landlord(**kwargs)
        else:
            return {
                'error': f'Unknown user type: {user_type}',
                'valid_types': ['director', 'sole_trader', 'company_owner', 'landlord']
            }
