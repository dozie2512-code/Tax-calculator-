# UK Tax Calculator

A comprehensive UK tax calculation system supporting PAYE (Pay As You Earn), Self Assessment, and Corporation Tax computations. This calculator uses current UK tax rates and thresholds for the 2024/25 tax year.

## 📋 Features

### 1. **PAYE (Pay As You Earn)**
Calculate income tax for UK employees with:
- **Personal Allowance**: £12,570 (tapered for high earners)
- **Basic Rate (20%)**: £12,571 to £50,270
- **Higher Rate (40%)**: £50,271 to £150,000
- **Additional Rate (45%)**: Over £150,000
- Support for tax-free allowances and deductions (pension contributions, etc.)

### 2. **Self Assessment**
Calculate tax for self-employed individuals and multiple income sources:
- Multiple income types (employment, self-employment, property, investment)
- Allowable deductions (pension contributions, charitable donations)
- Trading losses
- Comprehensive breakdown of income sources and deductions

### 3. **Corporate Tax**
Calculate UK Corporation Tax for businesses:
- **Small Profits Rate (19%)**: Up to £50,000
- **Main Rate (25%)**: Over £250,000
- **Marginal Relief**: For profits between £50,000 and £250,000
- Allowable business expense deductions
- **R&D Tax Credits**:
  - SMEs: 86% enhancement
  - Large companies: 13% credit
- **Loss Carry-Forward**: Apply previous year losses

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Tax-calculator-
```

2. No external dependencies required - uses Python standard library only!

### Basic Usage

```python
from backend.uk_tax_calculator import calculate_paye, calculate_self_assessment, calculate_corporate_tax

# Calculate PAYE for an employee
paye_result = calculate_paye(gross_income=45000, deductions=3000)
print(f"Total Tax: £{paye_result['total_tax']:,.2f}")

# Calculate Self Assessment with multiple income sources
income_sources = [
    {'type': 'employment', 'amount': 35000},
    {'type': 'self_employment', 'amount': 20000},
    {'type': 'property', 'amount': 12000}
]
deductions = {'pension': 4000, 'charity': 500}
sa_result = calculate_self_assessment(income_sources, deductions)

# Calculate Corporation Tax
corp_result = calculate_corporate_tax(
    gross_profit=300000,
    allowable_expenses=80000,
    rd_expenditure=25000,
    losses_brought_forward=10000
)
```

## 📖 Detailed Usage

### PAYE Calculator

```python
from backend.uk_tax_calculator import PAYECalculator

calculator = PAYECalculator()
result = calculator.calculate(
    gross_income=45000,  # Annual gross income in GBP
    deductions=3000      # Pension contributions, etc.
)

# Result includes:
print(result['gross_income'])          # Original gross income
print(result['personal_allowance'])    # Personal allowance applied
print(result['taxable_income'])        # Income after allowances
print(result['tax_breakdown'])         # Tax by band (basic, higher, additional)
print(result['total_tax'])             # Total PAYE tax
print(result['net_income'])            # Income after tax
```

#### PAYE Examples

**Example 1: Basic Rate Taxpayer**
```python
result = calculate_paye(gross_income=30000)
# Expected: Tax ≈ £3,486 (20% on £17,430)
```

**Example 2: Higher Rate Taxpayer**
```python
result = calculate_paye(gross_income=75000)
# Tax breakdown:
# - Basic rate: 20% on £37,700 = £7,540
# - Higher rate: 40% on £24,730 = £9,892
# Total tax: £17,432
```

**Example 3: With Pension Deductions**
```python
result = calculate_paye(gross_income=55000, deductions=5000)
# Deductions reduce taxable income before personal allowance
```

**Example 4: High Earner (Tapered Allowance)**
```python
result = calculate_paye(gross_income=125000)
# Personal allowance reduced by £1 for every £2 over £100,000
# Personal allowance: £12,570 - £12,500 = £70
```

### Self Assessment Calculator

```python
from backend.uk_tax_calculator import SelfAssessmentCalculator

calculator = SelfAssessmentCalculator()
result = calculator.calculate(
    income_sources=[
        {'type': 'employment', 'amount': 35000},
        {'type': 'self_employment', 'amount': 20000},
        {'type': 'property', 'amount': 12000},
        {'type': 'investment', 'amount': 5000}
    ],
    deductions={
        'pension': 4000,          # Pension contributions
        'charity': 500,           # Charitable donations
        'trading_losses': 2000,   # Trading losses
        'other': 1000             # Other allowable deductions
    }
)

# Result includes:
print(result['total_income'])              # Sum of all income
print(result['income_breakdown'])          # Breakdown by type
print(result['total_deductions'])          # Sum of all deductions
print(result['deductions_breakdown'])      # Breakdown by type
print(result['taxable_income'])            # Final taxable income
print(result['total_tax'])                 # Total tax liability
print(result['net_income'])                # Income after tax
```

#### Self Assessment Examples

**Example 1: Employed + Rental Income**
```python
income_sources = [
    {'type': 'employment', 'amount': 40000},
    {'type': 'property', 'amount': 15000}
]
deductions = {'pension': 3000}
result = calculate_self_assessment(income_sources, deductions)
# Total income: £55,000
# After deductions: £52,000
# Tax calculated on combined income
```

**Example 2: Multiple Self-Employment Ventures**
```python
income_sources = [
    {'type': 'self_employment', 'amount': 30000},
    {'type': 'self_employment', 'amount': 25000}
]
deductions = {
    'pension': 5000,
    'charity': 1000,
    'trading_losses': 3000
}
result = calculate_self_assessment(income_sources, deductions)
```

**Example 3: Portfolio Income**
```python
income_sources = [
    {'type': 'employment', 'amount': 50000},
    {'type': 'property', 'amount': 20000},
    {'type': 'investment', 'amount': 10000}
]
result = calculate_self_assessment(income_sources)
# Demonstrates multiple passive income streams
```

### Corporate Tax Calculator

```python
from backend.uk_tax_calculator import CorporateTaxCalculator

calculator = CorporateTaxCalculator()
result = calculator.calculate(
    gross_profit=300000,              # Company's gross profit
    allowable_expenses=80000,         # Deductible expenses
    rd_expenditure=25000,             # R&D spending
    losses_brought_forward=10000,     # Previous year losses
    is_sme=True                       # SME status for R&D credits
)

# Result includes:
print(result['gross_profit'])              # Original gross profit
print(result['allowable_expenses'])        # Applied expenses
print(result['adjusted_profit'])           # Profit after expenses
print(result['rd_tax_credit'])             # R&D tax credit amount
print(result['taxable_profit'])            # Final taxable profit
print(result['applicable_rate'])           # Tax rate applied
print(result['marginal_relief'])           # Marginal relief (if applicable)
print(result['corporation_tax'])           # Total corporation tax
print(result['effective_rate'])            # Effective tax rate %
print(result['net_profit'])                # Profit after tax
```

#### Corporation Tax Examples

**Example 1: Small Company (19% rate)**
```python
result = calculate_corporate_tax(
    gross_profit=80000,
    allowable_expenses=35000
)
# Taxable profit: £45,000 (below £50,000 threshold)
# Rate: 19%
# Corporation tax: £8,550
```

**Example 2: Large Company (25% rate)**
```python
result = calculate_corporate_tax(
    gross_profit=500000,
    allowable_expenses=150000
)
# Taxable profit: £350,000 (above £250,000 threshold)
# Rate: 25%
# Corporation tax: £87,500
```

**Example 3: Marginal Relief Band**
```python
result = calculate_corporate_tax(
    gross_profit=200000,
    allowable_expenses=50000
)
# Taxable profit: £150,000 (between £50k and £250k)
# Main rate applied with marginal relief
# Effective rate: lower than 25%
```

**Example 4: With R&D Credits (SME)**
```python
result = calculate_corporate_tax(
    gross_profit=400000,
    allowable_expenses=100000,
    rd_expenditure=50000,
    is_sme=True
)
# R&D credit: £43,000 (86% of £50,000)
# Significantly reduces taxable profit
```

**Example 5: With Loss Carry-Forward**
```python
result = calculate_corporate_tax(
    gross_profit=150000,
    allowable_expenses=30000,
    losses_brought_forward=40000
)
# Adjusted profit: £120,000
# After losses: £80,000
# Tax calculated on reduced profit
```

**Example 6: Large Company R&D**
```python
result = calculate_corporate_tax(
    gross_profit=1000000,
    allowable_expenses=300000,
    rd_expenditure=100000,
    is_sme=False  # Large company
)
# R&D credit: £13,000 (13% of £100,000)
# Different credit rate for non-SMEs
```

## 🔍 Input Validation

All calculators include comprehensive input validation with clear error messages:

```python
from backend.uk_tax_calculator import ValidationError

try:
    result = calculate_paye(gross_income=-5000)  # Invalid: negative income
except ValidationError as e:
    print(f"Error: {e}")  # "Gross income cannot be negative"

try:
    result = calculate_paye(gross_income=50000, deductions=60000)  # Invalid
except ValidationError as e:
    print(f"Error: {e}")  # "Deductions cannot exceed gross income"
```

### Common Validation Rules

**PAYE:**
- Gross income must be non-negative
- Deductions must be non-negative
- Deductions cannot exceed gross income

**Self Assessment:**
- At least one income source required
- Each income source must have 'type' and 'amount'
- All amounts must be non-negative
- Valid deduction types: pension, charity, trading_losses, other

**Corporation Tax:**
- All monetary values must be non-negative
- Gross profit, expenses, R&D, and losses must be >= 0

## 🧪 Testing

Run the included examples:

```bash
python backend/uk_tax_calculator.py
```

This will output example calculations for all three tax types.

### Manual Testing

```python
# Test PAYE with various income levels
for income in [20000, 40000, 60000, 100000, 200000]:
    result = calculate_paye(income)
    print(f"Income: £{income:,} -> Tax: £{result['total_tax']:,.2f}")

# Test Self Assessment validation
try:
    calculate_self_assessment([])  # Should raise error
except ValidationError as e:
    print(f"Caught expected error: {e}")

# Test Corporation Tax marginal relief
for profit in [40000, 100000, 150000, 200000, 300000]:
    result = calculate_corporate_tax(gross_profit=profit)
    print(f"Profit: £{profit:,} -> Rate: {result['effective_rate']:.2f}%")
```

## 📊 Tax Year 2024/25 Rates Reference

### Income Tax (PAYE & Self Assessment)
| Band | Income Range | Rate |
|------|--------------|------|
| Personal Allowance | £0 - £12,570 | 0% |
| Basic Rate | £12,571 - £50,270 | 20% |
| Higher Rate | £50,271 - £150,000 | 40% |
| Additional Rate | Over £150,000 | 45% |

**Note:** Personal allowance reduces by £1 for every £2 earned over £100,000

### Corporation Tax
| Profit Range | Rate | Notes |
|--------------|------|-------|
| £0 - £50,000 | 19% | Small Profits Rate |
| £50,001 - £250,000 | 19% - 25% | Marginal Relief applies |
| Over £250,000 | 25% | Main Rate |

### R&D Tax Credits
| Company Type | Credit Rate | Notes |
|--------------|-------------|-------|
| SME | 86% | 86% enhancement on qualifying expenditure |
| Large Company | 13% | 13% credit on qualifying expenditure |

## 🛠️ Advanced Usage

### Class-Based Approach

```python
from backend.uk_tax_calculator import (
    PAYECalculator, 
    SelfAssessmentCalculator, 
    CorporateTaxCalculator
)

# Create calculator instances for reuse
paye_calc = PAYECalculator()
sa_calc = SelfAssessmentCalculator()
corp_calc = CorporateTaxCalculator()

# Calculate for multiple employees
employees = [
    {'name': 'John', 'income': 45000, 'pension': 3000},
    {'name': 'Jane', 'income': 65000, 'pension': 5000},
    {'name': 'Bob', 'income': 120000, 'pension': 10000}
]

for emp in employees:
    result = paye_calc.calculate(emp['income'], emp['pension'])
    print(f"{emp['name']}: Tax = £{result['total_tax']:,.2f}")
```

### Batch Processing

```python
def process_employee_taxes(employee_data):
    """Process taxes for multiple employees"""
    calculator = PAYECalculator()
    results = []
    
    for emp in employee_data:
        try:
            result = calculator.calculate(
                emp['gross_income'],
                emp.get('deductions', 0)
            )
            results.append({
                'employee_id': emp['id'],
                'gross': result['gross_income'],
                'tax': result['total_tax'],
                'net': result['net_income']
            })
        except ValidationError as e:
            results.append({
                'employee_id': emp['id'],
                'error': str(e)
            })
    
    return results
```

### Custom Reporting

```python
def generate_tax_report(income, deductions=0):
    """Generate a formatted tax report"""
    result = calculate_paye(income, deductions)
    
    report = f"""
    TAX CALCULATION REPORT
    =====================
    
    Gross Income:        £{result['gross_income']:>12,.2f}
    Deductions:          £{result['deductions']:>12,.2f}
    Personal Allowance:  £{result['personal_allowance']:>12,.2f}
    Taxable Income:      £{result['taxable_income']:>12,.2f}
    
    TAX BREAKDOWN
    -------------
    Basic Rate (20%):    £{result['tax_breakdown']['basic_rate']:>12,.2f}
    Higher Rate (40%):   £{result['tax_breakdown']['higher_rate']:>12,.2f}
    Additional (45%):    £{result['tax_breakdown']['additional_rate']:>12,.2f}
    
    TOTAL TAX:           £{result['total_tax']:>12,.2f}
    NET INCOME:          £{result['net_income']:>12,.2f}
    
    Effective Rate:      {(result['total_tax']/result['gross_income']*100):>11.2f}%
    """
    return report

print(generate_tax_report(75000, 5000))
```

## 📁 Project Structure

```
Tax-calculator-/
├── backend/
│   ├── uk_tax_calculator.py      # UK tax calculation module (NEW)
│   ├── utils.py                  # Utility functions (existing)
│   ├── reconciliation.py         # Account reconciliation (existing)
│   ├── accruals.py              # Accrual calculations (existing)
│   └── financial_statements.py   # Financial statements (existing)
├── frontend/
│   └── dashboard.html           # Month-end close dashboard
├── sample_data/                 # Sample data files
├── output/                      # Generated output files
├── examples_uk_tax.py           # UK tax calculator examples (NEW)
├── README.md                    # UK tax calculator documentation (NEW)
├── README_MONTH_END_CLOSE.md   # Month-end close documentation
├── index.html                   # Month-end close prototype
└── run_month_end_close.py      # Month-end close orchestrator
```

**Note:** This repository contains both UK tax calculation functionality (new) and month-end close accounting processes (existing).

## 🔒 Important Notes

### Accuracy & Compliance
- This calculator uses 2024/25 UK tax rates and thresholds
- Calculations are for **estimation purposes** only
- Not a substitute for professional tax advice
- Always verify with HMRC or a qualified accountant for official submissions
- Tax laws change - ensure you're using current rates

### Limitations
- Does not include National Insurance contributions (NICs)
- Does not cover Scotland's different income tax rates
- Does not include Marriage Allowance transfers
- Does not cover Dividend Tax rates separately
- Simplified R&D credit calculations (actual claims are more complex)
- Does not include all possible deductions and reliefs

### Data Privacy
- All calculations are performed locally
- No data is sent to external services
- Suitable for processing sensitive financial information

## 🚀 Future Enhancements

Potential additions for production use:

1. **National Insurance Calculations**
   - Employee NI contributions
   - Employer NI contributions
   - Different NI categories

2. **Scottish Tax Rates**
   - Different rate bands for Scottish taxpayers
   - Separate calculation logic

3. **Dividend Tax**
   - Dividend allowance (£500)
   - Dividend tax rates by band

4. **Capital Gains Tax**
   - Annual exempt amount
   - CGT rates for assets

5. **VAT Calculations**
   - Standard rate (20%)
   - Reduced rates
   - VAT return preparation

6. **Advanced R&D Claims**
   - Detailed qualifying expenditure tracking
   - RDEC scheme for large companies
   - Payable tax credits

7. **Multi-Year Projections**
   - Tax planning scenarios
   - Pension contribution optimization
   - Income timing strategies

8. **Integration Features**
   - Import from accounting software
   - Export to HMRC-compatible formats
   - PDF report generation

9. **API Development**
   - REST API for tax calculations
   - Webhook support for real-time calculations
   - Authentication and rate limiting

## 🤝 Contributing

This is an open project. To contribute:

1. Follow existing code structure and style
2. Add comprehensive docstrings
3. Include usage examples
4. Ensure validation for all inputs
5. Update README with new features
6. Test thoroughly with various scenarios

## 📄 License

This project is provided as-is for educational and estimation purposes. Check with the repository owner for licensing information.

## 📞 Support

For questions or issues:
1. Review the code documentation and examples
2. Test with the provided example calculations
3. Ensure Python 3.7+ is installed
4. Check input validation error messages
5. Verify you're using correct input formats

## 🎯 Summary

This UK Tax Calculator provides:

✅ **PAYE calculations** with personal allowance and tax bands  
✅ **Self Assessment** support for multiple income sources  
✅ **Corporation Tax** with R&D credits and loss carry-forward  
✅ **Comprehensive validation** with clear error messages  
✅ **Well-documented code** with type hints and docstrings  
✅ **Easy-to-use API** with convenience functions  
✅ **Production-ready** structure and error handling  
✅ **No external dependencies** - pure Python  

Perfect for tax estimation, financial planning, and as a foundation for building comprehensive tax software!

---

**Disclaimer:** This calculator is for estimation purposes only. For official tax submissions and advice, please consult with HMRC or a qualified tax professional. Tax rates and thresholds are subject to change.
