# Nigeria Tax Calculator 2026

## Overview

This repository contains a comprehensive web-based tax calculator for Nigeria, implementing the Tax Act changes effective January 1, 2026.

## Purpose of This PR

This Pull Request documents the current state of the `index.html` file, which contains a fully functional Nigeria Tax Calculator application. The PR serves to establish a baseline version of the calculator for future enhancements and modifications.

## Features

The calculator provides four main tax calculation modules:

### 1. Value Added Tax (VAT) Calculator
- Calculates VAT at 7.5% for taxable items
- Handles exempt and zero-rated items
- Supports input VAT for recoverable calculations
- Computes net VAT payable

### 2. Withholding Tax (WHT) Calculator
- Default rates for common payment types:
  - Contracts: 5%
  - Rent, Dividends, Interest, Royalties, Management/Consultancy Fees: 10%
- Custom rate option for specialized scenarios
- Calculates WHT deductions and net payments

### 3. PAYE / Personal Income Tax (PIT) Calculator
- Implements 2026 progressive tax bands:
  - ₦0 - ₦800,000: 0%
  - ₦800,000 - ₦3,000,000: 15%
  - ₦3,000,000 - ₦12,000,000: 18%
  - ₦12,000,000 - ₦25,000,000: 21%
  - ₦25,000,000 - ₦50,000,000: 23%
  - Above ₦50,000,000: 25%
- Includes pension contributions (default 8%)
- NHF (National Housing Fund) deduction (2.5%)
- Supports additional reliefs and deductions
- Provides monthly and annual breakdowns

### 4. Company Income Tax (CIT) Calculator
- Standard CIT rate: 30%
- Small company exemption (turnover ≤ ₦100,000,000)
- Optional 4% Development Levy
- Calculates taxable profit and effective tax rates

## Additional Features

### Pre-loaded Examples
The calculator includes example scenarios for each tax type to help users understand the calculations and validate results.

### Data Export
Users can export all calculation results to CSV format for record-keeping and further analysis.

### Privacy & Security
All calculations are performed entirely in the browser using JavaScript. No data is transmitted to external servers or stored remotely.

### Accessibility
The application includes:
- ARIA labels and roles for screen reader compatibility
- Semantic HTML structure
- Keyboard navigation support
- Clear form labels and help text

## Technical Implementation

- **Technology**: Pure HTML, CSS (referenced but not included), and vanilla JavaScript
- **Browser-based**: No server-side processing required
- **Self-contained**: Single HTML file with embedded JavaScript
- **Currency**: All amounts in Nigerian Naira (₦), rounded to nearest naira

## Disclaimer

This calculator provides estimates based on publicly available advisory summaries from:
- PwC Nigeria
- EY Tax Alert
- Forvis Mazars
- AfricaCheck

**Important**: These calculations are for informational purposes only and do not constitute tax or legal advice. Tax obligations depend on individual circumstances. Users should always consult with qualified tax professionals or the Nigeria Revenue Service for official guidance.

## Sources & References

Calculations are based on advisory summaries and should be verified with official [Nigeria Revenue Service (FIRS)](https://www.firs.gov.ng/) publications.

## File Structure

```
/
├── index.html          # Main tax calculator application (Nigeria Tax Calculator 2026)
├── Tax calculator      # Historical file containing chat conversation about a different calculator
└── README.md          # This documentation file
```

**Note**: The "Tax calculator" file contains historical content unrelated to the current Nigeria Tax Calculator application.

## Usage

To use the calculator:
1. Open `index.html` in any modern web browser
2. Select the tax type you want to calculate
3. Fill in the required fields
4. Click the "Calculate" button for that tax type
5. Review the results and breakdown
6. Optionally export results to CSV

## Future Enhancements

Potential areas for future development:
- Create a `styles.css` file (currently referenced but not present in the repository - the application functions but may benefit from external styling)
- Implement additional tax types
- Add more detailed explanations and examples
- Include tax planning scenarios
- Multi-language support
- Mobile app version

## Generic Intent of This PR

This Pull Request establishes the current state of the Nigeria Tax Calculator application as a documented baseline. It serves several purposes:

1. **Documentation**: Provides clear documentation of the calculator's features and capabilities
2. **Reference Point**: Creates a reference point for tracking future changes and enhancements
3. **Onboarding**: Helps new contributors understand the project structure and purpose
4. **Maintenance**: Facilitates easier maintenance by documenting the current implementation

The PR does not introduce new features or changes to the existing calculator functionality. It purely serves as a documentation and tracking milestone for the project.

---

**Last Updated**: December 24, 2025  
**Effective Tax Year**: 2026 (Nigeria)
