# Tax Optimization Engine

A comprehensive UK tax optimization module providing tailored tax-saving recommendations for different user types based on HMRC guidelines.

## Overview

The Tax Optimization Engine has been refactored to provide:

- **Modular Design**: Separated into reusable components (`uk_tax_calculator.py` and `tax_optimization_engine.py`)
- **Error Handling**: Comprehensive input validation and error messages for all edge cases
- **Named Constants**: Replaced all hardcoded values (e.g., `12_570`, `0.20`) with descriptive constants
- **Improved Documentation**: Enhanced comments explaining tax strategies and calculations
- **Type Safety**: Full type hints for all parameters and return values

## Features

### User Types Supported

1. **Company Directors** - Salary vs dividends optimization
2. **Sole Traders** - Expense tracking and relief optimization
3. **Company Owners** - Corporation tax and R&D relief planning
4. **Landlords** - Property allowances and incorporation analysis

### Tax Calculations

The module provides accurate calculations for:

- PAYE (Pay As You Earn) income tax
- National Insurance contributions
- Dividend tax
- Corporation tax (with marginal relief)
- Pension tax relief
- Trading and property allowances

## Installation

No external dependencies required - uses Python 3.7+ standard library only.

```bash
# The module is ready to use in the backend/ directory
cd backend/
```

## Quick Start

### Basic Usage

```python
from backend.tax_optimization_engine import TaxOptimizationEngine

# Create engine instance
engine = TaxOptimizationEngine()

# Optimize for a company director
result = engine.optimize_for_director(
    salary=30_000,
    dividends=20_000,
    company_profit=60_000,
    pension_contribution=5_000
)

print(f"Potential saving: £{result['potential_saving']:,.2f}")
print(f"Recommendations: {len(result['recommendations'])} strategies")
```

### All User Types

```python
# Sole Trader
result = engine.optimize_for_sole_trader(
    trading_income=75_000,
    allowable_expenses=15_000,
    pension_contribution=10_000,
    capital_allowances=5_000
)

# Company Owner
result = engine.optimize_for_company_owner(
    company_profit=100_000,
    salary=30_000,
    dividends=40_000,
    r_and_d_expenditure=15_000,
    capital_investment=50_000
)

# Landlord
result = engine.optimize_for_landlord(
    rental_income=36_000,
    mortgage_interest=12_000,
    other_expenses=6_000,
    is_furnished=True,
    number_of_properties=4
)

# Generic comprehensive plan
result = engine.comprehensive_tax_plan(
    user_type='director',
    salary=25_000,
    dividends=15_000,
    company_profit=50_000
)
```

## Error Handling

All methods include comprehensive validation:

```python
try:
    result = engine.optimize_for_director(
        salary=-1000,  # Invalid: negative
        dividends=20000,
        company_profit=60000
    )
except ValueError as e:
    print(f"Error: {e}")
    # Output: Invalid input for director optimization: salary cannot be negative
```

### Validation Rules

- All monetary amounts must be non-negative
- All required fields must be provided
- `number_of_properties` must be a positive integer
- `is_furnished` must be a boolean
- `user_type` must be one of: 'director', 'sole_trader', 'company_owner', 'landlord'

## Tax Constants

All tax rates and thresholds are defined in `TaxConstants` class:

```python
from backend.uk_tax_calculator import TaxConstants

print(f"Personal Allowance: £{TaxConstants.PERSONAL_ALLOWANCE:,}")
print(f"Basic Rate: {TaxConstants.BASIC_RATE * 100}%")
print(f"Corporation Tax: {TaxConstants.CORPORATION_TAX_SMALL_PROFITS_RATE * 100}%")
```

### Key Constants (2025/2026 Tax Year)

- Personal Allowance: £12,570
- Basic Rate Threshold: £50,270
- Higher Rate Threshold: £150,000
- Basic Tax Rate: 20%
- Higher Tax Rate: 40%
- Additional Tax Rate: 45%
- Corporation Tax: 19% (small profits), 25% (main rate)
- Dividend Allowance: £500
- Trading/Property Allowance: £1,000 each
- Annual Investment Allowance: £1,000,000

## Architecture

### Module Structure

```
backend/
├── uk_tax_calculator.py          # Core tax calculation engine
│   ├── TaxConstants              # All tax rates and thresholds
│   ├── UKTaxCalculator          # PAYE, NI, dividend, corporation tax
│   └── TaxReliefs               # Pension, trading, property reliefs
│
└── tax_optimization_engine.py    # Optimization strategies
    └── TaxOptimizationEngine     # User-specific optimizations
```

### Key Classes

#### `TaxConstants`
Centralizes all UK tax constants for easy maintenance and updates.

#### `UKTaxCalculator`
Provides core tax calculation methods:
- `calculate_paye(annual_income)` - Income tax and NI
- `calculate_dividend_tax(dividend_amount, other_income)` - Dividend tax
- `calculate_corporation_tax(taxable_profit)` - Corporation tax with marginal relief

#### `TaxReliefs`
Calculates tax reliefs:
- `calculate_pension_relief(contribution, income)` - Pension tax relief
- `calculate_trading_allowance(trading_income)` - Trading allowance benefit
- `calculate_property_allowance(rental_income)` - Property allowance benefit

#### `TaxOptimizationEngine`
Provides optimization strategies:
- `optimize_for_director()` - Director-specific strategies
- `optimize_for_sole_trader()` - Sole trader strategies
- `optimize_for_company_owner()` - Company owner strategies
- `optimize_for_landlord()` - Landlord strategies
- `comprehensive_tax_plan()` - Generic router to specific strategies

## Optimization Strategies

### Company Directors

1. **Optimal Salary Level**: Set at personal allowance (£12,570) to minimize NI
2. **Dividend Strategy**: Extract remaining profits as dividends (lower tax, no NI)
3. **Pension Contributions**: Use employer contributions for corporation tax relief
4. **Dividend Timing**: Split payments across tax years to maximize allowance

### Sole Traders

1. **Expense Tracking**: Claim all allowable business expenses (20-45% relief)
2. **Annual Investment Allowance**: 100% first-year relief on equipment
3. **Pension Contributions**: Personal pension for tax relief
4. **Trading Allowance**: Consider £1,000 allowance vs expenses
5. **Income Splitting**: Employ spouse/partner for additional efficiency

### Company Owners

1. **R&D Tax Relief**: Claim up to 230% deduction for qualifying activities
2. **Capital Allowances**: Utilize AIA for equipment purchases
3. **Entrepreneur's Relief**: Plan for business sale with 10% CGT
4. **Patent Box**: Apply 10% rate on patent income
5. **Employer Pension**: Corporation tax deductible contributions

### Landlords

1. **Property Allowance**: Consider £1,000 allowance vs expenses
2. **Mortgage Interest Relief**: Use 20% tax reducer (post-2017 rules)
3. **Furnished Property Relief**: Claim replacement relief
4. **Capital Allowances**: Claim on qualifying fixtures
5. **Incorporation**: Consider for 3+ properties with savings > £1,000
6. **Joint Ownership**: Income splitting with spouse/partner

## Examples

See `example_tax_optimization.py` for comprehensive usage examples.

Run the example:

```bash
python3 example_tax_optimization.py
```

## Return Values

All optimization methods return a dictionary with:

```python
{
    'user_type': str,              # Type of user
    'current_position': dict,      # Current tax situation
    'optimal_position': dict,      # Recommended structure (where applicable)
    'potential_saving': float,     # Tax savings available
    'recommendations': list,       # List of strategies
    'detailed_calculations': dict  # Full calculation breakdown
}
```

## Testing

Manual testing is included in the codebase:

```bash
# Test all optimization methods
python3 -c "from backend.tax_optimization_engine import TaxOptimizationEngine; \
            engine = TaxOptimizationEngine(); \
            result = engine.optimize_for_director(30000, 20000, 60000); \
            print(f'Saving: £{result[\"potential_saving\"]:.2f}')"
```

## Refactoring Improvements

This refactored version addresses the following issues from the original code:

### 1. Modularization ✓
- Separated into `uk_tax_calculator.py` (core calculations) and `tax_optimization_engine.py` (strategies)
- Reusable calculator and reliefs classes
- Helper methods for common operations

### 2. Error Handling ✓
- Input validation in all methods
- Comprehensive error messages
- Type checking for all parameters
- Missing field detection

### 3. Optimization and Clarity ✓
- Named constants replace all hardcoded values
- Detailed docstrings with strategy explanations
- Inline comments for complex calculations
- Consistent code style and structure

## Tax Year

This module is configured for the **2025/2026 UK tax year**. To update for future tax years, modify the constants in `TaxConstants` class.

## Disclaimer

This tool provides illustrative tax calculations and optimization strategies. It should not be used as a substitute for professional tax advice. Always consult with a qualified tax professional or accountant for specific tax planning decisions.

## License

Part of the Tax-calculator- repository.
