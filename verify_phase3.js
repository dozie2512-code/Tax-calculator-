const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Check for Phase 3 functions
const requiredFunctions = [
    'exportToCSV',
    'exportToExcel',
    'exportToPDF',
    'handleCSVImport',
    'processCSVImport',
    'filterEntriesByDateRange',
    'formatDate',
    'downloadFile',
    'showColumnMappingUI',
    'confirmImport',
    'closeImportModal'
];

console.log('=== Phase 3 Function Check ===');
let allFound = true;
requiredFunctions.forEach(func => {
    if (html.includes('function ' + func)) {
        console.log('✓ Found:', func);
    } else {
        console.log('✗ Missing:', func);
        allFound = false;
    }
});

// Check for Phase 3 HTML elements
const requiredElements = [
    'exportDateFrom',
    'exportDateTo',
    'csvImportFileInput',
    'csvImportModal',
    'printableReport',
    'incomeDate',
    'expenseDate'
];

console.log('\n=== Phase 3 HTML Element Check ===');
requiredElements.forEach(elem => {
    if (html.includes('id="' + elem + '"')) {
        console.log('✓ Found element:', elem);
    } else {
        console.log('✗ Missing element:', elem);
        allFound = false;
    }
});

// Check for export buttons
console.log('\n=== Phase 3 Export Button Check ===');
const buttons = [
    'Export Full Ledger',
    'Export Income Summary',
    'Export Expenses Summary',
    'Export Tax Computation',
    'Export Annual Summary',
    'Export to Excel',
    'Export to PDF',
    'Import from CSV'
];

buttons.forEach(btn => {
    if (html.includes(btn)) {
        console.log('✓ Found button:', btn);
    } else {
        console.log('✗ Missing button:', btn);
        allFound = false;
    }
});

// Check for CSS styles
console.log('\n=== Phase 3 CSS Check ===');
const cssChecks = [
    'export-btn',
    'import-btn',
    'date-range-filter',
    'modal-overlay',
    'print-table'
];

cssChecks.forEach(css => {
    if (html.includes('.' + css)) {
        console.log('✓ Found CSS class:', css);
    } else {
        console.log('✗ Missing CSS class:', css);
        allFound = false;
    }
});

if (allFound) {
    console.log('\n✅ All Phase 3 components are present!');
    process.exit(0);
} else {
    console.log('\n❌ Some components are missing!');
    process.exit(1);
}
