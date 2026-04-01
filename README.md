# Tax Calculator with Xero Integration & HMRC Rules

A comprehensive tax calculator for UK taxpayers with real-time accounting software integration and intelligent tax optimization.

## 🎯 Features

### Tax Computation
- ✅ **Multi-Entity Support**: Sole traders, limited companies, landlords, and employees
- ✅ **UK HMRC Rules 2024/25**: Complete implementation of current tax rates and allowances
- ✅ **Smart Optimization**: AI-powered tax savings suggestions
- ✅ **Allowable Expenses**: Comprehensive expense guides for each entity type
- ✅ **Real-time Calculations**: Instant tax computations with detailed breakdowns

### Data Integration
- ✅ **Xero API Integration**: Seamless connection to Xero accounting software
- ✅ **Real-time Sync**: Automatic data synchronization for invoices and expenses
- ✅ **Error Handling**: Robust error recovery and retry mechanisms
- ✅ **Multiple Formats**: Export to JSON and CSV

### User Interface
- ✅ **Modern Design**: Clean, responsive interface
- ✅ **Entity-Specific Forms**: Customized inputs for each taxpayer type
- ✅ **Interactive Dashboard**: Visual financial overview
- ✅ **Tax Rules Reference**: Built-in HMRC rules and rates guide

### Quality & Reliability
- ✅ **Comprehensive Testing**: 22 unit tests with 100% pass rate
- ✅ **Zero Dependencies**: Uses Python standard library only
- ✅ **Well Documented**: Complete API and usage documentation
- ✅ **Production Ready**: Modular architecture for easy deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/dozie2512-code/Tax-calculator-.git
cd Tax-calculator-
```

2. **No additional setup required!** All Python modules use standard library only.

### Usage

#### Option 1: Use the Web Interface (Recommended)

Simply open `index.html` in your web browser:

```bash
# On Linux/Mac
open index.html

# On Windows
start index.html

# Or navigate to the file directly
```

The interface provides:
- Tax calculator for all entity types
- Invoice and expense management
- Real-time tax calculations
- HMRC rules reference

#### Option 2: Use the Backend API

1. **Start the API server:**

```bash
python backend/api_server.py 8080
```

2. **Access API endpoints:**

```bash
# Health check
curl http://localhost:8080/api/health

# Get tax optimization (example)
curl -X POST http://localhost:8080/api/tax/optimize \
  -H "Content-Type: application/json" \
  -d '{"entity_type":"sole_trader","income":60000,"expenses":8000}'
```

#### Option 3: Use Python Modules Directly

```python
from backend.tax_optimizer import TaxOptimizer

optimizer = TaxOptimizer()

# Calculate tax for sole trader
result = optimizer.optimize_sole_trader(
    income=60000,
    expenses=10000
)

print(f"Profit: £{result['current_profit']}")
for suggestion in result['suggestions']:
    print(f"- {suggestion['title']}: {suggestion['description']}")
```

## 📊 Supported Entity Types

### 1. Sole Trader / Self-Employed
- Income tax calculation
- Class 2 and Class 4 National Insurance
- Trading allowance (£1,000)
- Pension relief optimization
- VAT threshold monitoring

### 2. Limited Company
- Corporation tax (19-25%)
- Optimal salary/dividend mix
- Employer pension contributions
- Marginal relief calculations
- Tax-efficient profit extraction

### 3. Landlord / Property Owner
- Rental income tax
- Property allowance (£1,000)
- Mortgage interest restriction (20% credit)
- Capital gains tax on property sales
- Expense optimization

### 4. Employee (PAYE)
- Income tax and Class 1 NI
- Salary sacrifice benefits
- Marriage allowance transfer
- Student loan repayments
- Personal allowance tapering

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python tests/test_backend.py

# Test individual modules
python backend/xero_api.py
python backend/tax_optimizer.py
```

**Test Results:**
```
============================================================
Running Tax Calculator Backend Tests
============================================================

Ran 22 tests in 0.001s

OK

Tests run: 22
Successes: 22
Failures: 0
Errors: 0
```

## 📖 Documentation

- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)**: Complete technical documentation
- **[Month-End Close](README_MONTH_END_CLOSE.md)**: Accounting automation features
- **[API Reference](IMPLEMENTATION_GUIDE.md#api-endpoints)**: RESTful API documentation
- **Code Documentation**: All modules have comprehensive docstrings

## 🔧 Configuration

### Xero API Setup (Optional)

To connect to your Xero account:

1. **Create Xero app** at [https://developer.xero.com](https://developer.xero.com)

2. **Set environment variables:**
```bash
export XERO_CLIENT_ID="your_client_id"
export XERO_CLIENT_SECRET="your_client_secret"
```

3. **Connect via UI** or **API:**
```bash
curl -X POST http://localhost:8080/api/xero/connect \
  -H "Content-Type: application/json" \
  -d '{"client_id":"YOUR_ID","client_secret":"YOUR_SECRET"}'
```

### Customization

Modify tax rules in `backend/tax_optimizer.py`:

```python
@dataclass
class TaxRules:
    personal_allowance: float = 12570
    basic_rate: float = 0.20
    # ... customize as needed
```

## 📁 Project Structure

```
Tax-calculator-/
├── backend/
│   ├── xero_api.py              # Xero API integration
│   ├── tax_optimizer.py         # Tax calculation engine
│   ├── api_server.py            # HTTP API server
│   ├── accruals.py              # Accrual calculations
│   ├── reconciliation.py        # Account reconciliation
│   ├── financial_statements.py # Statement generation
│   └── utils.py                 # Utility functions
├── frontend/
│   └── dashboard.html           # Approval workflow UI
├── tests/
│   └── test_backend.py          # Unit tests
├── index.html                   # Main tax calculator UI
├── IMPLEMENTATION_GUIDE.md      # Technical documentation
└── README.md                    # This file
```

## 💡 Usage Examples

### Example 1: Basic Tax Calculation

```python
from backend.tax_optimizer import TaxOptimizer

optimizer = TaxOptimizer()

# Sole trader with £60k income, £10k expenses
result = optimizer.optimize_sole_trader(
    income=60000,
    expenses=10000
)

print(f"Trading Profit: £{result['current_profit']:,.2f}")
print(f"\nTax Optimization Suggestions:")
for suggestion in result['suggestions']:
    print(f"• {suggestion['title']}")
    print(f"  {suggestion['description']}")
    if suggestion['potential_saving'] > 0:
        print(f"  💰 Potential saving: £{suggestion['potential_saving']:,.2f}")
```

### Example 2: Company Tax Optimization

```python
# Limited company - optimize salary/dividend split
result = optimizer.optimize_company(
    profit=100000,
    salary=12570,  # Personal allowance
    dividends=40000
)

print(f"Company Profit: £{result['company_profit']:,.2f}")
print(f"Director Salary: £{result['director_salary']:,.2f}")
print(f"Dividends: £{result['dividends']:,.2f}")
```

### Example 3: Sync Data from Xero

```python
from backend.xero_api import XeroAPIClient, DataSyncManager

# Initialize client
client = XeroAPIClient(client_id="YOUR_ID", client_secret="YOUR_SECRET")

# Authenticate
auth_result = client.authenticate()
if auth_result['success']:
    # Sync all data
    sync_manager = DataSyncManager(client)
    result = sync_manager.sync_all(save_to_file=True)
    
    print(f"Synced {result['results']['invoices']['count']} invoices")
    print(f"Synced {result['results']['expenses']['count']} expenses")
```

### Example 4: API Integration

```javascript
// Frontend JavaScript - Get tax optimization
async function calculateTax() {
  const response = await fetch('http://localhost:8080/api/tax/optimize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      entity_type: 'sole_trader',
      income: 60000,
      expenses: 8000
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    console.log('Profit:', result.optimization.current_profit);
    console.log('Suggestions:', result.optimization.suggestions);
  }
}
```

## 🎓 Tax Rules Reference

### Income Tax Rates 2024/25

| Income Band | Rate |
|-------------|------|
| £0 - £12,570 (Personal Allowance) | 0% |
| £12,571 - £50,270 (Basic Rate) | 20% |
| £50,271 - £125,140 (Higher Rate) | 40% |
| Over £125,140 (Additional Rate) | 45% |

### National Insurance

**Employees (Class 1):**
- 12% on £12,570 - £50,270
- 2% on earnings over £50,270

**Self-Employed (Class 2 & 4):**
- Class 2: £3.45/week if profits over £6,725
- Class 4: 9% on £12,570 - £50,270, then 2%

### Corporation Tax

- 19% on profits up to £50,000
- 25% on profits over £250,000
- Marginal rate for £50,001 - £250,000

### Key Allowances

- **Trading Allowance**: £1,000
- **Property Allowance**: £1,000
- **Dividend Allowance**: £500
- **Pension Annual Allowance**: £60,000
- **CGT Annual Exemption**: £3,000
- **Marriage Allowance**: £1,260

## 🔒 Security

### Current Implementation
- OAuth2 authentication framework
- Secure token handling
- Input validation
- Error sanitization

### Production Recommendations
1. Enable HTTPS/TLS
2. Implement user authentication
3. Add rate limiting
4. Enable audit logging
5. Encrypt sensitive data
6. Regular security audits

## 🚧 Future Enhancements

### Planned Features
- [ ] QuickBooks integration
- [ ] Multi-year tax planning
- [ ] PDF report generation
- [ ] Mobile application
- [ ] MTD (Making Tax Digital) compliance
- [ ] Real-time HMRC API integration
- [ ] AI-powered expense categorization
- [ ] Tax deadline reminders

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Update documentation
5. Submit a pull request

## 📄 License

This project is provided for educational and demonstration purposes. Check with the repository owner for licensing information.

## 🆘 Support

- 📖 Read the [Implementation Guide](IMPLEMENTATION_GUIDE.md)
- 🐛 Report issues on GitHub
- 💬 Check code comments and docstrings
- 🧪 Run tests to verify functionality

## ⚠️ Disclaimer

This tool provides tax calculations based on HMRC rules but should not replace professional tax advice. Always consult with a qualified accountant or tax advisor for your specific situation.

**Tax rates and rules are for the 2024/25 tax year and subject to change.**

## 🌟 Highlights

- **Zero Dependencies**: Pure Python standard library
- **22 Tests**: 100% pass rate
- **Production Ready**: Modular, scalable architecture
- **Well Documented**: Comprehensive guides and examples
- **Modern UI**: Responsive, intuitive interface
- **Smart Optimization**: Intelligent tax savings suggestions

---

Made with ❤️ for UK taxpayers | [Report an Issue](https://github.com/dozie2512-code/Tax-calculator-/issues)
