# UK Tax-Saving Calculator

A comprehensive HMRC-compliant tax calculator and optimization tool for UK taxpayers, covering PAYE, Capital Gains Tax, Corporation Tax, VAT, and various tax reliefs.

**Tax Year: 2024/2025**

## 🌟 Features

### Tax Calculations
- ✅ **PAYE (Pay As You Earn)** - Income tax and National Insurance
- ✅ **Capital Gains Tax (CGT)** - For shares and property
- ✅ **Corporation Tax** - With marginal relief calculations
- ✅ **Dividend Tax** - Including dividend allowance
- ✅ **Value Added Tax (VAT)** - Registration and liability
- ✅ **Tax Reliefs** - Pension, trading allowance, property allowance

### User-Specific Optimizations
- 👔 **Company Directors** - Salary vs dividend optimization
- 💼 **Sole Traders** - Expense maximization and allowances
- 🏢 **Company Owners** - R&D relief and capital allowances
- 🏠 **Landlords** - Property income and incorporation strategies

### Key Capabilities
- 💡 Personalized tax-saving recommendations
- 📊 Current vs optimized tax position comparison
- 💰 Potential savings calculations
- 📈 Interactive web interface
- 🐍 Python backend for automation
- 📚 Comprehensive HMRC guidelines reference

## 🚀 Quick Start

### Web Interface (Easiest)

1. Open `uk_tax_calculator.html` in your web browser
2. Select your user type (Director, Sole Trader, Company Owner, or Landlord)
3. Enter your financial information
4. Click "Calculate & Optimize"
5. Review your tax position and recommendations

### Python Backend

```python
from backend.uk_tax_calculator import UKTaxCalculator
from backend.tax_optimization import TaxOptimizationEngine

# Basic tax calculation
calculator = UKTaxCalculator()
paye = calculator.calculate_paye(50000)
print(f"Tax: £{paye['income_tax']:,.2f}")
print(f"NI: £{paye['employee_ni']:,.2f}")
print(f"Net: £{paye['net_salary']:,.2f}")

# Get optimization recommendations
optimizer = TaxOptimizationEngine()
results = optimizer.optimize_for_director(
    salary=50000,
    dividends=30000,
    company_profit=100000
)
print(f"Potential Saving: £{results['potential_saving']:,.2f}")
```

### Run Sample Scenarios

```bash
python sample_scenarios.py
```

This demonstrates 7 realistic scenarios showing tax calculations and optimization strategies.

## 📁 Project Structure

```
Tax-calculator-/
├── backend/
│   ├── uk_tax_calculator.py      # Core tax calculations
│   ├── tax_optimization.py       # Optimization strategies
│   ├── utils.py                  # Utility functions
│   ├── reconciliation.py         # Account reconciliation
│   ├── accruals.py              # Accrual calculations
│   └── financial_statements.py   # Statement generation
├── frontend/
│   └── dashboard.html           # Month-end close dashboard
├── uk_tax_calculator.html       # Tax calculator interface
├── sample_scenarios.py          # Demonstration scenarios
├── UK_TAX_GUIDELINES.md        # Comprehensive tax guide
├── README_MONTH_END_CLOSE.md   # Month-end close docs
└── index.html                   # Payroll calculator
```

## 💡 Example Scenarios

### Scenario 1: Company Director Optimization

**Before:**
- Salary: £50,000
- Dividends: £30,000
- Total Tax: £43,119

**After Optimization:**
- Salary: £12,570 (personal allowance)
- Dividends: £68,011
- Total Tax: £32,779

**Saving: £10,340 per year** 💰

### Scenario 2: Sole Trader with Expenses

**Before:**
- Income: £60,000
- Expenses: £12,000
- Tax: £8,486

**After Optimization:**
- Enhanced expenses: £15,000
- Pension: £5,000
- Tax: £4,486

**Saving: £4,000 per year** 💰

### Scenario 3: Company Owner with R&D

**Before:**
- Profit: £200,000
- Corporation Tax: £49,250

**After R&D Claim:**
- R&D Expenditure: £50,000
- Enhanced Relief: £15,000
- Corporation Tax: £32,250

**Saving: £17,000 per year** 💰

## 📊 Tax Rates & Thresholds (2024/2025)

### Income Tax
- Personal Allowance: £12,570
- Basic Rate (20%): £12,571 - £50,270
- Higher Rate (40%): £50,271 - £125,140
- Additional Rate (45%): Over £125,140

### National Insurance
- Employee (8%): £12,571 - £50,270
- Employee (2%): Over £50,270
- Employer (13.8%): Over £9,100

### Corporation Tax
- Small Profits (19%): Up to £50,000
- Main Rate (25%): Over £250,000
- Marginal Relief: Between thresholds

### Capital Gains Tax
- Annual Exemption: £3,000
- Basic Rate: 10% (assets) / 18% (property)
- Higher Rate: 20% (assets) / 28% (property)

### VAT
- Registration Threshold: £90,000
- Standard Rate: 20%

## 🎯 Tax-Saving Strategies

### For Company Directors
1. **Optimal Salary Level** - Set at £12,570 to minimize NI
2. **Dividend Strategy** - Extract profits as dividends (lower tax, no NI)
3. **Pension Contributions** - Employer contributions (corporation tax deductible)
4. **Dividend Timing** - Split across tax years to maximize allowance

### For Sole Traders
1. **Maximize Expenses** - Claim all allowable business expenses
2. **Annual Investment Allowance** - 100% first-year relief on equipment
3. **Pension Contributions** - Tax relief at marginal rate
4. **Trading Allowance** - £1,000 simplified option for small income

### For Company Owners
1. **R&D Tax Relief** - 230% deduction for qualifying activities
2. **Capital Allowances** - Up to £1,000,000 Annual Investment Allowance
3. **Patent Box** - 10% corporation tax on patent income
4. **Business Asset Disposal Relief** - 10% CGT on business sale

### For Landlords
1. **Property Allowance** - £1,000 tax-free for small rental income
2. **Mortgage Interest Relief** - 20% tax credit
3. **Replacement Relief** - Full cost for furnished property items
4. **Incorporation** - Consider for 3+ properties if beneficial

## 📚 Documentation

- **[UK_TAX_GUIDELINES.md](UK_TAX_GUIDELINES.md)** - Comprehensive HMRC guidelines, detailed calculations, and examples
- **[README_MONTH_END_CLOSE.md](README_MONTH_END_CLOSE.md)** - Month-end close process documentation
- **sample_scenarios.py** - 7 realistic scenarios with code

## 🔧 Technical Details

### Backend Modules

#### `uk_tax_calculator.py`
Core tax calculation engine with HMRC-compliant calculations:
- `UKTaxCalculator` - Main calculator class
- `TaxReliefs` - Relief and allowance calculations

#### `tax_optimization.py`
User-specific optimization strategies:
- `TaxOptimizationEngine` - Optimization recommendations
- Methods for each user type (directors, sole traders, etc.)

### Frontend

#### `uk_tax_calculator.html`
Interactive web interface featuring:
- User type selection
- Dynamic input forms
- Real-time calculations
- Visual results display
- Personalized recommendations

## 🧮 Calculations Supported

### PAYE Calculation
```python
calculator = UKTaxCalculator()
result = calculator.calculate_paye(
    annual_salary=50000,
    include_ni=True,
    ni_category='A'
)
# Returns: income_tax, employee_ni, employer_ni, net_salary, etc.
```

### Capital Gains Tax
```python
result = calculator.calculate_cgt(
    capital_gains=50000,
    annual_income=40000,
    is_property=False
)
# Returns: cgt_due, effective_rate, taxable_gains, etc.
```

### Corporation Tax
```python
result = calculator.calculate_corporation_tax(
    profit=200000,
    associated_companies=0
)
# Returns: corporation_tax, effective_rate, band, profit_after_tax
```

### Dividend Tax
```python
result = calculator.calculate_dividend_tax(
    dividends=30000,
    other_income=20000
)
# Returns: dividend_tax, effective_rate, taxable_dividends
```

### VAT
```python
result = calculator.calculate_vat(
    turnover=95000,
    expenses=30000,
    scheme='standard'
)
# Returns: vat_due, output_vat, input_vat, etc.
```

## 🎓 Learning Resources

### HMRC Official Resources
- Income Tax: www.gov.uk/income-tax-rates
- National Insurance: www.gov.uk/national-insurance-rates
- Corporation Tax: www.gov.uk/corporation-tax-rates
- Capital Gains Tax: www.gov.uk/capital-gains-tax
- VAT: www.gov.uk/vat-rates
- Self Assessment: www.gov.uk/self-assessment-tax-returns

### Key Deadlines
- Self Assessment Registration: 5 October
- Online Tax Return: 31 January
- Payment Deadline: 31 January
- Payment on Account: 31 January & 31 July

## ⚠️ Important Disclaimer

This calculator provides illustrative tax calculations and optimization strategies based on HMRC guidelines for the 2024/2025 tax year. The results are for **informational purposes only** and should not be considered as financial or tax advice.

**Key Points:**
- Tax situations can be complex and individual circumstances vary
- Always consult with a qualified tax advisor or accountant
- Verify current rates and thresholds with HMRC
- Tax legislation may change
- Professional advice recommended before implementing strategies

## 🤝 Use Cases

### Individual Users
- Calculate personal tax liability
- Plan tax-efficient income extraction
- Understand potential savings
- Compare different strategies

### Accountants & Tax Advisors
- Quick calculations for clients
- Scenario modeling
- Strategy comparison
- Client presentations

### Business Owners
- Tax planning and optimization
- Structure decisions (salary vs dividends)
- R&D relief assessment
- Incorporation analysis

### Students & Educators
- Learn UK tax system
- Understand tax calculations
- Explore optimization strategies
- Real-world examples

## 🔍 Example Outputs

### Tax Calculation Output
```json
{
  "gross_salary": 50000,
  "personal_allowance": 12570,
  "taxable_income": 37430,
  "income_tax": 7486.00,
  "employee_ni": 2994.40,
  "net_salary": 39519.60,
  "effective_tax_rate": 20.96,
  "monthly_net": 3293.30
}
```

### Optimization Recommendations
```json
{
  "user_type": "Company Director",
  "potential_saving": 10340.22,
  "recommendations": [
    {
      "strategy": "Optimal Salary Level",
      "description": "Set salary at £12,570 (personal allowance)",
      "saving": 2994.40
    },
    {
      "strategy": "Dividend Strategy",
      "description": "Extract profits as dividends",
      "saving": "Lower tax rate than salary"
    }
  ]
}
```

## 🛠️ Requirements

- **Python**: 3.7 or higher (for backend)
- **Web Browser**: Modern browser (Chrome, Firefox, Safari, Edge)
- **No external dependencies**: Uses Python standard library only

## 🚦 Getting Started Checklist

- [ ] Open `uk_tax_calculator.html` in browser
- [ ] Select your user type
- [ ] Enter your financial information
- [ ] Review calculations and recommendations
- [ ] Run `python sample_scenarios.py` for examples
- [ ] Read `UK_TAX_GUIDELINES.md` for detailed information
- [ ] Consult with a tax advisor for personalized advice

## 📈 Future Enhancements

Potential improvements:
- Real-time HMRC rate updates
- Multi-year tax planning
- PDF report generation
- Database integration
- REST API
- Mobile app
- Historical tax year comparisons
- International tax considerations

## 📝 Version History

**v1.0** - Initial Release (Tax Year 2024/2025)
- Complete PAYE, CGT, Corporation Tax, VAT calculations
- User-specific optimization strategies
- Interactive web interface
- Comprehensive documentation
- 7 sample scenarios

## 📧 Support

For questions about UK tax regulations, consult:
- HMRC website: www.gov.uk/government/organisations/hm-revenue-customs
- HMRC helpline: 0300 200 3300
- Qualified tax advisor or accountant

## 📄 License

This is a demonstration project for educational purposes. Check with the repository owner for licensing information.

---

**Made with ❤️ for UK taxpayers seeking to optimize their tax position legally and efficiently.**

*Remember: Tax avoidance (legal) is different from tax evasion (illegal). This tool helps with legal tax optimization strategies.*
