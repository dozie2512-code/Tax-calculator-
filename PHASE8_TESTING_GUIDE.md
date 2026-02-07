# Phase 8 Testing Guide

## Quick Start Testing

### Option 1: Using Test Suite (Recommended)
1. Open `test_phase8.html` in your browser
2. The main calculator will be embedded in an iframe
3. Follow the 20-point checklist
4. Complete the 4 manual test scenarios
5. Track your progress with the "Check Test Progress" button

### Option 2: Direct Testing
1. Open `index.html` in your browser
2. Add sample data (see test scenarios below)
3. Calculate tax
4. Verify HMRC Compliance section appears
5. Test each feature individually

---

## Detailed Test Scenarios

### Test Scenario 1: Basic Self-Employed Tax Calculation

**Setup:**
1. Open index.html
2. Select tax year: 2025/26
3. Select category: Sole Trader

**Add Income:**
- Date: 15/04/2025
- Description: "Freelance Work"
- Amount: £50,000
- Click "Add Income"

**Add Expenses:**
- Date: 20/04/2025
- Description: "Office Supplies"
- Amount: £5,000
- Click "Add Expense"

- Date: 25/04/2025
- Description: "Software Subscriptions"
- Amount: £2,000
- Click "Add Expense"

- Date: 30/04/2025
- Description: "Professional Fees"
- Amount: £8,000
- Click "Add Expense"

**Advanced Tax Settings:**
- Student Loan Plan: None
- Dividend Income: £0
- Savings Interest: £0

**Calculate Tax:**
- Click "Calculate Tax"

**Expected Results:**
1. **HMRC Tax Computation displays:**
   - Total Income: £50,000.00
   - Personal Allowance: (£12,570.00)
   - Trading Allowance: (£1,000.00)
   - Taxable Income: £36,430.00
   - Basic rate tax calculated
   - National Insurance calculated
   - Effective tax rate displayed

2. **Self Assessment Pre-Fill shows:**
   - Box 11.1: £50,000.00 (Turnover)
   - Box 11.2: £15,000.00 (Expenses)
   - Box 11.3: £35,000.00 (Net profit)

3. **Audit Trail shows:**
   - "Added income: Freelance Work - £50,000.00"
   - "Added expense: Office Supplies - £5,000.00"
   - "Added expense: Software Subscriptions - £2,000.00"
   - "Added expense: Professional Fees - £8,000.00"

---

### Test Scenario 2: VAT Registered Business

**Setup:**
1. Continue from Scenario 1 or start fresh
2. Add multiple transactions across different quarters

**Add Q1 Income (Apr-Jul):**
- 15/04/2025: "Sales Q1 - April", £8,000
- 20/05/2025: "Sales Q1 - May", £7,500
- 15/06/2025: "Sales Q1 - June", £8,500
- Total Q1 Income: £24,000

**Add Q1 Expenses:**
- 25/04/2025: "Supplies Q1", £2,000
- 30/05/2025: "Equipment Q1", £1,500
- Total Q1 Expenses: £3,500

**Add Q2 Income (Jul-Oct):**
- 20/07/2025: "Sales Q2 - July", £9,000
- 15/08/2025: "Sales Q2 - August", £8,000
- Total Q2 Income: £17,000

**Test VAT Return:**
1. Open "VAT Return (Making Tax Digital)" section
2. Select Quarter: Q1
3. Select VAT Rate: 20%
4. Click to update

**Expected Results for Q1:**
- Box 1 (VAT on sales): £4,800.00 (20% of £24,000)
- Box 2 (VAT on acquisitions): £0.00
- Box 3 (Total VAT due): £4,800.00
- Box 4 (VAT reclaimed): £700.00 (20% of £3,500)
- Box 5 (Net VAT): £4,100.00 (Box 3 - Box 4)
- Box 6 (Sales ex VAT): £24,000
- Box 7 (Purchases ex VAT): £3,500
- Box 8 (EU supplies): £0
- Box 9 (EU acquisitions): £0

**Test Copy Functionality:**
1. Click "Copy Values for MTD Submission"
2. Paste into text editor
3. Verify all 9 boxes copied correctly

**Test Quarter Change:**
1. Change quarter to Q2
2. Verify calculations update to show Q2 transactions only
3. Box 1 should show £3,400.00 (20% of £17,000)

---

### Test Scenario 3: Tax Deadlines Verification

**Open Section:**
1. Scroll to HMRC Compliance section
2. Open "Tax Deadlines & Calendar"

**Verify Deadlines:**
1. **Self Assessment section shows:**
   - Paper return: 31 October 2025
   - Online return: 31 January 2026
   - Payment: 31 January 2026
   - Days remaining calculated correctly
   - Status indicators correct (✓ for past, ⚠ for < 30 days, ○ for future)

2. **VAT Returns section shows:**
   - Q1 (6 Apr - 5 Jul): Due 7 Aug 2025
   - Q2 (6 Jul - 5 Oct): Due 7 Nov 2025
   - Q3 (6 Oct - 5 Jan): Due 7 Feb 2026
   - Q4 (6 Jan - 5 Apr): Due 7 May 2026
   - Each with correct status indicator

3. **Payments on Account:**
   - First payment: 31 January 2026
   - Second payment: 31 July 2026
   - Days remaining displayed

**Test Calculation:**
- Today's date: [Current date]
- 31 Jan 2026 - Today = X days
- Verify displayed days match calculation

---

### Test Scenario 4: Late Payment Penalty Calculator

**Open Section:**
1. Scroll to HMRC Compliance section
2. Open "Late Payment Penalty Calculator"

**Test Case 1: 44 Days Late**
1. Tax Due: £5,000
2. Due Date: 31/01/2026
3. Paid Date: 15/03/2026
4. Click "Calculate Penalties"

**Expected Results:**
- Days Late: 44
- Fixed Penalty (1-90 days): £100.00
- Interest: £5,000 × 0.075 × (44/365) = £45.21
- Total Additional: £145.21
- Total Amount Due: £5,145.21

**Test Case 2: 120 Days Late**
1. Tax Due: £10,000
2. Due Date: 31/01/2026
3. Paid Date: 30/05/2026
4. Click "Calculate Penalties"

**Expected Results:**
- Days Late: 120
- Fixed Penalty (1+ days): £100.00
- Daily Penalty (90+ days): 30 days × £10 = £300.00
- Total Penalty: £400.00
- Interest: £10,000 × 0.075 × (120/365) = £246.58
- Total Additional: £646.58
- Total Amount Due: £10,646.58

**Test Case 3: On Time Payment**
1. Tax Due: £3,000
2. Due Date: 31/01/2026
3. Paid Date: 31/01/2026
4. Click "Calculate Penalties"

**Expected Results:**
- Days Late: 0
- No penalty: £0.00
- No interest: £0.00
- Total Amount Due: £3,000.00

---

### Test Scenario 5: Audit Trail Testing

**Test Add Operation:**
1. Add new income: "Consulting Fee", £2,500
2. Open "Digital Record Audit Trail"
3. Verify entry appears: "Added income: Consulting Fee - £2,500.00"
4. Check timestamp is correct

**Test Edit Operation:**
1. Find the "Consulting Fee" entry in Income List
2. Click "Edit"
3. Change description to "Consulting Services"
4. Change amount to £2,750
5. Save changes
6. Refresh Audit Trail
7. Verify entry: "Edited income: Consulting Fee (£2,500.00) → Consulting Services (£2,750.00)"

**Test Delete Operation:**
1. Find the "Consulting Services" entry
2. Click "Delete"
3. Confirm deletion
4. Refresh Audit Trail
5. Verify entry: "Deleted income: Consulting Services - £2,750.00"

**Test Export:**
1. Click "Export Audit Log"
2. Verify CSV file downloads
3. Open CSV in spreadsheet software
4. Verify format: Timestamp, Action, Details
5. Verify all recent entries present

**Test Clear:**
1. Click "Clear Old Entries"
2. Confirm the action (clears entries > 90 days)
3. Verify audit trail shows: "Cleared X audit entries older than 90 days"

---

### Test Scenario 6: Advanced Tax with Dividends and Savings

**Setup:**
1. Start fresh or continue
2. Add base income: £40,000

**Advanced Tax Settings:**
1. Dividend Income: £5,000
2. Savings Interest: £2,000
3. Student Loan Plan: Plan 2 (£27,295 threshold @ 9%)

**Calculate Tax:**
1. Click "Calculate Tax"

**Verify HMRC Tax Computation:**
1. Income section shows:
   - Trading Income: £40,000.00
   - Dividend Income: £5,000.00
   - Savings Interest: £2,000.00
   - Total Income: £47,000.00

2. Tax Calculation shows:
   - Income Tax
   - Dividend Tax (after £500 allowance)
   - Savings Tax (after £1,000 allowance)
   - National Insurance
   - Student Loan Repayment

3. Student Loan Repayment:
   - Above threshold: £47,000 - £27,295 = £19,705
   - Repayment: £19,705 × 9% = £1,773.45

4. Effective tax rate calculated correctly

**Verify Self Assessment Pre-Fill:**
1. SA100 Dividends box shows: £5,000.00
2. SA100 Interest box shows: £2,000.00

---

## Quick Checklist

### Before Testing
- [ ] Browser supports localStorage
- [ ] JavaScript enabled
- [ ] No console errors on page load

### Feature Testing
- [ ] HMRC Tax Computation displays after Calculate Tax
- [ ] Computation shows all income sources
- [ ] Allowances calculated correctly
- [ ] Tax by bands displayed
- [ ] Effective tax rate shown
- [ ] Self Assessment boxes populated
- [ ] VAT Return quarter selector works
- [ ] VAT calculations correct for selected quarter
- [ ] Copy VAT data works
- [ ] Tax deadlines all displayed
- [ ] Days until deadline calculated
- [ ] Status indicators correct (✓ ⚠ ○)
- [ ] Penalty calculator accepts input
- [ ] Penalty calculations accurate
- [ ] Interest calculated at 7.5% annual
- [ ] Audit trail displays entries
- [ ] Add operations logged
- [ ] Edit operations logged with before/after
- [ ] Delete operations logged
- [ ] Export audit trail works
- [ ] Clear old entries works

### Visual Testing
- [ ] HMRC blue color (#005ea5) used throughout
- [ ] Monospace font for figures
- [ ] Clean, professional layout
- [ ] Sections collapsible/expandable
- [ ] Print-friendly formatting
- [ ] Status indicators color-coded correctly
- [ ] No layout issues on different screen sizes

### Data Integrity
- [ ] Calculations match manual verification
- [ ] Quarter filtering accurate
- [ ] Deadline dates correct for 2025/26
- [ ] Audit timestamps accurate
- [ ] Data persists after page reload
- [ ] No data loss on import/export

---

## Common Issues and Solutions

### Issue: HMRC section not appearing
**Solution:** Ensure you've clicked "Calculate Tax" first

### Issue: VAT Return shows zero values
**Solution:** Check that transactions exist for the selected quarter

### Issue: Audit Trail empty
**Solution:** Add, edit, or delete an entry to generate audit logs

### Issue: Deadlines showing wrong dates
**Solution:** Verify system date is correct; deadlines are for 2025/26 tax year

### Issue: Penalty calculator not working
**Solution:** Ensure all three fields (tax due, due date, paid date) are filled

### Issue: Copy button does nothing
**Solution:** Check browser supports Clipboard API; try manual copy

---

## Browser Testing

Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

Verify:
- [ ] All features work consistently
- [ ] Styling appears correctly
- [ ] No console errors
- [ ] localStorage works
- [ ] Copy functionality works

---

## Performance Testing

1. **Large Dataset Test:**
   - Add 100+ income entries
   - Add 100+ expense entries
   - Calculate tax
   - Verify performance is acceptable
   - Check audit trail displays correctly

2. **Audit Trail Test:**
   - Perform 50+ operations
   - Verify audit trail shows last 50
   - Export audit log
   - Verify all entries exported

3. **Quarter Filtering Test:**
   - Add entries across all 4 quarters
   - Switch between quarters in VAT Return
   - Verify filtering is fast
   - Verify calculations update correctly

---

## Final Verification

After completing all tests:
1. Export full data backup
2. Clear all data
3. Import backup
4. Verify all data restored correctly
5. Verify HMRC sections still work
6. Verify audit trail preserved

---

## Test Sign-Off

**Tester Name:** _______________  
**Date:** _______________  
**Browser:** _______________  
**Version:** _______________  

**Test Results:**
- [ ] All features working
- [ ] No critical issues
- [ ] Documentation accurate
- [ ] Ready for production

**Notes:**
_______________________________
_______________________________
_______________________________

---

## Support

For issues or questions:
1. Check PHASE8_IMPLEMENTATION_COMPLETE.md for feature details
2. Review PHASE8_SUMMARY.md for overview
3. Verify test steps followed correctly
4. Check browser console for errors
5. Test in different browser if issues persist
