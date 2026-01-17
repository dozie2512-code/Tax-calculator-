"""
Tax Optimization Engine for UK Tax Calculations

Provides optimization calculations for different taxpayer categories:
- Company Directors
- Sole Traders
- Company Owners
- Landlords
"""


class TaxOptimizationEngine:
    """
    Engine for calculating optimized tax positions for different taxpayer categories.
    Uses UK tax rates and allowances for calculations.
    """
    
    # UK Tax Rates (2023/2024 Tax Year)
    PERSONAL_ALLOWANCE = 12570
    BASIC_RATE_LIMIT = 50270
    HIGHER_RATE_LIMIT = 125140
    
    BASIC_RATE = 0.20
    HIGHER_RATE = 0.40
    ADDITIONAL_RATE = 0.45
    
    DIVIDEND_ALLOWANCE = 1000
    DIVIDEND_BASIC_RATE = 0.0875
    DIVIDEND_HIGHER_RATE = 0.3375
    DIVIDEND_ADDITIONAL_RATE = 0.3935
    
    NI_LOWER_LIMIT = 12570
    NI_UPPER_LIMIT = 50270
    NI_RATE_PRIMARY = 0.12
    NI_RATE_ADDITIONAL = 0.02
    
    # National Insurance Class 2 & 4 (for sole traders)
    NI_CLASS2_RATE = 163.80  # Annual flat rate for 2023/24
    NI_CLASS2_THRESHOLD = 6725  # Small profits threshold
    NI_CLASS4_LOWER_RATE = 0.09  # 9% on profits £12,570-£50,270
    NI_CLASS4_UPPER_RATE = 0.02  # 2% on profits above £50,270
    
    CORPORATION_TAX_RATE = 0.19
    
    # R&D and Investment Allowances
    RD_ADDITIONAL_RELIEF = 0.30  # 30% additional relief (total 130% deduction)
    RD_TAX_CREDIT_DISPLAY = 130  # Display value
    ANNUAL_INVESTMENT_ALLOWANCE = 1000000  # £1M AIA limit
    
    def __init__(self):
        """Initialize the tax optimization engine."""
        pass
    
    def calculate_income_tax(self, income):
        """Calculate income tax on a given income."""
        if income <= self.PERSONAL_ALLOWANCE:
            return 0
        
        taxable_income = income - self.PERSONAL_ALLOWANCE
        tax = 0
        
        if taxable_income <= (self.BASIC_RATE_LIMIT - self.PERSONAL_ALLOWANCE):
            tax = taxable_income * self.BASIC_RATE
        elif taxable_income <= (self.HIGHER_RATE_LIMIT - self.PERSONAL_ALLOWANCE):
            tax = (self.BASIC_RATE_LIMIT - self.PERSONAL_ALLOWANCE) * self.BASIC_RATE
            tax += (taxable_income - (self.BASIC_RATE_LIMIT - self.PERSONAL_ALLOWANCE)) * self.HIGHER_RATE
        else:
            tax = (self.BASIC_RATE_LIMIT - self.PERSONAL_ALLOWANCE) * self.BASIC_RATE
            tax += (self.HIGHER_RATE_LIMIT - self.BASIC_RATE_LIMIT) * self.HIGHER_RATE
            tax += (taxable_income - (self.HIGHER_RATE_LIMIT - self.PERSONAL_ALLOWANCE)) * self.ADDITIONAL_RATE
        
        return round(tax, 2)
    
    def calculate_dividend_tax(self, dividends, other_income=0):
        """Calculate dividend tax."""
        if dividends <= self.DIVIDEND_ALLOWANCE:
            return 0
        
        taxable_dividends = dividends - self.DIVIDEND_ALLOWANCE
        total_income = other_income + dividends
        tax = 0
        
        if total_income <= self.BASIC_RATE_LIMIT:
            tax = taxable_dividends * self.DIVIDEND_BASIC_RATE
        elif other_income < self.BASIC_RATE_LIMIT:
            basic_rate_dividends = min(taxable_dividends, self.BASIC_RATE_LIMIT - other_income)
            higher_rate_dividends = taxable_dividends - basic_rate_dividends
            tax = basic_rate_dividends * self.DIVIDEND_BASIC_RATE
            tax += higher_rate_dividends * self.DIVIDEND_HIGHER_RATE
        elif total_income <= self.HIGHER_RATE_LIMIT:
            tax = taxable_dividends * self.DIVIDEND_HIGHER_RATE
        else:
            if other_income < self.HIGHER_RATE_LIMIT:
                higher_rate_dividends = min(taxable_dividends, self.HIGHER_RATE_LIMIT - other_income)
                additional_rate_dividends = taxable_dividends - higher_rate_dividends
                tax = higher_rate_dividends * self.DIVIDEND_HIGHER_RATE
                tax += additional_rate_dividends * self.DIVIDEND_ADDITIONAL_RATE
            else:
                tax = taxable_dividends * self.DIVIDEND_ADDITIONAL_RATE
        
        return round(tax, 2)
    
    def calculate_national_insurance(self, income):
        """Calculate National Insurance contributions."""
        if income <= self.NI_LOWER_LIMIT:
            return 0
        
        ni = 0
        if income <= self.NI_UPPER_LIMIT:
            ni = (income - self.NI_LOWER_LIMIT) * self.NI_RATE_PRIMARY
        else:
            ni = (self.NI_UPPER_LIMIT - self.NI_LOWER_LIMIT) * self.NI_RATE_PRIMARY
            ni += (income - self.NI_UPPER_LIMIT) * self.NI_RATE_ADDITIONAL
        
        return round(ni, 2)
    
    def calculate_class4_ni(self, profit):
        """Calculate National Insurance Class 4 contributions for sole traders."""
        if profit <= self.NI_LOWER_LIMIT:
            return 0
        
        ni = 0
        if profit <= self.NI_UPPER_LIMIT:
            ni = (profit - self.NI_LOWER_LIMIT) * self.NI_CLASS4_LOWER_RATE
        else:
            ni = (self.NI_UPPER_LIMIT - self.NI_LOWER_LIMIT) * self.NI_CLASS4_LOWER_RATE
            ni += (profit - self.NI_UPPER_LIMIT) * self.NI_CLASS4_UPPER_RATE
        
        return round(ni, 2)
    
    def optimize_director(self, data):
        """
        Optimize tax position for a company director.
        
        Args:
            data: Dictionary with salary, dividends, company_profit, pension_contribution
        
        Returns:
            Dictionary with tax calculations and recommendations
        """
        salary = data.get('salary', 0)
        dividends = data.get('dividends', 0)
        company_profit = data.get('company_profit', 0)
        pension = data.get('pension_contribution', 0)
        
        # Calculate taxes
        income_tax = self.calculate_income_tax(salary)
        dividend_tax = self.calculate_dividend_tax(dividends, salary)
        ni_contributions = self.calculate_national_insurance(salary)
        corporation_tax = company_profit * self.CORPORATION_TAX_RATE
        
        # Calculate pension relief
        pension_relief = pension * self.BASIC_RATE
        
        total_tax = income_tax + dividend_tax + ni_contributions + corporation_tax
        total_income = salary + dividends
        net_income = total_income - income_tax - dividend_tax - ni_contributions
        effective_rate = (total_tax / total_income * 100) if total_income > 0 else 0
        
        # Recommendations
        recommendations = []
        if salary < self.NI_LOWER_LIMIT:
            recommendations.append(f"Consider increasing salary to £{self.NI_LOWER_LIMIT:,.2f} to maximize NI credits")
        if dividends > 0 and salary > self.BASIC_RATE_LIMIT:
            recommendations.append("Consider reducing salary and increasing dividends for better tax efficiency")
        if pension < 40000:
            recommendations.append(f"You can contribute up to £{40000 - pension:,.2f} more to pension for tax relief")
        
        return {
            'category': 'Company Director',
            'summary': {
                'total_income': round(total_income, 2),
                'net_income': round(net_income, 2),
                'total_tax': round(total_tax, 2),
                'effective_tax_rate': round(effective_rate, 2)
            },
            'breakdown': {
                'salary': round(salary, 2),
                'dividends': round(dividends, 2),
                'income_tax': round(income_tax, 2),
                'dividend_tax': round(dividend_tax, 2),
                'national_insurance': round(ni_contributions, 2),
                'corporation_tax': round(corporation_tax, 2),
                'pension_contribution': round(pension, 2),
                'pension_relief': round(pension_relief, 2)
            },
            'recommendations': recommendations
        }
    
    def optimize_sole_trader(self, data):
        """
        Optimize tax position for a sole trader.
        
        Args:
            data: Dictionary with trading_income, allowable_expenses, pension_contribution, capital_allowances
        
        Returns:
            Dictionary with tax calculations and recommendations
        """
        trading_income = data.get('trading_income', 0)
        expenses = data.get('allowable_expenses', 0)
        pension = data.get('pension_contribution', 0)
        capital_allowances = data.get('capital_allowances', 0)
        
        # Calculate taxable profit
        taxable_profit = trading_income - expenses - capital_allowances - pension
        
        # Calculate taxes
        income_tax = self.calculate_income_tax(taxable_profit)
        ni_class2 = self.NI_CLASS2_RATE if taxable_profit > self.NI_CLASS2_THRESHOLD else 0
        ni_class4 = self.calculate_class4_ni(taxable_profit)
        
        total_tax = income_tax + ni_class2 + ni_class4
        net_income = taxable_profit - total_tax
        effective_rate = (total_tax / trading_income * 100) if trading_income > 0 else 0
        
        # Recommendations
        recommendations = []
        if expenses < trading_income * 0.3:
            recommendations.append("Review expenses - you may be missing legitimate business deductions")
        if capital_allowances == 0:
            recommendations.append("Consider claiming Annual Investment Allowance for equipment purchases")
        if pension < 40000:
            recommendations.append(f"Pension contributions provide tax relief - you can contribute up to £{40000 - pension:,.2f} more")
        
        return {
            'category': 'Sole Trader',
            'summary': {
                'trading_income': round(trading_income, 2),
                'taxable_profit': round(taxable_profit, 2),
                'net_income': round(net_income, 2),
                'total_tax': round(total_tax, 2),
                'effective_tax_rate': round(effective_rate, 2)
            },
            'breakdown': {
                'trading_income': round(trading_income, 2),
                'allowable_expenses': round(expenses, 2),
                'capital_allowances': round(capital_allowances, 2),
                'pension_contribution': round(pension, 2),
                'income_tax': round(income_tax, 2),
                'ni_class_2': round(ni_class2, 2),
                'ni_class_4': round(ni_class4, 2)
            },
            'recommendations': recommendations
        }
    
    def optimize_company_owner(self, data):
        """
        Optimize tax position for a company owner.
        
        Args:
            data: Dictionary with company_profit, salary, dividends, r_and_d_expenditure, capital_investment
        
        Returns:
            Dictionary with tax calculations and recommendations
        """
        company_profit = data.get('company_profit', 0)
        salary = data.get('salary', 0)
        dividends = data.get('dividends', 0)
        rd_expenditure = data.get('r_and_d_expenditure', 0)
        capital_investment = data.get('capital_investment', 0)
        
        # Calculate R&D tax relief (130% deduction = 100% cost + 30% additional relief)
        rd_relief = rd_expenditure * self.RD_ADDITIONAL_RELIEF
        adjusted_profit = company_profit - rd_relief - capital_investment
        
        # Calculate taxes
        corporation_tax = max(0, adjusted_profit * self.CORPORATION_TAX_RATE)
        income_tax = self.calculate_income_tax(salary)
        dividend_tax = self.calculate_dividend_tax(dividends, salary)
        ni_contributions = self.calculate_national_insurance(salary)
        
        total_tax = corporation_tax + income_tax + dividend_tax + ni_contributions
        total_income = salary + dividends
        net_income = total_income - income_tax - dividend_tax - ni_contributions
        effective_rate = (total_tax / (company_profit + total_income) * 100) if (company_profit + total_income) > 0 else 0
        
        # Recommendations
        recommendations = []
        if rd_expenditure == 0:
            recommendations.append(f"Consider R&D tax credits if your company innovates - up to {self.RD_TAX_CREDIT_DISPLAY}% deduction available")
        if capital_investment < self.ANNUAL_INVESTMENT_ALLOWANCE:
            recommendations.append(f"Annual Investment Allowance allows up to £{self.ANNUAL_INVESTMENT_ALLOWANCE:,} tax-free capital investment")
        if salary < self.NI_LOWER_LIMIT:
            recommendations.append(f"Consider salary of £{self.NI_LOWER_LIMIT:,.2f} for optimal NI benefits")
        
        return {
            'category': 'Company Owner',
            'summary': {
                'company_profit': round(company_profit, 2),
                'total_personal_income': round(total_income, 2),
                'net_income': round(net_income, 2),
                'total_tax': round(total_tax, 2),
                'effective_tax_rate': round(effective_rate, 2)
            },
            'breakdown': {
                'corporation_tax': round(corporation_tax, 2),
                'income_tax': round(income_tax, 2),
                'dividend_tax': round(dividend_tax, 2),
                'national_insurance': round(ni_contributions, 2),
                'rd_relief': round(rd_relief, 2),
                'capital_investment': round(capital_investment, 2)
            },
            'recommendations': recommendations
        }
    
    def optimize_landlord(self, data):
        """
        Optimize tax position for a landlord.
        
        Args:
            data: Dictionary with rental_income, mortgage_interest, other_expenses, 
                  is_furnished, number_of_properties
        
        Returns:
            Dictionary with tax calculations and recommendations
        """
        rental_income = data.get('rental_income', 0)
        mortgage_interest = data.get('mortgage_interest', 0)
        other_expenses = data.get('other_expenses', 0)
        is_furnished = data.get('is_furnished', False)
        num_properties = data.get('number_of_properties', 1)
        
        # Mortgage interest relief (20% tax credit, not deduction)
        mortgage_relief = mortgage_interest * 0.20
        
        # Furnished property allowance
        furnished_allowance = min(1000, rental_income * 0.10) if is_furnished else 0
        
        # Calculate taxable profit
        taxable_profit = rental_income - other_expenses - furnished_allowance
        
        # Calculate taxes
        income_tax = self.calculate_income_tax(taxable_profit)
        net_tax = max(0, income_tax - mortgage_relief)
        
        net_income = rental_income - other_expenses - mortgage_interest - net_tax
        effective_rate = (net_tax / rental_income * 100) if rental_income > 0 else 0
        
        # Recommendations
        recommendations = []
        if not is_furnished:
            recommendations.append("Consider furnished lettings for additional tax allowances")
        if num_properties > 1:
            recommendations.append("Multiple properties may benefit from incorporation for tax efficiency")
        if mortgage_interest > rental_income * 0.5:
            recommendations.append("High mortgage costs - consider refinancing or incorporating")
        recommendations.append("Track all expenses carefully - repairs, insurance, management fees are deductible")
        
        return {
            'category': 'Landlord',
            'summary': {
                'rental_income': round(rental_income, 2),
                'taxable_profit': round(taxable_profit, 2),
                'net_income': round(net_income, 2),
                'total_tax': round(net_tax, 2),
                'effective_tax_rate': round(effective_rate, 2)
            },
            'breakdown': {
                'rental_income': round(rental_income, 2),
                'mortgage_interest': round(mortgage_interest, 2),
                'mortgage_relief': round(mortgage_relief, 2),
                'other_expenses': round(other_expenses, 2),
                'furnished_allowance': round(furnished_allowance, 2),
                'income_tax': round(income_tax, 2),
                'number_of_properties': num_properties
            },
            'recommendations': recommendations
        }
