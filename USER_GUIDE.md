# Multi-User and Multi-Business Tax Calculator - User Guide

## Overview

The Tax Calculator now supports multiple users and multiple businesses, with integrated bank transaction import functionality. This guide explains how to use the new features.

## Features

### 1. User Authentication
- **Registration**: Create a new user account with username, password, email, and full name
- **Login**: Secure login with session management
- **Session Management**: Sessions automatically expire after 24 hours

### 2. Multi-Business Support
- Create and manage multiple businesses per user
- Switch between businesses seamlessly
- Each business has independent data and transactions
- Business types: Sole Trader, Limited Company, Partnership, etc.

### 3. Bank Transaction Integration
- Upload bank statement CSV files
- Automatic transaction categorization
- Map transactions to tax computation categories
- Apply imported data to tax calculations

## Getting Started

### Initial Setup

1. **Open the Application**
   - Open `index.html` in your web browser
   - You'll see the authentication modal

2. **Register a New Account**
   - Click the "Register" tab
   - Fill in:
     - Full Name
     - Email Address
     - Username
     - Password
   - Click "Register"
   - You'll see a success message

3. **Login**
   - Switch to the "Login" tab
   - Enter your username and password
   - Click "Login"

### Managing Businesses

#### Create a New Business

1. After logging in, click the "➕ New Business" button in the top bar
2. Enter the business name (e.g., "ABC Consulting Ltd")
3. Enter the business type (e.g., "Limited Company", "Sole Trader")
4. The business will be created and automatically selected

#### Switch Between Businesses

1. Use the "Business" dropdown in the top bar
2. Select the business you want to work with
3. All tax calculations and transactions will be scoped to the selected business

### Importing Bank Transactions

#### Upload CSV File

1. Navigate to the "🇬🇧 UK Tax Computations" tab
2. Expand the "🏦 Bank Transaction Upload & Categorization" section
3. Click the upload area or drag and drop your CSV file
4. The system will parse and categorize transactions automatically

#### CSV Format

Your bank statement CSV should include at least these columns:
```csv
date,description,amount
2024-01-15,Customer payment - ABC Corp,5000.00
2024-01-16,Rent payment to landlord,-1500.00
2024-01-17,Office supplies,-120.00
```

**Supported Formats:**
- **Option 1**: `date,description,amount`
- **Option 2**: `date,description,debit,credit`
- **Option 3**: `date,reference,description,amount`

**Date Formats:**
- `YYYY-MM-DD` (2024-01-15)
- `DD/MM/YYYY` (15/01/2024)
- `DD-MM-YYYY` (15-01-2024)

#### Transaction Categories

Transactions are automatically categorized into:

**Income Categories:**
- Sales
- Service Revenue
- Interest Income
- Other Income

**Expense Categories:**
- Rent
- Utilities
- Salaries
- Insurance
- Office Supplies
- Professional Fees
- Travel
- Marketing
- Equipment
- Other Expenses

**Tax Categories:**
- VAT Payment
- PAYE
- Corporation Tax
- Self Assessment

#### Apply to Tax Calculations

1. After uploading transactions, review the summary
2. Click "Apply to Tax Calculations"
3. The system will automatically populate relevant tax forms with transaction data
4. Review and adjust values as needed

## Using Tax Computation Features

### Self-Assessment Tax

1. Navigate to the "Self-Assessment Tax" section
2. If you've imported bank transactions, income and expenses will be pre-filled
3. Adjust values and add additional income sources
4. Click "Calculate Tax" to see your tax liability

### VAT Calculations

1. Use imported transactions to calculate VAT
2. The system separates sales and purchases
3. Generate VAT return summaries

### Corporate Tax

1. Import transactions to populate turnover and expenses
2. Calculate corporation tax based on business profits
3. Account for capital allowances and other adjustments

## Data Storage

### Local Storage
- All user data is stored in browser localStorage
- Data persists between sessions
- Each user's data is isolated and secure

### Session Management
- Sessions expire after 24 hours
- Logout clears your session
- Multiple tabs can share the same session

## Best Practices

### Transaction Import

1. **Regular Imports**: Import transactions monthly for accurate tax tracking
2. **Review Categories**: Check auto-categorization and adjust if needed
3. **Backup Data**: Export important calculations before clearing data

### Business Management

1. **Separate Businesses**: Keep each business's data separate
2. **Descriptive Names**: Use clear business names for easy identification
3. **Tax Settings**: Configure tax year and VAT registration per business

### Security

1. **Strong Passwords**: Use unique, strong passwords
2. **Logout**: Always logout when using shared computers
3. **Data Privacy**: Data is stored locally in your browser

## Transaction Categorization Rules

The system uses keyword matching to categorize transactions:

**Income Keywords:**
- payment, deposit, transfer in, credit, invoice, sale
- interest, dividend

**Expense Keywords:**
- rent, lease, landlord
- electric, gas, water, utility
- salary, wage, payroll, paye
- insurance, policy
- stationery, supplies, office
- accountant, lawyer, consultant, professional
- travel, hotel, flight, train, taxi
- advertising, marketing, promotion
- equipment, computer, software

**Tax Keywords:**
- vat, value added tax
- corporation tax, ct600
- self assessment

## Troubleshooting

### Cannot Upload CSV
- **Check Format**: Ensure CSV has required columns (date, description, amount)
- **Check Business**: Verify a business is selected in the dropdown
- **File Type**: Only CSV files are supported

### Login Issues
- **Check Credentials**: Verify username and password
- **Session Expired**: Try logging in again
- **Clear Browser Data**: Clear localStorage if persistent issues

### Missing Data
- **Select Business**: Ensure correct business is selected
- **Check Imports**: Verify transactions were imported successfully
- **Refresh Page**: Try refreshing the browser

## API Integration (For Developers)

### JavaScript API Client

The application includes a JavaScript API client (`frontend/api-client.js`) that provides:

```javascript
// Authentication
taxCalcAPI.register(username, password, email, fullName)
taxCalcAPI.login(username, password)
taxCalcAPI.logout()
taxCalcAPI.validateSession()

// Business Management
taxCalcAPI.createBusiness(name, businessType, taxNumber, address)
taxCalcAPI.getUserBusinesses()
taxCalcAPI.getBusiness(businessId)

// Transactions
taxCalcAPI.uploadBankTransactions(businessId, csvContent)
taxCalcAPI.getTransactions(businessId, startDate, endDate, category)
```

### Backend Services

Python backend services are available in the `backend/` directory:

- `auth.py` - User authentication and session management
- `business_manager.py` - Business entity management
- `bank_transactions.py` - CSV parsing and categorization
- `api.py` - Main API integration layer

## Example Workflows

### Workflow 1: New User Setup

1. Register account → Login
2. Create first business
3. Upload bank statements
4. Calculate taxes
5. Review and approve

### Workflow 2: Multiple Businesses

1. Login to existing account
2. Create second business (➕ New Business)
3. Switch between businesses in dropdown
4. Import separate bank statements for each
5. Calculate taxes independently

### Workflow 3: Monthly Tax Review

1. Login and select business
2. Upload current month's bank statement
3. Review transaction categorization
4. Apply to tax calculations
5. Generate tax computation reports
6. Save/export results

## Support

For issues or questions:
1. Check this user guide
2. Review the troubleshooting section
3. Check browser console for error messages
4. Ensure JavaScript is enabled in your browser

## Technical Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- LocalStorage enabled
- CSV files in supported format

## Updates and Changes

### Version 2.0 Features
- ✅ Multi-user authentication
- ✅ Multi-business support
- ✅ Bank transaction CSV import
- ✅ Automatic transaction categorization
- ✅ Business-scoped tax calculations
- ✅ Session management
- ✅ User-friendly interface

---

For more information, see the README files in the repository.
