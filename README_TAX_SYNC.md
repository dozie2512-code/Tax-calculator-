# Tax Data Synchronization Feature

## Overview

The Tax Data Synchronization feature automatically synchronizes financial data from postings to optimize tax computations with reliefs, allowances, allowable expenses, and capital allowances for various entity types and tax classes.

## Supported Entities

- **Sole Traders / Self-Employed** - Income Tax, Class 2 & 4 National Insurance
- **Limited Companies** - Corporation Tax, Directors' PAYE
- **Landlords / Property Owners** - Income Tax, Capital Gains Tax (CGT)
- **Employees** - PAYE, Class 1 National Insurance

## Supported Tax Classes

- **PAYE** (Pay As You Earn) - Employee and Director taxation
- **Company Tax** - Corporation Tax for limited companies
- **Capital Gains Tax (CGT)** - Property and asset disposals
- **Withholding Tax (WHT)** - Interest, royalties, dividends
- **VAT** (Value Added Tax) - Standard, reduced, and zero rates

## Key Features

### 1. **Automated Data Synchronization**
- Reads financial transactions from posting data
- Categorizes transactions by type (income, expenses, capital, etc.)
- Identifies allowable vs non-allowable expenses
- Calculates capital allowances automatically

### 2. **Relief and Allowance Optimization**
The system automatically applies UK HMRC allowances and reliefs:

#### Personal Allowances
- Personal Allowance: £12,570
- Trading Allowance: £1,000 (sole traders)
- Property Allowance: £1,000 (landlords)
- Dividend Allowance: £500
- Personal Savings Allowance: £1,000 (basic) / £500 (higher)
- Marriage Allowance: £1,260 (transferable)
- Pension Annual Allowance: £60,000
- Capital Gains Allowance: £3,000

#### Capital Allowances
- **Annual Investment Allowance (AIA)**: 100% relief up to £1,000,000
- **Writing Down Allowance (WDA)**: 
  - Main Pool: 18% per annum
  - Special Rate Pool: 6% per annum

### 3. **Intelligent Expense Categorization**
The system automatically identifies allowable business expenses:
- ✅ Office supplies, utilities, software
- ✅ Travel, marketing, advertising
- ✅ Professional fees, training
- ✅ Equipment, maintenance
- ❌ Entertainment, personal expenses
- ❌ Fines and penalties

## Usage

### Backend (Python)

#### Run Tax Synchronization Standalone
```bash
cd /home/runner/work/Tax-calculator-/Tax-calculator-
python backend/tax_sync.py
```

#### Run Complete Month-End Close Process
```bash
python run_month_end_close.py
```

This will:
1. Perform account reconciliation
2. Calculate and post accruals
3. Generate financial statements
4. **Synchronize tax data from postings** ← New Step

### Frontend (Web Interface)

1. Navigate to the **Tax Optimization** section
2. Select your **Entity Type** (Sole Trader, Company, Landlord, or Employee)
3. Click **"🔄 Sync Data from Postings"** to synchronize fresh data
4. Or click **"📥 Load Synced Data"** to load previously synchronized data
5. Review auto-populated fields
6. Click **"Calculate Comprehensive Tax"** to see detailed analysis

## Output Files

### `output/tax_synchronized_data.json`
Contains synchronized data for all entity types:
```json
{
  "synchronization_date": "2026-01-17T23:08:15.544625",
  "entities": {
    "sole_trader": {
      "gross_income": 42000.0,
      "allowable_expenses": 17200.0,
      "capital_allowance": {
        "aia_relief": 0,
        "wda_relief": 0.0,
        "total_relief": 0.0
      },
      "trading_allowance": 1000,
      "profit": 24800.0
    },
    "company": { ... },
    "landlord": { ... },
    "employee": { ... }
  },
  "allowances": { ... },
  "summary": { ... }
}
```

## Tax Computation Features

### For Sole Traders
- Gross income from business activities
- Allowable business expenses
- Trading allowance option (£1,000)
- Capital allowances (AIA & WDA)
- Income Tax calculation with progressive rates
- Class 2 NI (£3.45/week if profits > £6,725)
- Class 4 NI (9% on £12,570-£50,270, 2% above)
- Pension contribution relief
- VAT tracking (if registered)

### For Limited Companies
- Company profit before tax
- Corporation Tax (19% up to £50k, 25% over £250k)
- Director's salary optimization
- Dividend tax calculation
- Employer's NI considerations
- VAT tracking

### For Landlords
- Rental income
- Property expenses
- Property allowance option (£1,000)
- Mortgage interest relief (20% tax credit)
- Capital Gains Tax on property sales
- CGT annual exemption (£3,000)

### For Employees (PAYE)
- Gross salary and bonuses
- Income Tax via PAYE
- Class 1 NI (12% on £12,570-£50,270, 2% above)
- Student loan repayments
- Pension contributions relief
- Additional income from dividends/rental

## Tax Optimization Tips

The system provides intelligent optimization suggestions:
- Review all allowable business expenses
- Consider increasing pension contributions for tax relief
- Optimal salary/dividend mix for company directors
- Timing of dividend payments
- Property ownership structure optimization
- Marriage allowance transfer opportunities
- VAT registration threshold monitoring

## Architecture

### Backend Module: `backend/tax_sync.py`

**Key Classes:**
- `TaxDataSynchronizer` - Main synchronization engine

**Key Methods:**
- `categorize_transactions()` - Categorizes transactions by type
- `synchronize_sole_trader_data()` - Syncs sole trader data
- `synchronize_company_data()` - Syncs company data
- `synchronize_landlord_data()` - Syncs landlord data
- `synchronize_employee_data()` - Syncs employee data
- `calculate_optimized_allowances()` - Calculates all allowances
- `_calculate_capital_allowance()` - Computes capital allowances
- `export_synchronized_data()` - Exports to JSON

### Frontend Integration: `index.html`

**New UI Components:**
- Data Synchronization Card
- Sync/Load buttons
- Status notifications
- Auto-population of form fields

**Key JavaScript Functions:**
- `syncTaxData()` - Triggers synchronization
- `loadSyncedData()` - Loads synced data from JSON
- `populateFormWithSyncedData()` - Auto-fills form fields
- `generateMockSyncData()` - Fallback mock data

## Integration with Month-End Close

The tax synchronization is integrated as Step 4 in the autonomous month-end close process:

1. **Step 1**: Account Reconciliation
2. **Step 2**: Accrual Postings
3. **Step 3**: Financial Statement Generation
4. **Step 4**: Tax Data Synchronization ← NEW

## Sample Output

### Console Output
```
=== Tax Data Synchronization ===

Synchronizing Sole Trader data...
Synchronizing Company data...
Synchronizing Landlord data...
Synchronizing Employee data...
Calculating optimized allowances...

✓ Tax data synchronized and exported to output/tax_synchronized_data.json

--- Synchronization Summary ---
Total Income: £42,000.00
Total Expenses: £17,200.00
Allowable Expenses: £17,200.00
Capital Expenditure: £0.00
VAT Transactions Count: 0
Payroll Transactions Count: 1
```

### Tax Calculation Example (Sole Trader)
```
Gross Income:              £42,000.00
Less: Expenses:            £17,200.00
Trading Profit:            £24,800.00
Less: Pension:             £0.00
Adjusted Profit:           £24,800.00
Personal Allowance:        £12,570.00
Taxable Income:            £12,230.00
Income Tax:                £2,446.00
Class 2 NI:                £179.40
Class 4 NI:                £1,100.70
Total Tax & NI:            £3,726.10
Net Income After Tax:      £21,073.90
```

## UK HMRC Compliance

All calculations are based on UK HMRC tax rules for the 2024/25 tax year:
- Income Tax rates: 20%, 40%, 45%
- Personal Allowance: £12,570 (tapers above £100k)
- NI thresholds and rates
- Corporation Tax: 19%-25%
- CGT annual exemption: £3,000
- VAT threshold: £90,000

**Note**: Always consult HMRC guidance or a qualified tax professional for specific advice.

## Future Enhancements

- Real-time Xero API integration
- Multi-year tax planning
- Tax loss carry-forward/carry-back
- R&D tax credit calculations
- HMRC MTD (Making Tax Digital) submission
- Scenario analysis (what-if calculations)
- Multi-currency support
- Scottish/Welsh tax variations

## Support

For issues or questions about the tax synchronization feature, please refer to:
- Main README: `README_MONTH_END_CLOSE.md`
- Implementation Summary: `IMPLEMENTATION_SUMMARY.txt`
- Backend code: `backend/tax_sync.py`
- Frontend code: `index.html` (search for "syncTaxData")
