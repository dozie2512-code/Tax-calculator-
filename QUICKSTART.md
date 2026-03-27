# Quick Start Guide - UK Tax Calculator

## 🚀 Get Started in 3 Minutes

### Option 1: Web Interface (Recommended for Most Users)

1. **Open the Calculator**
   - Double-click `uk_tax_calculator.html` 
   - Or open it in your web browser (Chrome, Firefox, Safari, Edge)

2. **Select Your Profile**
   - Click on your user type:
     - 👔 Company Director
     - 💼 Sole Trader
     - 🏢 Company Owner
     - 🏠 Landlord

3. **Enter Your Information**
   - Fill in the form fields with your financial data
   - All amounts should be in GBP (£)
   - Annual figures (not monthly)

4. **Calculate & Optimize**
   - Click the "Calculate & Optimize" button
   - Review your current tax position
   - See your potential savings
   - Read personalized recommendations

### Option 2: Run Sample Scenarios (See Examples)

```bash
python sample_scenarios.py
```

This shows 7 realistic scenarios with detailed calculations:
- Company Director Optimization
- Sole Trader with Expenses
- Company Owner with R&D
- Landlord with Multiple Properties
- High Earner Advanced Planning
- Capital Gains Tax Planning
- VAT Planning

### Option 3: Generate Professional Reports

```bash
python generate_tax_report.py
```

This creates detailed text reports:
- `director_tax_report.txt`
- `sole_trader_tax_report.txt`

Reports include:
- Executive summary
- Current tax position
- Optimized position
- Detailed breakdowns
- Savings calculations
- Recommendations

### Option 4: Use Python API (For Developers)

```python
from backend.uk_tax_calculator import UKTaxCalculator
from backend.tax_optimization import TaxOptimizationEngine

# Initialize
calculator = UKTaxCalculator()
optimizer = TaxOptimizationEngine()

# Calculate PAYE
result = calculator.calculate_paye(50000)
print(f"Net Salary: £{result['net_salary']:,.2f}")

# Get optimization advice
advice = optimizer.optimize_for_director(
    salary=50000,
    dividends=30000,
    company_profit=100000
)
print(f"Potential Saving: £{advice['potential_saving']:,.2f}")
```

## 📋 What You Need to Know

### For Company Directors
Enter:
- Your current salary
- Current dividends
- Company's profit
- Any pension contributions

Get:
- Optimal salary/dividend split
- Potential tax savings
- Pension contribution advice
- Dividend timing strategies

### For Sole Traders
Enter:
- Trading income
- Business expenses
- Capital allowances
- Pension contributions

Get:
- Tax liability calculation
- Expense optimization tips
- Allowance comparisons
- Pension relief details

### For Company Owners
Enter:
- Company profit
- Director salary
- Dividends paid
- R&D expenditure
- Capital investments

Get:
- Corporation tax calculation
- R&D relief estimates
- Capital allowance benefits
- Profit extraction strategies

### For Landlords
Enter:
- Rental income
- Mortgage interest
- Other expenses
- Property type (furnished/unfurnished)
- Number of properties

Get:
- Property income tax calculation
- Mortgage relief details
- Incorporation analysis
- Expense optimization

## 💡 Pro Tips

1. **Accurate Data** - Use actual figures for accurate results
2. **Annual Amounts** - All inputs should be yearly totals
3. **Professional Advice** - Always verify with a tax advisor
4. **Save Reports** - Keep reports for your records
5. **Plan Ahead** - Use before tax year end for planning

## 📊 Example Results

### Company Director Example
**Input:**
- Salary: £50,000
- Dividends: £30,000
- Profit: £100,000

**Output:**
- Current Tax: £43,119
- Optimized Tax: £32,779
- **Saving: £10,340/year** 💰

### Sole Trader Example
**Input:**
- Income: £60,000
- Expenses: £12,000
- Capital Allowances: £8,000

**Output:**
- Taxable Profit: £40,000
- Tax Liability: £8,486
- Recommendations for further savings

## ❓ Common Questions

**Q: Is this calculator accurate?**
A: Yes, it uses official HMRC rates for 2024/2025. However, always verify with a tax professional.

**Q: Can I use this for my tax return?**
A: This is a planning tool. For tax returns, consult an accountant or use HMRC-approved software.

**Q: What if my situation is complex?**
A: The calculator handles most common scenarios. For complex cases, seek professional advice.

**Q: Is my data secure?**
A: Yes! The web calculator runs entirely in your browser. No data is sent anywhere.

**Q: Can I save my calculations?**
A: Use the Python report generator to save detailed reports to files.

## 🆘 Need Help?

1. **Read the Documentation**
   - See `README.md` for full documentation
   - See `UK_TAX_GUIDELINES.md` for HMRC details

2. **Try Sample Scenarios**
   - Run `python sample_scenarios.py`
   - See realistic examples

3. **Consult HMRC**
   - Visit: www.gov.uk/government/organisations/hm-revenue-customs
   - Call: 0300 200 3300

4. **Get Professional Advice**
   - Speak to a qualified accountant
   - Consult a Chartered Tax Adviser (CTA)

## ⚠️ Remember

- This is a planning and educational tool
- Not a substitute for professional advice
- Tax rules can change
- Individual circumstances vary
- Always verify with HMRC or an accountant

## 🎯 Next Steps

1. ✅ Run the web calculator with your data
2. ✅ Review the recommendations
3. ✅ Read relevant sections in UK_TAX_GUIDELINES.md
4. ✅ Generate a report for your records
5. ✅ Discuss with your accountant/tax advisor
6. ✅ Implement the strategies
7. ✅ Monitor and review annually

---

**Ready to optimize your tax?** Open `uk_tax_calculator.html` now! 🚀
