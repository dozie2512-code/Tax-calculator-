# UK Tax Computations - Multi-User & Multi-Business Support

## Overview

The UK Tax Computations section has been enhanced with multi-user and multi-business support, enabling dynamic tax calculations based on imported bank transaction data. This feature allows different users and businesses to have their own isolated transaction data and tax computations.

## Features

### 1. Multi-User & Multi-Business Selection
- **User Dropdown**: Select from predefined users (John Smith, Jane Doe, Michael Brown)
- **Business Dropdown**: Select from predefined businesses (Tech Solutions Ltd, Consulting Services Ltd, Retail Ventures Ltd)
- **Selection Indicator**: Clear display of the selected user-business combination

### 2. CSV Import Functionality
- **File Upload**: Upload CSV files directly from your computer
- **Paste Data**: Paste CSV data directly into the text area
- **Format Validation**: Real-time validation of CSV format and content
- **Transaction Preview**: Preview all transactions before importing
- **Sample Data**: Load pre-configured sample data for testing

#### CSV Format Requirements
```csv
date,description,amount,reference,category
2024-12-01,Client Payment,15000.00,INV001,Income
2024-12-05,Office Rent,-3000.00,RENT12,Expense
```

**Required Fields:**
- `date`: Transaction date (YYYY-MM-DD format recommended)
- `description`: Transaction description
- `amount`: Transaction amount (positive for income, negative for expenses)

**Optional Fields:**
- `reference`: Reference number or code
- `category`: Transaction category

### 3. CSV Validation
The system validates:
- ✅ File structure (headers and data rows)
- ✅ Required fields presence
- ✅ Data type validation (numeric amounts)
- ✅ Empty field detection
- ⚠️ Date format warnings

### 4. Dynamic Tax Computation
Based on imported transactions, the system automatically calculates:

#### Corporation Tax
- **Small Profits Rate (19%)**: For profits up to £50,000
- **Main Rate (25%)**: For profits over £250,000
- **Marginal Relief**: For profits between £50,000 and £250,000

#### VAT
- **Output VAT**: 20% on sales/income
- **Input VAT**: 20% on purchases/expenses
- **Net VAT**: Payable or refundable amount

### 5. Transaction Summary
- **Income Transactions**: Detailed list with dates, descriptions, and amounts
- **Expense Transactions**: Detailed list with dates, descriptions, and amounts
- Color-coded display for easy identification

## Usage Guide

### Step 1: Select User and Business
1. Navigate to the UK Tax Computations tab
2. Select a user from the "Select User" dropdown
3. Select a business from the "Select Business" dropdown
4. Verify the selection is displayed below the dropdowns

### Step 2: Import Transaction Data
1. Click on "📁 Import Bank Transaction Data (CSV)" to expand the section
2. Choose one of the following options:
   - **Upload File**: Click "Choose File" and select a CSV file
   - **Paste Data**: Paste CSV content into the text area
   - **Load Sample**: Click "Load Sample Data" to use pre-configured data
3. Click "Validate & Import CSV"

### Step 3: Review Validation Results
- ✅ **Success**: Green message showing number of valid transactions
- ❌ **Errors**: Red message listing validation errors to fix
- Transaction preview table displays all valid transactions

### Step 4: Confirm Import
1. Review the transaction preview table
2. Click "✓ Confirm Import" to import the transactions
3. See success message confirming import

### Step 5: Calculate Taxes
1. Expand "📊 Dynamic Tax Computation from Transactions"
2. Click "Calculate Taxes from Transactions"
3. Review the comprehensive tax computation results:
   - Transaction count
   - Total income and expenses
   - Net profit
   - Corporation tax liability with rate
   - VAT calculations

## Backend API

### Module: `uk_tax_computations.py`

The backend module provides:

```python
from backend.uk_tax_computations import UKTaxComputations

# Initialize
tax_comp = UKTaxComputations()

# Add users and businesses
tax_comp.add_user('user1', 'John Smith')
tax_comp.add_business('biz1', 'Tech Solutions Ltd')

# Import transactions
csv_data = "date,description,amount\n2024-12-01,Payment,1000.00"
result = tax_comp.import_transactions_from_csv(csv_data, 'user1', 'biz1')

# Compute taxes
computation = tax_comp.compute_tax_from_transactions('user1', 'biz1')
```

### Key Methods

#### `add_user(user_id, user_name, user_data=None)`
Add a new user to the system.

#### `add_business(business_id, business_name, business_data=None)`
Add a new business to the system.

#### `validate_csv_data(csv_content)`
Validate CSV format and content. Returns validation results.

#### `import_transactions_from_csv(csv_content, user_id, business_id)`
Import transactions from CSV for a specific user-business combination.

#### `compute_tax_from_transactions(user_id, business_id)`
Compute taxes based on imported transactions for a user-business pair.

#### `get_transactions(user_id=None, business_id=None)`
Retrieve transactions filtered by user and/or business.

## Testing

### Unit Tests
Run the comprehensive test suite:

```bash
cd /home/runner/work/Tax-calculator-/Tax-calculator-
python -m unittest tests.test_uk_tax_computations -v
```

**Test Coverage:**
- ✅ User and business management
- ✅ User-business associations
- ✅ CSV validation (valid/invalid cases)
- ✅ Transaction import
- ✅ Tax computation accuracy
- ✅ Multi-user/business isolation
- ✅ VAT calculations

### Manual Testing
1. Open `index.html` in a web browser
2. Navigate to UK Tax Computations tab
3. Follow the usage guide above
4. Test with different user-business combinations
5. Test with various CSV data formats

## Sample Data

Sample transaction data is provided in:
- `sample_data/bank_transactions_uk.csv`

Sample includes:
- 4 income transactions (£42,000 total)
- 6 expense transactions (£11,800 total)
- Net profit: £30,200
- Expected Corporation Tax: £5,738 (19% small profits rate)

## Tax Computation Logic

### Corporation Tax Rates (2024/25)

| Profit Range | Rate | Description |
|-------------|------|-------------|
| £0 - £50,000 | 19% | Small profits rate |
| £50,001 - £249,999 | 25% - relief | Marginal relief |
| £250,000+ | 25% | Main rate |

**Marginal Relief Formula:**
```
Relief = (Upper Limit - Taxable Profit) × 0.015
Tax = (Taxable Profit × 25%) - Relief
```

### VAT Calculation
- **Standard Rate**: 20%
- **Calculation**: Net of Input VAT and Output VAT
- **Positive**: Payable to HMRC
- **Negative**: Refundable from HMRC

## Data Isolation

Each user-business combination has:
- **Isolated Transaction Store**: Transactions are stored separately
- **Independent Computations**: Tax calculations are per combination
- **No Data Leakage**: Changing selection shows only relevant data

## Error Handling

The system handles:
- ❌ Missing required fields
- ❌ Invalid data types
- ❌ Empty required fields
- ❌ Malformed CSV structure
- ⚠️ Date format warnings

## Future Enhancements

Potential improvements:
1. **Persistent Storage**: Save data to database
2. **More Tax Types**: PAYE, Self-Assessment integration
3. **Export Results**: PDF/Excel export
4. **Historical Data**: Track computations over time
5. **Advanced Validation**: Custom validation rules
6. **Bulk Import**: Multiple files at once
7. **Data Analytics**: Trends and insights

## Architecture

### Frontend (JavaScript)
- `ukTaxState`: Global state management
- Event handlers for user interactions
- CSV parsing and validation
- Dynamic UI updates

### Backend (Python)
- `UKTaxComputations` class: Main business logic
- CSV validation and parsing
- Tax computation algorithms
- Data storage and retrieval

## Support

For issues or questions:
1. Check validation messages
2. Review CSV format requirements
3. Ensure user and business are selected
4. Verify transaction data format

## Version History

**v1.0** (Current)
- Multi-user and multi-business support
- CSV import functionality
- Dynamic tax computations
- Transaction preview and validation
- Comprehensive unit tests
