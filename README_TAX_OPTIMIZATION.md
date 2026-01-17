# UK Tax Optimization Tool

A comprehensive web application for calculating and optimizing tax positions for different UK taxpayer categories.

## Features

- **Health Check Dashboard** - Real-time API status monitoring
- **Multiple Taxpayer Categories**:
  - Company Directors
  - Sole Traders
  - Company Owners
  - Landlords
- **Responsive Bootstrap UI** - Works on desktop, tablet, and mobile devices
- **Real-time Tax Calculations** - Instant results with detailed breakdowns
- **Tax Optimization Recommendations** - Personalized suggestions to reduce tax liability
- **Form Validation** - Comprehensive input validation with helpful error messages

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Tax-calculator-
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Company Director Tax Optimization

Calculate tax for company directors receiving salary and dividends:

- **Required Fields**: Salary, Dividends, Company Profit
- **Optional Fields**: Pension Contribution

### Sole Trader Tax Optimization

Calculate tax for self-employed individuals:

- **Required Fields**: Trading Income
- **Optional Fields**: Allowable Expenses, Pension Contribution, Capital Allowances

### Company Owner Tax Optimization

Calculate tax for business owners with complex structures:

- **Required Fields**: Company Profit, Salary, Dividends
- **Optional Fields**: R&D Expenditure, Capital Investment

### Landlord Tax Optimization

Calculate tax for property landlords:

- **Required Fields**: Rental Income
- **Optional Fields**: Mortgage Interest, Other Expenses, Number of Properties, Is Furnished

## API Endpoints

- `GET /api/health` - Check API status
- `POST /api/optimize/director` - Company director tax calculation
- `POST /api/optimize/sole-trader` - Sole trader tax calculation
- `POST /api/optimize/company-owner` - Company owner tax calculation
- `POST /api/optimize/landlord` - Landlord tax calculation

## Tax Rates & Allowances

The application uses UK tax rates and allowances for the 2023/2024 tax year:

- Personal Allowance: £12,570
- Basic Rate (20%): Up to £50,270
- Higher Rate (40%): £50,271 to £125,140
- Additional Rate (45%): Over £125,140
- Dividend Allowance: £1,000
- Corporation Tax Rate: 19%

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **API**: RESTful JSON API

## Project Structure

```
Tax-calculator-/
├── app.py                              # Flask application & API endpoints
├── backend/
│   └── tax_optimization_engine.py     # Tax calculation engine
├── index.html                          # Frontend UI
├── requirements.txt                    # Python dependencies
└── README_TAX_OPTIMIZATION.md         # This file
```

## Features Implemented

✅ Health check with real-time status display
✅ Four complete tax optimization forms
✅ Responsive Bootstrap layout with tabs
✅ Client-side form validation
✅ AJAX/Fetch API integration
✅ Loading indicators during API calls
✅ Detailed tax breakdown display
✅ Personalized tax optimization recommendations
✅ Error handling and user-friendly messages
✅ Currency formatting (GBP)
✅ Mobile-responsive design

## Future Enhancements

- User authentication and saved calculations
- Historical comparison of tax positions
- PDF report generation
- Email notifications
- Multiple tax year support
- Advanced tax planning scenarios
- Integration with accounting software

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions, please contact the development team.
