# Autonomous Month-End Close Process

An automated month-end close system for accounting processes, featuring account reconciliation, accrual postings, financial statement generation, and a human approval workflow.

## 📋 Overview

This prototype automates the month-end close process with the following features:

1. **Account Reconciliation** - Matches general ledger transactions with bank statements
2. **Accrual Postings** - Automatically calculates interest, depreciation, and other accruals
3. **Financial Statement Generation** - Creates P&L, Balance Sheet, and Cash Flow statements
4. **Approval Workflow** - Simple web dashboard for reviewing and approving results

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Tax-calculator-
```

2. No additional Python packages required - uses only standard library!

### Running the Process

1. **Run the month-end close process:**
```bash
python run_month_end_close.py
```

This will:
- Perform account reconciliation between GL and bank statements
- Calculate and post accruals (interest, depreciation, expenses)
- Generate financial statements (P&L, Balance Sheet, Cash Flow)
- Save all results to the `output/` directory

2. **Review and approve results:**

Open the approval dashboard in your browser:
```bash
# On Linux/Mac
open index.html

# On Windows
start index.html

# Or navigate directly to:
# file:///path/to/Tax-calculator-/index.html
```

## 📁 Project Structure

```
Tax-calculator-/
├── backend/
│   ├── reconciliation.py      # Account reconciliation module
│   ├── accruals.py            # Accrual calculations module
│   ├── financial_statements.py # Statement generation module
│   └── utils.py               # Utility functions
├── sample_data/
│   ├── general_ledger.csv     # Sample GL transactions
│   ├── bank_statement.csv     # Sample bank transactions
│   ├── transactions.csv       # Sample transaction data
│   └── accruals.csv          # Accrual specifications
├── output/                    # Generated output files (created on run)
│   ├── reconciliation_*.csv   # Reconciliation results
│   ├── journal_entries.*      # Journal entries
│   ├── financial_statements.json # Financial statements
│   └── month_end_close_results.json # Complete results
├── index.html                 # Approval workflow UI dashboard
├── run_month_end_close.py     # Main orchestration script
└── README.md                  # This file
```

## 🔧 Usage

### 1. Account Reconciliation

The reconciliation module matches transactions between your general ledger and bank statement:

**Input Files:**
- `sample_data/general_ledger.csv`
- `sample_data/bank_statement.csv`

**CSV Format:**
```csv
date,reference,description,amount
2024-12-01,REF001,Customer Payment,15000.00
```

**Output:**
- `output/reconciliation_matched.csv` - Successfully matched transactions
- `output/reconciliation_unmatched_gl.csv` - Unmatched GL items
- `output/reconciliation_unmatched_bank.csv` - Unmatched bank items
- `output/reconciliation_discrepancies.csv` - Flagged discrepancies
- `output/reconciliation_summary.json` - Summary report

**Running standalone:**
```bash
cd backend
python reconciliation.py
```

### 2. Accrual Postings

Automatically calculates accruals and generates journal entries:

**Input File:**
- `sample_data/accruals.csv`

**Supported Accrual Types:**
- **Interest**: Based on principal and interest rate
- **Depreciation**: Straight-line method
- **Expenses**: Periodic expense accruals

**CSV Format:**
```csv
type,principal,asset_cost,salvage_value,useful_life_years,months,name,annual_amount,debit_account,credit_account,date
interest,100000,,,,,,,7200,2300,2024-12-31
depreciation,,50000,5000,5,,,,7100,1500,2024-12-31
expense,,,,,1,Insurance,12000,6100,2000,2024-12-31
```

**Output:**
- `output/journal_entries.json` - Journal entries in JSON format
- `output/journal_entries.csv` - Journal entries in CSV format

**Running standalone:**
```bash
cd backend
python accruals.py
```

### 3. Financial Statement Generation

Generates comprehensive financial statements from transaction data:

**Input File:**
- `sample_data/transactions.csv`

**CSV Format:**
```csv
date,account,description,debit,credit
2024-12-01,1000,Cash - Opening Balance,50000.00,0
2024-12-01,4100,Sales Revenue,0,15000.00
```

**Output:**
- `output/financial_statements.json` - Complete statements including:
  - Profit & Loss Statement (Income Statement)
  - Balance Sheet
  - Cash Flow Statement

**Running standalone:**
```bash
cd backend
python financial_statements.py
```

## 🎨 Approval Dashboard

The approval dashboard (index.html) provides a user-friendly interface for reviewing and approving month-end close results.

**Features:**
- Visual summary of reconciliation results
- Accrual posting overview
- Financial statement highlights
- Approve/reject workflow for each component
- Approval history tracking
- Responsive design

**Access:**
Open `index.html` in your web browser after running the month-end close process.

## 📊 Sample Data

The repository includes sample data to demonstrate functionality:

- **general_ledger.csv**: 9 sample GL transactions
- **bank_statement.csv**: 9 sample bank transactions
- **transactions.csv**: 30 sample accounting transactions
- **accruals.csv**: 3 sample accrual specifications

### Customizing Sample Data

You can modify the CSV files in the `sample_data/` directory to test with your own data. Ensure the column headers match the expected format.

## 🏗️ Architecture

### Modular Design

Each module is self-contained and can be used independently:

```python
# Example: Using reconciliation module independently
from backend.reconciliation import AccountReconciliation

reconciler = AccountReconciliation('gl.csv', 'bank.csv')
summary = reconciler.reconcile()
reconciler.export_results('output/recon')
```

### Account Type Classification

The system uses account number ranges to classify accounts:
- **1000-1999**: Assets
- **2000-2999**: Liabilities
- **3000-3999**: Equity
- **4000-4999**: Revenue
- **5000-5999**: Cost of Goods Sold
- **6000-7999**: Expenses

### Configuration

Accrual rates can be customized via a JSON config file:

```json
{
  "interest_rate": 0.05,
  "depreciation_rate": 0.10,
  "accrual_accounts": {
    "interest_expense": "7200",
    "interest_payable": "2300"
  }
}
```

## 🔍 How It Works

### Month-End Close Process Flow

1. **Initialization**
   - Create output directory
   - Load configuration and sample data

2. **Account Reconciliation**
   - Read GL and bank statement data
   - Match transactions based on amount, date, and reference
   - Flag discrepancies
   - Export matched/unmatched items

3. **Accrual Postings**
   - Calculate interest accruals
   - Calculate depreciation
   - Calculate expense accruals
   - Generate balanced journal entries

4. **Financial Statement Generation**
   - Process all transactions
   - Calculate account balances
   - Generate P&L statement (revenue, expenses, net income)
   - Generate balance sheet (assets, liabilities, equity)
   - Generate cash flow statement

5. **Approval Workflow**
   - Display results in dashboard
   - Allow human review and approval
   - Track approval history

## 🛠️ Extending the System

### Adding Custom Accrual Types

Edit `backend/accruals.py` and add a new calculation method:

```python
def calculate_custom_accrual(self, params):
    # Your calculation logic
    accrual = {
        'type': 'Custom Accrual',
        'accrual_amount': calculated_amount,
        # ... other fields
    }
    return accrual
```

### Adding New Reconciliation Rules

Edit `backend/reconciliation.py` to customize matching criteria:

```python
# In the reconcile() method, modify matching logic:
amount_match = abs(gl_amount - bank_amount) <= tolerance
date_match = gl_date == bank_date
# Add custom matching rules here
```

### Customizing Financial Statements

Edit `backend/financial_statements.py` to add sections or modify calculations:

```python
def generate_custom_section(self) -> Dict[str, Any]:
    # Your custom statement section
    return custom_data
```

## 📝 Testing

### Running Individual Modules

Each backend module can be tested independently:

```bash
# Test reconciliation
cd backend
python reconciliation.py

# Test accruals
python accruals.py

# Test financial statements
python financial_statements.py
```

### Testing with Custom Data

1. Create your own CSV files in `sample_data/`
2. Update the file paths in the modules if needed
3. Run the appropriate module or the full process

## 🔒 Security Considerations

- This is a prototype for demonstration purposes
- In production, add authentication to the approval dashboard
- Implement audit logging for all approvals/rejections
- Add data validation and sanitization
- Use secure storage for financial data
- Implement access controls based on user roles

## 🚀 Future Enhancements

Potential improvements for production use:

1. **Database Integration**
   - Replace CSV files with database connections
   - Support multiple data sources (SQL, REST APIs)

2. **Advanced Reconciliation**
   - Machine learning for transaction matching
   - Multi-currency support
   - Partial matching algorithms

3. **Enhanced UI**
   - Backend API (Flask/FastAPI)
   - Interactive charts and graphs
   - Email notifications for approvals
   - Mobile-responsive design improvements

4. **Workflow Engine**
   - Multi-level approval workflows
   - Role-based access control
   - Automated escalation

5. **Reporting**
   - PDF/Excel export functionality
   - Custom report templates
   - Scheduled report generation

6. **Integration**
   - ERP system integration
   - Banking API connections
   - Accounting software plugins

## 📖 Code Comments

All code is well-commented to facilitate future development:

- Module-level docstrings explain purpose and usage
- Function docstrings detail parameters and return values
- Inline comments clarify complex logic
- Type hints improve code readability

## 🤝 Contributing

This is a prototype project. To extend it:

1. Follow the existing code structure
2. Add docstrings to new functions
3. Update this README with new features
4. Test thoroughly with sample data

## 📄 License

This is a demonstration project. Check with the repository owner for licensing information.

## ❓ Support

For questions or issues:
1. Check the code comments for implementation details
2. Review the sample data format
3. Test with the provided sample data first
4. Ensure Python 3.7+ is installed

## 🎯 Summary

This Autonomous Month-End Close prototype demonstrates:

✅ Automated account reconciliation with discrepancy flagging  
✅ Automated accrual calculations and journal entry generation  
✅ Complete financial statement generation from transaction data  
✅ Human approval workflow with simple web interface  
✅ Modular, extensible architecture  
✅ Well-documented, commented code  
✅ Sample data for immediate testing  

Perfect for understanding month-end close automation concepts and as a foundation for building production-ready systems!
