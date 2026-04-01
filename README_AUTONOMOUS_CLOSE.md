# Autonomous Month-End Close - HTML Prototype

A standalone, browser-based implementation of the autonomous month-end close process. This HTML file converts the Python backend functionality into an interactive web application that runs entirely in the browser.

## 🚀 Quick Start

Simply open `autonomous_close.html` in any modern web browser:

```bash
# On Linux/Mac
open autonomous_close.html

# On Windows
start autonomous_close.html

# Or double-click the file
```

No server, no installation, no dependencies required!

## 📋 Features

### 1. Autonomous Reconciliation 🔍
- **GL vs Bank Matching**: Automatically matches general ledger transactions with bank statements
- **Smart Algorithm**: Matches based on amount, date, and reference/description similarity
- **Discrepancy Detection**: Identifies and flags potential issues
- **Confidence Scoring**: High/Medium confidence levels for matches
- **Summary Metrics**: Reconciliation rate, matched/unmatched counts, total amounts

**How to Use:**
1. Click "Load Sample Data" or paste your own CSV data
2. Click "Run Reconciliation"
3. Review matched, unmatched, and discrepancy results

### 2. Intelligent Accrual Postings 📊
- **Interest Accrual**: Calculate based on principal and annual rate
- **Depreciation**: Straight-line depreciation calculation
- **Expense Accrual**: Periodic expense accruals (rent, insurance, etc.)
- **Journal Entry Generation**: Automatic balanced journal entries
- **Balance Verification**: Ensures debits equal credits

**How to Use:**
1. Enter values for each accrual type (or use defaults)
2. Click "Calculate" for each accrual
3. View generated journal entries and summary

### 3. Financial Statement Generation 📈
- **Profit & Loss Statement**: Revenue, COGS, expenses, net income
- **Balance Sheet**: Assets, liabilities, equity with balance verification
- **Account Classification**: Automatic classification by account number
- **Summary Metrics**: Key financial indicators

**How to Use:**
1. Click "Load Sample Data" or paste transaction data
2. Click "Generate Statements"
3. Review P&L and Balance Sheet

### 4. Automated Close with Risk Scoring 🎯
- **Progressive Workflow**: Step-by-step close process with progress bar
- **Risk Assessment**: Evaluates risk level for each step
- **Overall Risk Score**: 0-100 score with color-coded indicator
- **Visual Feedback**: Real-time status updates

**How to Use:**
1. Complete Reconciliation, Accruals, and Statements tabs first
2. Click "Start Automated Close"
3. Watch the progress and review risk assessment

### 5. Human Approval Workflow ✅
- **Approve/Reject**: Approve or reject each component
- **Comments**: Add reviewer notes for each item
- **Approval History**: Track all approvals with timestamps
- **Status Tracking**: Visual status badges for each item

**How to Use:**
1. Review results from previous tabs
2. Add comments if needed
3. Click "Approve" or "Reject" for each component
4. View approval history at the bottom

## 📊 Sample Data

The application includes built-in sample data for testing:

**Reconciliation:**
- 9 GL transactions
- 9 Bank transactions
- 88.89% reconciliation rate
- 1 unmatched GL item
- 1 unmatched Bank item

**Accruals:**
- Interest: £416.67 (£100,000 @ 5% annual for 1 month)
- Depreciation: £750.00 (£50,000 asset, £5,000 salvage, 5 years)
- Insurance: £1,000.00 (£12,000 annual for 1 month)

**Transactions:**
- 20 sample transactions
- Revenue: £42,000
- Net Income: £18,500
- Total Assets: £73,500
- Balanced Balance Sheet

## 🎨 User Interface

- **Gradient Background**: Purple gradient design
- **Tab Navigation**: Easy switching between sections
- **Responsive Cards**: Clean, modern card layout
- **Color-Coded Badges**: Visual status indicators
- **Progress Bars**: Visual progress tracking
- **Tables**: Organized data presentation
- **Interactive Forms**: Real-time calculations

## 💾 Data Format

### Reconciliation CSV Format:
```csv
date,reference,description,amount
2024-12-01,REF001,Customer Payment,15000.00
```

### Transaction CSV Format:
```csv
date,account,description,debit,credit
2024-12-01,1000,Cash,50000.00,0
```

### Accrual CSV Format (not required for HTML):
```csv
type,principal,asset_cost,salvage_value,useful_life_years,months,name,annual_amount,debit_account,credit_account,date
interest,100000,,,,,,,7200,2300,2024-12-31
```

## 🔧 Technical Details

- **File Size**: 52KB
- **Lines of Code**: 1,273
- **Dependencies**: None (pure vanilla JavaScript)
- **Browser Compatibility**: Chrome, Firefox, Safari, Edge (modern versions)
- **Performance**: Instant calculations, no server required

## 🏗️ Architecture

### JavaScript Functions:
- `performReconciliation()`: Matches GL and bank transactions
- `calculateInterest()`: Calculates interest accruals
- `calculateDepreciation()`: Calculates depreciation
- `calculateExpense()`: Calculates expense accruals
- `generateStatements()`: Generates financial statements
- `runAutomatedClose()`: Orchestrates automated close process
- `approveItem()` / `rejectItem()`: Handles approval workflow

### State Management:
```javascript
state = {
    reconciliation: null,    // Reconciliation results
    accruals: [],           // Array of accrual entries
    statements: null,       // Financial statements
    approvals: {},          // Approval status
    approvalHistory: []     // History of approvals
}
```

## 📈 Workflows Demonstrated

### 1. Month-End Close Process:
```
Reconciliation → Accruals → Statements → Automated Close → Approval
```

### 2. Risk Scoring Algorithm:
```
- Reconciliation: >95% = Low, 80-95% = Medium, <80% = High
- Accruals: <£5K = Low, £5K-£10K = Medium, >£10K = High
- Statements: Balanced = Low, Unbalanced = High
- Overall: Average of all risk scores
```

### 3. Approval Workflow:
```
Pending → Review → Approve/Reject → History
```

## 🔍 Use Cases

1. **Training**: Teach accounting teams about month-end close processes
2. **Demonstration**: Show automated reconciliation capabilities
3. **Prototyping**: Test workflows before building production systems
4. **Education**: Learn about financial close automation
5. **Planning**: Design month-end close procedures

## ⚙️ Customization

### Modify Interest Rate:
```javascript
// Line ~415
const rate = safeFloat(document.getElementById('interestRate').value) / 100;
```

### Adjust Risk Thresholds:
```javascript
// Lines ~1141-1155
function calculateReconciliationRisk() {
    if (summary.reconPercentage >= 95) return 'low';
    if (summary.reconPercentage >= 80) return 'medium';
    return 'high';
}
```

### Change Account Classifications:
```javascript
// Lines ~1041-1048
function getAccountType(account) {
    const firstChar = account.charAt(0);
    if (firstChar === '1') return 'Asset';
    // ... modify as needed
}
```

## 🚨 Limitations

- **In-Memory Only**: Data is not saved to disk (use browser's download features if needed)
- **No Authentication**: No user login or access control
- **Single User**: Designed for single-user demonstrations
- **Sample Data**: Uses predefined sample data (can be customized)
- **Client-Side Only**: All processing happens in the browser

## 🔐 Security Notes

This is a **prototype** for demonstration purposes:
- Do not use with real financial data without proper security measures
- No data encryption or secure storage
- No audit logging (only in-memory approval history)
- No role-based access control

For production use, consider:
- Backend API with authentication
- Database storage with encryption
- Audit trail logging
- Multi-level approval workflows
- Data validation and sanitization

## 📚 Related Files

- `run_month_end_close.py`: Python backend orchestrator
- `backend/reconciliation.py`: Python reconciliation module
- `backend/accruals.py`: Python accruals module
- `backend/financial_statements.py`: Python statements module
- `frontend/dashboard.html`: Original approval dashboard (loads JSON files)

## 🎯 Key Differences from Python Backend

| Feature | Python Backend | HTML Prototype |
|---------|---------------|----------------|
| Execution | Command-line | Browser-based |
| Data Input | CSV files | Paste or load samples |
| Output | CSV/JSON files | On-screen display |
| State | File-based | In-memory |
| UI | Terminal | Interactive web UI |
| Portability | Requires Python | Runs anywhere |

## 🤝 Contributing

To enhance this prototype:
1. Open `autonomous_close.html` in a text editor
2. Modify the JavaScript functions as needed
3. Test in a browser
4. Share improvements!

## ❓ Troubleshooting

**Problem**: Page doesn't load
- **Solution**: Ensure you're using a modern browser (Chrome 90+, Firefox 88+, Safari 14+)

**Problem**: Sample data doesn't load
- **Solution**: Check browser console for JavaScript errors

**Problem**: Calculations seem wrong
- **Solution**: Verify input data format matches expected CSV structure

**Problem**: Approval buttons don't work
- **Solution**: Refresh the page and ensure you completed previous tabs first

## 📖 Documentation

For more details on the month-end close process, see:
- `README_MONTH_END_CLOSE.md`: Python backend documentation
- `IMPLEMENTATION_SUMMARY.txt`: Original implementation notes

## 🎓 Learning Resources

This prototype demonstrates:
- JavaScript ES6+ features
- DOM manipulation
- State management
- Event handling
- CSS Grid and Flexbox
- Responsive design
- Financial calculations
- Business logic implementation

## 📄 License

See repository license for details.

---

**Autonomous Month-End Close HTML Prototype**  
*Converting Python MVP to Interactive Web Application*  
*No dependencies • No installation • Just open and run*
