# Tax Optimization Calculator - Usage Guide

## Overview

This application provides comprehensive tax optimization recommendations for four types of UK taxpayers:
- **Company Directors**: Optimize salary vs dividends
- **Sole Traders**: Maximize expense claims and reliefs
- **Company Owners**: Corporation tax and R&D planning
- **Landlords**: Property income optimization

## Quick Start

### 1. Start the Backend API

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Flask API
python backend/api.py
```

The API will start on `http://localhost:5000`

### 2. Open the Frontend

Open `frontend/tax_optimizer.html` in your web browser:

```bash
# macOS
open frontend/tax_optimizer.html

# Linux
xdg-open frontend/tax_optimizer.html

# Windows
start frontend/tax_optimizer.html
```

Or use the convenience script:

```bash
# On Unix/Linux/macOS
./start.sh
```

## Using the Calculator

### Step 1: Select Your User Type

Click on one of the four user type cards:
- 👔 Company Director
- 🛠️ Sole Trader
- 🏢 Company Owner
- 🏠 Landlord

### Step 2: Enter Your Details

Fill in the required fields for your user type:

#### For Company Directors:
- Annual Salary (required)
- Dividends (required)
- Company Profit (required)
- Pension Contribution (optional)

#### For Sole Traders:
- Trading Income (required)
- Allowable Expenses (required)
- Pension Contribution (optional)
- Capital Allowances (optional)

#### For Company Owners:
- Company Profit (required)
- Director Salary (required)
- Dividends (required)
- R&D Expenditure (optional)
- Capital Investment (optional)

#### For Landlords:
- Rental Income (required)
- Mortgage Interest (required)
- Other Expenses (required)
- Number of Properties (optional, default: 1)
- Properties are Furnished (optional checkbox)

### Step 3: View Your Results

The calculator will show:

1. **Current Position**: Your current tax situation
2. **Optimal Position**: Recommended structure for tax efficiency
3. **Potential Savings**: How much you could save
4. **Tax Strategies**: Personalized recommendations

## Example Scenarios

### Example 1: Company Director

**Input:**
- Salary: £30,000
- Dividends: £20,000
- Company Profit: £60,000

**Output:**
- Current total tax: £21,586.65
- Optimal total tax: £12,384.13
- **Potential saving: £9,202.52**

**Recommendations:**
1. Set salary at £12,570 (personal allowance)
2. Extract remaining profits as dividends
3. Consider pension contributions
4. Split dividends across tax years

### Example 2: Sole Trader

**Input:**
- Trading Income: £50,000
- Allowable Expenses: £8,000
- Pension Contribution: £3,000

**Output:**
- Taxable Profit: £40,000
- Tax position calculated with pension relief

**Recommendations:**
1. Enhance expense tracking
2. Claim Annual Investment Allowance
3. Maximize pension contributions
4. Consider income splitting

### Example 3: Landlord

**Input:**
- Rental Income: £30,000
- Mortgage Interest: £8,000
- Other Expenses: £5,000
- 2 properties, furnished

**Output:**
- Taxable Income: £25,000
- Method: Expenses + Finance Cost Restriction

**Recommendations:**
1. Utilize replacement of domestic items relief
2. Consider incorporation (potential saving: £2,500)
3. Joint ownership with spouse/partner
4. Maximize allowable expenses

## API Testing

You can test the API directly using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Test director optimization
curl -X POST http://localhost:5000/api/optimize/director \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 30000,
    "dividends": 20000,
    "company_profit": 60000,
    "pension_contribution": 0
  }'

# Test sole trader optimization
curl -X POST http://localhost:5000/api/optimize/sole-trader \
  -H "Content-Type: application/json" \
  -d '{
    "trading_income": 50000,
    "allowable_expenses": 8000,
    "pension_contribution": 3000,
    "capital_allowances": 2000
  }'
```

## Features

### Frontend Features
- ✅ Responsive design with TailwindCSS
- ✅ Dynamic form validation
- ✅ User-friendly interface
- ✅ Visual result comparison
- ✅ Loading states and error handling
- ✅ Mobile-friendly layout

### Backend Features
- ✅ RESTful API with Flask
- ✅ Comprehensive tax calculations
- ✅ Input validation
- ✅ Error handling
- ✅ CORS enabled for frontend integration
- ✅ Modular architecture

### Tax Calculations
- ✅ PAYE (Income Tax)
- ✅ National Insurance
- ✅ Corporation Tax
- ✅ Dividend Tax
- ✅ Pension Relief
- ✅ Trading Allowance
- ✅ Property Allowance
- ✅ Capital Allowances
- ✅ R&D Relief

## Tax Rates Used

Based on HMRC 2025/2026 rates (illustrative):

- Personal Allowance: £12,570
- Basic Rate: 20% (£12,571 - £50,270)
- Higher Rate: 40% (£50,271 - £150,000)
- Additional Rate: 45% (Over £150,000)
- NI Rate below UEL: 8%
- NI Rate above UEL: 2%
- Corporation Tax: 19%-25%
- Dividend Allowance: £500

## Troubleshooting

### API not starting
- Check port 5000 is available
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version: Python 3.7+

### Frontend not connecting to API
- Ensure API is running on port 5000
- Check browser console for errors
- Verify CORS is enabled in api.py

### Form validation errors
- All required fields must be filled
- Values must be non-negative numbers
- Number of properties must be at least 1

## Security Notice

⚠️ **Important**: This is a demonstration application. For production use:
- Add authentication
- Implement rate limiting
- Use HTTPS
- Add input sanitization
- Implement logging
- Use environment variables

## Legal Disclaimer

This calculator provides illustrative guidance only and is not official tax advice. Always consult with a qualified tax advisor or accountant for official advice.

## Support

For issues or questions:
1. Check this guide
2. Review README_TAX_OPTIMIZER.md
3. Test with provided examples
4. Check API logs in /tmp/api.log

## Next Steps

After using the calculator:
1. Review all recommendations carefully
2. Consult with a tax advisor
3. Implement changes gradually
4. Track savings achieved
5. Review annually

---

**Built with Python, Flask, TailwindCSS, and JavaScript**
