# Month-End Close Automation System

A comprehensive financial automation system available in both Python and HTML implementations.

## 🎯 What's New

The Python-based month-end close automation script has been converted into a **standalone HTML front-end prototype** (`index.html`). You can now run the entire month-end close process directly in your web browser without any installation!

## 📁 Repository Structure

```
Tax-calculator-/
├── index.html                    # ⭐ NEW: Standalone HTML prototype (recommended)
├── run_month_end_close.py       # Python orchestration script
├── backend/                      # Python backend modules
│   ├── reconciliation.py
│   ├── accruals.py
│   ├── financial_statements.py
│   └── utils.py
├── frontend/
│   └── dashboard.html           # Python output viewer
└── sample_data/                 # Sample CSV data files
```

## 🚀 Quick Start

### Option 1: HTML Prototype (Recommended - No Installation!)

Simply open `index.html` in any modern web browser:

```bash
# On Linux/Mac
open index.html

# On Windows
start index.html

# Or just double-click the file
```

**Features:**
- ✅ No installation required
- ✅ Works offline
- ✅ Interactive user interface
- ✅ Real-time calculations
- ✅ Visual data entry and display

### Option 2: Python Implementation

If you prefer the Python version:

1. Install Python 3.7+
2. Run the process:
   ```bash
   python run_month_end_close.py
   ```
3. View results in `frontend/dashboard.html`

## 📊 Features

Both implementations provide:

### 1. Account Reconciliation 🔍
- Match GL transactions with bank statements
- Identify discrepancies and unmatched items
- Calculate reconciliation percentage
- Export detailed reconciliation reports

### 2. Accrual Postings 📝
- Interest accrual calculations
- Depreciation (straight-line method)
- Periodic expense accruals
- Automated journal entry generation

### 3. Financial Statements 💰
- Profit & Loss Statement
- Balance Sheet
- Cash Flow Statement
- Automatic balance validation

## 🎨 HTML Prototype Features

The new HTML prototype offers:

- **Modern UI**: Clean, gradient design with intuitive navigation
- **Tabbed Interface**: Easy access to all features
- **CSV Support**: Standard CSV format for data input
- **Real-time Processing**: Instant calculations in the browser
- **Responsive Design**: Works on desktop, tablet, and mobile
- **No Dependencies**: Pure HTML/CSS/JavaScript

## 📖 Usage Guide

### HTML Prototype

1. **Overview Tab**: View system statistics and feature descriptions
2. **Reconciliation Tab**: 
   - Paste GL transactions in CSV format
   - Paste bank transactions in CSV format
   - Click "Perform Reconciliation"
3. **Accruals Tab**:
   - Select accrual type (Interest/Depreciation/Expense)
   - Enter relevant parameters
   - Click "Calculate Accrual"
   - Generate journal entry if needed
4. **Financial Statements Tab**:
   - Paste transaction data in CSV format
   - Select statement type
   - Click "Generate Statements"

### Python Implementation

See `README_MONTH_END_CLOSE.md` for detailed Python instructions.

## 📝 CSV Format Examples

### Reconciliation Input
```csv
date,reference,description,amount
2026-01-01,INV001,Client Payment,1500.00
2026-01-02,INV002,Office Supplies,-250.00
```

### Financial Statements Input
```csv
date,account,account_type,description,debit,credit
2026-01-01,4000,Revenue,Sales,0,5000
2026-01-01,1000,Asset,Cash,5000,0
```

## 🔒 Security & Privacy

- All HTML prototype calculations run client-side
- No data is transmitted to any server
- No external dependencies or tracking
- Your data stays in your browser

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is provided as-is for educational and business use.

## 🎉 Which Version Should I Use?

| Need | Use |
|------|-----|
| Quick demo or testing | HTML Prototype |
| No technical knowledge | HTML Prototype |
| Mobile/tablet access | HTML Prototype |
| Integration with Python systems | Python Implementation |
| Batch processing | Python Implementation |
| Automated workflows | Python Implementation |

**Recommendation**: Start with the HTML prototype (`index.html`) for ease of use, then consider the Python implementation if you need automation or integration capabilities.
