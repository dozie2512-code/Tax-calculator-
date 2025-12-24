# 🇳🇬 Nigeria Tax Calculator 2026

A comprehensive, browser-based tax calculator for Nigerian tax obligations based on the Tax Act changes effective January 1, 2026.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

## 🎯 Features

### Tax Calculators

- **Value Added Tax (VAT)**: Calculate 7.5% VAT on taxable supplies with support for exempt and zero-rated items, plus input VAT recovery
- **Withholding Tax (WHT)**: Calculate WHT deductions for various payment types (contracts, rent, dividends, interest, royalties, etc.)
- **PAYE / Personal Income Tax (PIT)**: Calculate personal income tax using 2026 tax bands with pension, NHF, and other relief deductions
- **Company Income Tax (CIT)**: Calculate corporate income tax with small company exemption and optional 4% development levy

### User Experience

- 📋 **Example Scenarios**: Pre-filled examples for quick validation and learning
- 📥 **CSV Export**: Download all calculations for record-keeping
- 🔒 **Privacy First**: All calculations performed locally in your browser - no data transmitted
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- ⚡ **Real-time Calculations**: Instant results with detailed breakdowns

## 🚀 Getting Started

### Quick Start

1. **Download or Clone**
   ```bash
   git clone https://github.com/dozie2512-code/Tax-calculator-.git
   cd Tax-calculator-
   ```

2. **Open in Browser**
   - Simply open `index.html` in your web browser
   - No installation or build process required!

3. **Start Calculating**
   - Use the example scenarios to see the calculator in action
   - Enter your own values to calculate taxes

### Usage

#### VAT Calculator
1. Enter the transaction amount
2. Select item category (Taxable, Exempt, or Zero-rated)
3. Optionally enter input VAT for recovery calculation
4. Click "Calculate VAT" to see results

#### WHT Calculator
1. Enter the payment amount
2. Select payment type from dropdown or choose custom rate
3. Click "Calculate WHT" to see withholding tax and net payment

#### PAYE Calculator
1. Enter annual gross salary and allowances
2. Set pension contribution percentage (default 8%)
3. Enable/disable NHF deduction (2.5% of basic salary)
4. Enter other reliefs (life insurance, NHIS, etc.)
5. Click "Calculate PAYE" to see detailed tax breakdown

#### CIT Calculator
1. Enter annual business revenue
2. Enter allowable business expenses
3. Enter company turnover (for small company exemption check)
4. Optionally apply 4% development levy
5. Click "Calculate CIT" to see corporate tax

## 📊 2026 Tax Rates & Bands

### VAT
- Standard rate: **7.5%**
- Exempt items: **0%**
- Zero-rated items: **0%**

### WHT Rates
- Contracts: **5%**
- Rent: **10%**
- Dividends: **10%**
- Interest: **10%**
- Royalties: **10%**
- Management/Consultancy Fees: **10%**

### PAYE/PIT Bands (2026)
| Taxable Income Range | Tax Rate |
|---------------------|----------|
| ₦0 - ₦800,000 | 0% |
| ₦800,001 - ₦3,000,000 | 15% |
| ₦3,000,001 - ₦12,000,000 | 18% |
| ₦12,000,001 - ₦25,000,000 | 21% |
| ₦25,000,001 - ₦50,000,000 | 23% |
| Above ₦50,000,000 | 25% |

### CIT
- Standard rate: **30%**
- Small companies (turnover ≤ ₦100,000,000): **Exempt (0%)**
- Development levy: **4%** (optional/conditional)

## 🔧 Technical Details

### Technology Stack
- **Pure HTML5**: Semantic markup for accessibility
- **Pure CSS3**: Custom properties, flexbox, and grid layout
- **Vanilla JavaScript**: No frameworks or dependencies required

### Browser Support
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Opera (latest)

### Architecture
- **Client-side only**: No server required, works offline
- **Privacy-focused**: Zero data collection or external API calls
- **Lightweight**: Single HTML file (~38KB)
- **Fast**: Instant calculations with no network latency

## 📝 Example Calculations

### Example 1: VAT Calculation
**Input:**
- Transaction Amount: ₦1,000,000
- Category: Taxable (7.5% VAT)
- Input VAT: ₦50,000

**Output:**
- VAT Charged: ₦75,000
- Net VAT Payable: ₦25,000
- Total Amount: ₦1,075,000

### Example 2: PAYE Calculation
**Input:**
- Annual Gross Salary: ₦6,000,000
- Allowances: ₦1,200,000
- Pension: 8%
- NHF: Enabled

**Output:**
- Total Income: ₦7,200,000
- Taxable Income: ₦6,570,000
- Annual Tax: ₦972,600
- Monthly Net Income: ₦518,950

## ⚠️ Disclaimer

**This calculator provides estimates only and should not be considered tax or legal advice.**

Tax obligations depend on individual circumstances, and calculations are based on publicly available advisory summaries. Always consult with a qualified tax professional or the [Federal Inland Revenue Service (FIRS)](https://www.firs.gov.ng/) for official guidance.

## 📚 References

This calculator is based on tax information from:
- [PwC Nigeria](https://www.pwc.com/ng/en/publications.html)
- [EY Tax Alert](https://www.ey.com/en_ng)
- Forvis Mazars
- [AfricaCheck](https://africacheck.org/)

All calculations are effective January 1, 2026, and amounts are rounded to the nearest Naira (₦).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development
```bash
# Clone the repository
git clone https://github.com/dozie2512-code/Tax-calculator-.git

# Open index.html in your browser
# Make your changes
# Test thoroughly
# Submit a PR
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋 Support

If you encounter any issues or have questions:
1. Check the [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for detailed testing information
2. Open an issue on GitHub
3. Consult the references listed above for tax-specific questions

## 🌟 Acknowledgments

- Thanks to all tax advisory firms providing public guidance on Nigerian tax changes
- Built with ❤️ for the Nigerian business community

---

**Note**: Tax laws and rates are subject to change. Always verify calculations with the most current official sources.
