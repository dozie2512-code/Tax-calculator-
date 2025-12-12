# Nigeria Tax Calculator 2026

A client-side tax calculator for Nigeria implementing VAT, WHT, PAYE/PIT, and CIT calculations based on the Nigeria Tax Act changes effective January 1, 2026.

## 🚀 Features

- **VAT Calculator**: Calculate Value Added Tax with support for taxable, exempt, and zero-rated categories (7.5% standard rate)
- **WHT Calculator**: Withholding Tax for contracts, rent, dividends, interest, royalties, and management fees
- **PAYE/PIT Calculator**: Personal income tax with 2026 tax bands and reliefs
- **CIT Calculator**: Company Income Tax with small company exemption and development levy
- **Privacy-First**: All calculations performed client-side - no data transmitted or stored
- **CSV Export**: Download your calculations for record-keeping
- **Mobile-Friendly**: Responsive design works on all devices
- **Example Scenarios**: Pre-filled examples to validate calculations

## 📋 How to Use

1. **Access the Calculator**:
   - Open `index.html` in your browser
   - Click the "🇳🇬 Nigeria Tax Calculator 2026" link in the header
   - Or directly open `tax-calculator.html` in your browser

2. **Calculate Taxes**:
   - **VAT**: Enter transaction amount, select item category, optionally add input VAT
   - **WHT**: Enter payment amount and select payment type (or use custom rate)
   - **PAYE**: Enter annual gross salary, allowances, and configure pension/NHF contributions
   - **CIT**: Enter revenue, expenses, turnover, and toggle development levy if applicable

3. **View Results**:
   - Each calculator displays a detailed breakdown
   - Results include explanations of how tax is calculated
   - All amounts rounded to nearest Naira (₦)

4. **Export Data**:
   - Click "Download CSV" to export all calculations
   - CSV includes inputs, outputs, and disclaimer

## 📊 Example Scenarios

### VAT Example
- **Input**: Transaction Amount = ₦1,000,000, Category = Taxable, Input VAT = ₦50,000
- **Expected Output**: VAT Charged = ₦75,000, Net VAT Payable = ₦25,000, Total = ₦1,075,000

### WHT Example
- **Input**: Payment Amount = ₦500,000, Type = Rent (10%)
- **Expected Output**: WHT Deducted = ₦50,000, Net Payment = ₦450,000

### PAYE Example
- **Input**: Gross Salary = ₦6,000,000, Allowances = ₦1,200,000, Pension = 8%, NHF = Yes
- **Expected Output**: 
  - Total Income = ₦7,200,000
  - Pension = ₦480,000
  - NHF = ₦150,000
  - Taxable Income = ₦6,570,000
  - Annual Tax ≈ ₦1,006,650
  - Monthly Net ≈ ₦516,113

### CIT Example
- **Input**: Revenue = ₦50,000,000, Expenses = ₦30,000,000, Turnover = ₦50,000,000
- **Expected Output**: 
  - Taxable Profit = ₦20,000,000
  - Small Company Status = Yes (Exempt)
  - CIT = ₦0
  - Net Profit = ₦20,000,000

## 🧮 Tax Rates & Rules (2026)

### VAT (Value Added Tax)
- **Standard Rate**: 7.5% on taxable supplies
- **Exempt**: 0% (basic food items, medical services, educational services)
- **Zero-rated**: 0% (exports, goods in commercial quantities)

### WHT (Withholding Tax) - Default Rates
- **Contracts**: 5%
- **Rent**: 10%
- **Dividends**: 10%
- **Interest**: 10%
- **Royalties**: 10%
- **Management/Consultancy Fees**: 10%

### PAYE / PIT (Personal Income Tax) - 2026 Bands
| Income Band (₦) | Rate |
|----------------|------|
| 0 - 800,000 | 0% |
| 800,001 - 3,000,000 | 15% |
| 3,000,001 - 12,000,000 | 18% |
| 12,000,001 - 25,000,000 | 21% |
| 25,000,001 - 50,000,000 | 23% |
| Above 50,000,000 | 25% |

**Deductions**:
- Employee pension contribution (default 8%)
- National Housing Fund (NHF) - 2.5% of basic salary
- Life insurance premiums
- National Health Insurance Scheme (NHIS)

### CIT (Company Income Tax)
- **Standard Rate**: 30% on taxable profits
- **Small Company Exemption**: Companies with turnover ≤ ₦100,000,000 may be exempt (0%)
- **Development Levy**: 4% (optional toggle, applies to certain companies)
- **Calculation**: CIT = (Revenue - Allowable Expenses) × Rate

## 🔄 Rounding Rules

All calculations round to the **nearest Naira (₦)**. This means:
- ₦0.50 and above rounds up
- Below ₦0.50 rounds down
- Example: ₦1,234.56 → ₦1,235

## ⚠️ Important Disclaimer

**ESTIMATES ONLY — NOT TAX OR LEGAL ADVICE**

This calculator provides estimates based on publicly available advisory summaries and general interpretations of the Nigeria Tax Act 2026. 

- Tax obligations depend on individual circumstances
- Rates and rules may vary based on specific situations
- This tool is for informational purposes only
- **Always consult** with a qualified tax professional or the Nigeria Revenue Service for official guidance
- The developers assume no liability for decisions made based on these calculations

## 📚 Sources & References

This calculator is based on advisory summaries from:

- **PwC Nigeria**: [Tax Publications](https://www.pwc.com/ng/en/publications.html)
- **EY Nigeria**: [Tax Alerts](https://www.ey.com/en_ng)
- **Forvis Mazars**: Tax advisory summaries
- **AfricaCheck**: [Fact-checking resource](https://africacheck.org/)
- **Federal Inland Revenue Service (FIRS)**: [Official Tax Authority](https://www.firs.gov.ng/)

**Verification**: Users should verify all calculations with official Nigeria Revenue Service publications and consult tax professionals for compliance.

## 🔒 Privacy & Security

- ✅ **100% Client-Side**: All calculations performed in your browser
- ✅ **No Data Transmission**: Nothing sent to external servers
- ✅ **No Storage**: No data stored or tracked
- ✅ **No Cookies**: No tracking or analytics
- ✅ **Open Source**: Code is transparent and auditable

## 💻 Technical Details

- **Single-File HTML Application**: Self-contained with embedded CSS and JavaScript
- **No Dependencies**: Works offline, no external libraries required
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Responsive Design**: Mobile and desktop friendly
- **Accessibility**: Basic ARIA attributes for screen readers

## 📄 Files

- `tax-calculator.html` - Main tax calculator application
- `index.html` - Demo page with link to tax calculator
- `README.md` - This documentation file

## 🤝 Contributing

This is a simple client-side tool. To suggest improvements:
1. Review the calculation logic in `tax-calculator.html`
2. Verify against official FIRS publications
3. Submit issues or pull requests with references to official sources

## 📅 Version

- **Version**: 1.0.0
- **Effective Date**: January 1, 2026
- **Last Updated**: December 2025

---

**Note**: Tax laws change frequently. Verify current rates and rules with the [Federal Inland Revenue Service (FIRS)](https://www.firs.gov.ng/) before making any financial decisions.
