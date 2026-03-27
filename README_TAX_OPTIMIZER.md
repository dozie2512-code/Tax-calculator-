# UK Tax Optimization Calculator

A comprehensive tax optimization tool for UK taxpayers that provides personalized tax-saving recommendations for different user types including Company Directors, Sole Traders, Company Owners, and Landlords.

## 🎯 Features

### User Types Supported
- **Company Directors**: Optimize salary vs dividends, pension contributions
- **Sole Traders**: Maximize expense claims, capital allowances, pension relief
- **Company Owners**: Corporation tax planning, R&D relief, profit extraction strategies
- **Landlords**: Property allowances, mortgage interest relief, incorporation analysis

### Key Capabilities
- ✅ Real-time tax calculations based on HMRC 2025/2026 rates
- ✅ Personalized optimization recommendations
- ✅ Comparison of current vs optimal tax positions
- ✅ Potential tax savings calculations
- ✅ Modern, responsive UI with TailwindCSS
- ✅ RESTful API backend with Flask
- ✅ Comprehensive input validation

## 📸 Screenshots

### Homepage with User Selection
![Tax Optimizer Homepage](https://github.com/user-attachments/assets/f21239c7-7512-4725-a6da-09eaa1965eb7)

### Results with Recommendations
![Tax Optimizer Results](https://github.com/user-attachments/assets/41f9a03e-9bdd-47ef-88d3-31a2e913fcd3)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Tax-calculator-
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

1. **Start the Flask API backend**
```bash
python backend/api.py
```

The API will start on `http://localhost:5000`

You should see:
```
============================================================
Starting Tax Optimization API...
============================================================

Available endpoints:
  - POST /api/optimize/director
  - POST /api/optimize/sole-trader
  - POST /api/optimize/company-owner
  - POST /api/optimize/landlord
  - GET  /api/health

Server running on: http://localhost:5000
============================================================
```

2. **Open the frontend in your browser**

Open the file in your browser:
```bash
# On macOS
open frontend/tax_optimizer.html

# On Linux
xdg-open frontend/tax_optimizer.html

# On Windows
start frontend/tax_optimizer.html

# Or navigate directly to:
# file:///path/to/Tax-calculator-/frontend/tax_optimizer.html
```

**Note**: For full functionality including API calls, it's recommended to serve the frontend through a web server:

```bash
# Serve frontend on port 8000
cd frontend
python -m http.server 8000

# Then open: http://localhost:8000/tax_optimizer.html
```

## 📁 Project Structure

```
Tax-calculator-/
├── backend/
│   ├── api.py                      # Flask REST API
│   ├── uk_tax_calculator.py        # Tax calculation engine
│   ├── tax_optimization_engine.py  # Optimization strategies
│   ├── utils.py                    # Utility functions
│   ├── accruals.py                 # Accrual calculations
│   ├── financial_statements.py     # Financial statements
│   └── reconciliation.py           # Account reconciliation
├── frontend/
│   ├── tax_optimizer.html          # Main tax optimization UI
│   ├── js/
│   │   └── optimizer.js            # Tax optimization logic & API calls
│   ├── css/
│   │   └── styles.css              # Custom styles
│   └── dashboard.html              # Month-end close dashboard
├── sample_data/                    # Sample data files
├── requirements.txt                # Python dependencies
├── README.md                       # Main documentation
└── README_TAX_OPTIMIZER.md         # This file
```

## 🔧 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Company Director Optimization
```
POST /api/optimize/director
```

**Request Body:**
```json
{
  "salary": 30000.00,
  "dividends": 20000.00,
  "company_profit": 60000.00,
  "pension_contribution": 5000.00
}
```

**Response:**
```json
{
  "user_type": "Company Director",
  "current_position": {
    "salary": 30000.00,
    "dividends": 20000.00,
    "total_tax": 21686.65,
    "net_income": 40463.35
  },
  "optimal_position": {
    "salary": 12570.00,
    "dividends": 38418.30,
    "total_tax": 18664.93,
    "net_income": 44473.37
  },
  "potential_saving": 3021.72,
  "recommendations": [...]
}
```

#### 2. Sole Trader Optimization
```
POST /api/optimize/sole-trader
```

**Request Body:**
```json
{
  "trading_income": 50000.00,
  "allowable_expenses": 8000.00,
  "pension_contribution": 3000.00,
  "capital_allowances": 2000.00
}
```

#### 3. Company Owner Optimization
```
POST /api/optimize/company-owner
```

**Request Body:**
```json
{
  "company_profit": 100000.00,
  "salary": 30000.00,
  "dividends": 40000.00,
  "r_and_d_expenditure": 15000.00,
  "capital_investment": 20000.00
}
```

#### 4. Landlord Optimization
```
POST /api/optimize/landlord
```

**Request Body:**
```json
{
  "rental_income": 30000.00,
  "mortgage_interest": 8000.00,
  "other_expenses": 5000.00,
  "is_furnished": true,
  "number_of_properties": 2
}
```

#### 5. Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Tax Optimization API is running",
  "version": "1.0.0"
}
```

## 💡 Usage Examples

### Example 1: Company Director

**Scenario:**
- Current salary: £30,000
- Dividends: £20,000
- Company profit: £60,000

**Recommendation:**
- Optimal salary: £12,570 (personal allowance)
- Optimal dividends: £38,418
- Potential saving: £3,022

### Example 2: Sole Trader

**Scenario:**
- Trading income: £50,000
- Expenses: £8,000
- Pension contribution: £3,000

**Recommendation:**
- Claim all allowable expenses
- Consider Annual Investment Allowance
- Maximize pension contributions
- Potential relief: £1,350+

### Example 3: Landlord

**Scenario:**
- Rental income: £30,000
- Mortgage interest: £8,000
- Other expenses: £5,000
- 2 properties, furnished

**Recommendation:**
- Utilize replacement of domestic items relief
- Consider incorporation (potential saving: £2,500)
- Joint ownership with spouse

## 📊 Tax Calculations

The calculator uses HMRC 2025/2026 tax rates (illustrative):

### Income Tax
- Personal Allowance: £12,570
- Basic Rate (20%): £12,571 to £50,270
- Higher Rate (40%): £50,271 to £150,000
- Additional Rate (45%): Over £150,000

### National Insurance
- Primary Threshold: £12,570
- Upper Earnings Limit: £50,270
- Rate below UEL: 8%
- Rate above UEL: 2%

### Corporation Tax
- Small Profits Rate (19%): Up to £50,000
- Main Rate (25%): Over £250,000
- Marginal relief: £50,000 to £250,000

### Dividend Tax
- Dividend Allowance: £500
- Basic Rate: 8.75%
- Higher Rate: 33.75%
- Additional Rate: 39.35%

## 🎨 Frontend Features

### User Experience
- **User Type Selection**: Visual cards for easy selection
- **Dynamic Forms**: Context-specific input fields
- **Input Validation**: Client-side validation with helpful error messages
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Results**: Instant display of optimization recommendations
- **Visual Comparisons**: Side-by-side current vs optimal positions

### Technology Stack
- **HTML5**: Semantic markup
- **TailwindCSS**: Modern, responsive styling via CDN
- **JavaScript (ES6)**: Vanilla JS for API interactions
- **Font Awesome**: Icon library for visual elements

## 🔒 Security Considerations

⚠️ **Important**: This is a demonstration/prototype application.

For production use, consider:
- [ ] Add authentication and authorization
- [ ] Implement rate limiting
- [ ] Use HTTPS for API communication
- [ ] Add input sanitization
- [ ] Implement logging and monitoring
- [ ] Add data persistence (database)
- [ ] Use environment variables for configuration
- [ ] Implement CSRF protection
- [ ] Add API key authentication

## 🧪 Testing

### Testing the API with curl

```bash
# Test health check
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
```

### Testing with Sample Scenarios

The frontend includes preset scenarios for each user type:

- **Director**: Earning £30,000 salary + £20,000 dividends
- **Sole Trader**: £50,000 trading income with £8,000 expenses
- **Company Owner**: £100,000 profit with R&D expenditure
- **Landlord**: £30,000 rental income with 2 furnished properties

## 🐛 Troubleshooting

### API Connection Error
**Problem**: "Unable to connect to the server"

**Solution**:
1. Ensure Flask API is running: `python backend/api.py`
2. Check the API is on port 5000: `curl http://localhost:5000/api/health`
3. Verify no firewall blocking port 5000

### Import Error
**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install -r requirements.txt
```

### CORS Error
**Problem**: Browser blocks API requests

**Solution**: Flask-CORS is configured in `api.py`. If still having issues, ensure you're accessing the frontend through a web server (not `file://` protocol).

### CDN Resources Blocked
**Problem**: TailwindCSS or Font Awesome not loading

**Solution**: Check your network/firewall settings. CDN resources require internet access.

## ⚖️ Tax Disclaimer

⚠️ **Important Legal Notice**:

This calculator provides **illustrative guidance only** based on 2025/2026 tax rates and is **not official tax advice**.

- Tax calculations are simplified and may not cover all scenarios
- Actual tax liability depends on individual circumstances
- Tax laws and rates change regularly
- Always consult with a qualified tax advisor or accountant for official advice
- Not verified by HMRC or any tax authority

## 🔮 Future Enhancements

Planned features:
- [ ] Save and load tax scenarios
- [ ] Multi-year tax planning
- [ ] Export reports to PDF
- [ ] Integration with accounting software
- [ ] Real-time HMRC rate updates
- [ ] User accounts and history
- [ ] Advanced tax scenarios (e.g., multiple income sources)
- [ ] Mobile app version
- [ ] Tax deadline reminders
- [ ] Historical tax comparison

## 🤝 Contributing

This is a demonstration project. To extend it:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This is a demonstration project. Check with the repository owner for licensing information.

## 📧 Support

For questions or issues:
1. Check this README for common solutions
2. Review the code comments for implementation details
3. Test with the provided examples
4. Ensure all dependencies are installed

## 🙏 Acknowledgments

- HMRC for tax rate information
- Flask and Flask-CORS communities
- TailwindCSS for styling framework
- Font Awesome for icon library

---

**Built with**: Python 3, Flask, TailwindCSS, JavaScript (ES6)

**Last Updated**: January 2025
