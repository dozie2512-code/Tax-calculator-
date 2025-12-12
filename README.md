# Nigeria Tax Calculator 2026 🇳🇬

A comprehensive client-side tax calculator for Nigerian taxes including VAT, WHT, PAYE/PIT, and CIT based on the Nigeria Tax Act changes effective January 1, 2026.

## 🚀 Features

- **VAT Calculator**: Calculate Value Added Tax at 7.5% standard rate
- **WHT Calculator**: Withholding Tax calculations for various payment types
- **PAYE/PIT Calculator**: Personal Income Tax with 2026 tax bands
- **CIT Calculator**: Companies Income Tax with small company exemptions
- **Client-Side Only**: All calculations happen in your browser - no data transmitted
- **Mobile-Friendly**: Responsive design works on all devices
- **CSV Export**: Export calculation results for record keeping

## 📖 How to Use

### Getting Started

1. Open `index.html` in your web browser to see the Leaflet ride demo
2. Click on "🇳🇬 Nigeria Tax Calculator 2026 →" link in the header
3. Or directly open `tax-calculator.html` in your browser

### VAT Calculator

1. Enter the transaction amount (base amount excluding VAT)
2. Select item category:
   - **Taxable**: Standard 7.5% VAT applies
   - **Exempt**: No VAT charged or claimable
   - **Zero-rated**: 0% VAT but input VAT is claimable
3. Optionally enter input VAT amount for purchases
4. Click "Calculate VAT" to see results

### WHT Calculator

1. Enter the gross payment amount
2. Select payment type (or choose custom rate):
   - Contracts: 5%
   - Rent: 10%
   - Dividends: 10%
   - Interest: 10%
   - Royalties: 10%
   - Management/Consultancy Fees: 10%
3. Select payer type (Company or Individual)
4. Click "Calculate WHT" to see results

### PAYE/PIT Calculator

1. Enter annual gross salary
2. Enter any taxable allowances
3. Set pension contribution rate (default 8%)
4. Check/uncheck NHF (National Housing Fund at 2.5%)
5. Enter any other permitted reliefs
6. Click "Calculate PAYE" to see tax breakdown by bands

**2026 Tax Bands:**
- ₦0 - ₦800,000: 0%
- ₦800,001 - ₦3,000,000: 15%
- ₦3,000,001 - ₦12,000,000: 18%
- ₦12,000,001 - ₦25,000,000: 21%
- ₦25,000,001 - ₦50,000,000: 23%
- Above ₦50,000,000: 25%

### CIT Calculator

1. Enter annual revenue
2. Enter allowable business expenses
3. Enter company turnover (for small company exemption check)
4. Check/uncheck Development Levy (4%)
5. Adjust CIT rate if needed (default 30%)
6. Click "Calculate CIT" to see results

**Small Company Exemption**: Companies with turnover ≤ ₦100,000,000 are treated as exempt (0% CIT).

## 💰 Rounding Rules

All monetary amounts are **rounded to the nearest Naira (₦)**. This follows standard Nigerian tax practice where fractions of Naira are rounded.

- Example: ₦1,234.56 → ₦1,235
- Example: ₦9,876.23 → ₦9,876

## 📊 Example Scenarios

### Example 1: VAT Calculation
**Input:**
- Transaction Amount: ₦100,000
- Category: Taxable
- Input VAT: ₦0

**Output:**
- VAT Charged: ₦7,500 (7.5%)
- Total Amount: ₦107,500
- Net VAT Payable: ₦7,500

### Example 2: WHT on Rent
**Input:**
- Payment Amount: ₦500,000
- Type: Rent (10%)
- Payer: Company

**Output:**
- WHT Amount: ₦50,000
- Net Payment: ₦450,000

### Example 3: PAYE Calculation
**Input:**
- Annual Gross Salary: ₦5,000,000
- Allowances: ₦0
- Pension: 8%
- NHF: Yes (2.5%)

**Output:**
- Pension Contribution: ₦400,000
- NHF Contribution: ₦125,000
- Taxable Income: ₦4,475,000
- Annual PAYE Tax: ₦595,500
- Monthly Net Income: ₦323,292

### Example 4: CIT for Small Company
**Input:**
- Revenue: ₦80,000,000
- Expenses: ₦50,000,000
- Turnover: ₦80,000,000
- Dev Levy: Yes

**Output:**
- Taxable Profit: ₦30,000,000
- CIT: ₦0 (Small company exemption)
- Development Levy: ₦1,200,000
- Net Profit: ₦28,800,000

## ⚠️ Important Disclaimer

**ESTIMATES ONLY — NOT TAX OR LEGAL ADVICE**

This calculator provides estimates based on publicly available advisory summaries of the Nigeria Tax Act 2025/2026. Results are for **informational purposes only** and should not be considered as:
- Official tax calculations
- Tax advice
- Legal advice
- A substitute for professional consultation

**Users must:**
- Verify all rates, thresholds, and calculations against official publications from the Federal Inland Revenue Service (FIRS)
- Consult qualified tax professionals before making tax decisions
- Confirm current tax laws with the official Nigeria gazette

## 🔒 Privacy & Security

**Client-Side Only — No Data Transmitted or Stored**

- All calculations are performed entirely in your browser using JavaScript
- No data is sent to any external server
- No cookies or tracking mechanisms are used
- No personal or financial information is collected or stored
- You can use this calculator offline (after initial page load)

## 📚 Sources & References

Default rates and bands are based on publicly available advisory summaries from reputable sources:

1. **PwC Nigeria Tax Summaries**  
   [https://taxsummaries.pwc.com/nigeria](https://taxsummaries.pwc.com/nigeria)

2. **EY Tax Alert Nigeria**  
   [https://www.ey.com/en_ng](https://www.ey.com/en_ng)

3. **Forvis Mazars Nigeria Tax Guide**  
   [https://www.mazars.ng/](https://www.mazars.ng/)

4. **AfricaCheck**  
   [https://africacheck.org/](https://africacheck.org/)

**Note**: Defaults reflect tax law and advisory summaries effective January 1, 2026. Users should verify with official gazette or Federal Inland Revenue Service (FIRS).

## 🛠️ Technical Details

### Technology Stack
- Pure HTML5, CSS3, and JavaScript (ES6+)
- No external dependencies or frameworks
- No build process required
- Works in all modern browsers

### Browser Compatibility
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

### Accessibility
- ARIA labels and roles for screen readers
- Keyboard navigation support
- Semantic HTML structure
- Clear focus indicators

## 📥 Export Functionality

The CIT calculator includes a CSV export feature that allows you to download calculation results for record keeping. The exported CSV includes:
- Calculation type and date
- All input values
- All calculated results
- Disclaimer notice

## 🧪 Testing

A test harness file (`tax-calculator-test.html`) is included with pre-filled scenarios to validate calculations.

## 📄 Files in This Repository

- `index.html` - Leaflet ride demo (existing)
- `tax-calculator.html` - Nigeria Tax Calculator 2026 (new)
- `tax-calculator-test.html` - Test scenarios (new)
- `README.md` - This documentation file

## 🤝 Contributing

This is a demonstration project. For production use, please:
1. Verify all tax rates with FIRS official publications
2. Add comprehensive test coverage
3. Consider backend validation for critical applications
4. Engage professional tax advisors for implementation

## 📜 License

This project maintains the same license as the parent repository.

## 🔄 Updates

**Version 1.0 (2025-12-12)**
- Initial release
- VAT, WHT, PAYE/PIT, and CIT calculators
- 2026 tax bands and rates
- Client-side calculations
- CSV export functionality

---

**Developed for demonstration purposes. Always consult with qualified tax professionals and verify with FIRS for official tax matters.**
