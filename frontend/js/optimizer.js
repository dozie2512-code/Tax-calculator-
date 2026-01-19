/**
 * Tax Optimizer JavaScript
 * Handles user interactions, API calls, and dynamic UI updates
 */

// API configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let currentUserType = null;
let currentResults = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupUserTypeSelection();
    setupFormSubmissions();
});

/**
 * Setup user type card selection
 */
function setupUserTypeSelection() {
    const userCards = document.querySelectorAll('.user-card');
    
    userCards.forEach(card => {
        card.addEventListener('click', function() {
            const userType = this.getAttribute('data-user-type');
            selectUserType(userType);
        });
    });
}

/**
 * Handle user type selection
 */
function selectUserType(userType) {
    currentUserType = userType;
    
    // Update card selection UI
    const userCards = document.querySelectorAll('.user-card');
    userCards.forEach(card => {
        if (card.getAttribute('data-user-type') === userType) {
            card.classList.add('active');
        } else {
            card.classList.remove('active');
        }
    });
    
    // Hide all forms
    hideAllForms();
    
    // Show appropriate form
    showForm(userType);
    
    // Show input section
    const inputSection = document.getElementById('inputSection');
    inputSection.classList.remove('hidden');
    
    // Scroll to form
    inputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Hide results
    hideResults();
    hideError();
}

/**
 * Hide all forms
 */
function hideAllForms() {
    document.getElementById('directorForm').classList.add('hidden');
    document.getElementById('soleTraderForm').classList.add('hidden');
    document.getElementById('companyOwnerForm').classList.add('hidden');
    document.getElementById('landlordForm').classList.add('hidden');
}

/**
 * Show specific form based on user type
 */
function showForm(userType) {
    let formId, formTitle;
    
    switch(userType) {
        case 'director':
            formId = 'directorForm';
            formTitle = 'Company Director - Enter Your Details';
            break;
        case 'sole-trader':
            formId = 'soleTraderForm';
            formTitle = 'Sole Trader - Enter Your Details';
            break;
        case 'company-owner':
            formId = 'companyOwnerForm';
            formTitle = 'Company Owner - Enter Your Details';
            break;
        case 'landlord':
            formId = 'landlordForm';
            formTitle = 'Landlord - Enter Your Details';
            break;
    }
    
    document.getElementById(formId).classList.remove('hidden');
    document.getElementById('formTitle').textContent = formTitle;
}

/**
 * Setup form submission handlers
 */
function setupFormSubmissions() {
    document.getElementById('directorForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitOptimization('director', this);
    });
    
    document.getElementById('soleTraderForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitOptimization('sole-trader', this);
    });
    
    document.getElementById('companyOwnerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitOptimization('company-owner', this);
    });
    
    document.getElementById('landlordForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitOptimization('landlord', this);
    });
}

/**
 * Submit optimization request to API
 */
async function submitOptimization(userType, form) {
    // Get form data
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (key === 'is_furnished') {
            data[key] = form.querySelector(`[name="${key}"]`).checked;
        } else if (key === 'number_of_properties') {
            data[key] = parseInt(value);
        } else {
            data[key] = parseFloat(value);
        }
    }
    
    // Show loading
    showLoading();
    hideError();
    hideResults();
    
    try {
        // Make API call
        const response = await fetch(`${API_BASE_URL}/optimize/${userType}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || errorData.message || 'API request failed');
        }
        
        const results = await response.json();
        currentResults = results;
        
        // Hide loading
        hideLoading();
        
        // Display results
        displayResults(results);
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showError(error.message);
    }
}

/**
 * Display optimization results
 */
function displayResults(results) {
    // Update summary cards
    document.getElementById('currentTax').textContent = formatCurrency(
        results.current_position.total_tax
    );
    document.getElementById('optimalTax').textContent = formatCurrency(
        results.optimal_position.total_tax
    );
    document.getElementById('potentialSaving').textContent = formatCurrency(
        results.potential_saving
    );
    
    // Display current position
    displayPosition('currentPosition', results.current_position, 'current');
    
    // Display optimal position
    displayPosition('optimalPosition', results.optimal_position, 'optimal');
    
    // Display recommendations
    displayRecommendations(results.recommendations);
    
    // Show results section
    document.getElementById('resultsSection').classList.remove('hidden');
}

/**
 * Display position details
 */
function displayPosition(elementId, position, type) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';
    
    // Determine which fields to display based on available data
    const fields = [];
    
    // Common fields
    if (position.salary !== undefined) {
        fields.push({ label: 'Salary', value: position.salary });
    }
    if (position.dividends !== undefined) {
        fields.push({ label: 'Dividends', value: position.dividends });
    }
    if (position.trading_income !== undefined) {
        fields.push({ label: 'Trading Income', value: position.trading_income });
    }
    if (position.rental_income !== undefined) {
        fields.push({ label: 'Rental Income', value: position.rental_income });
    }
    if (position.company_profit !== undefined) {
        fields.push({ label: 'Company Profit', value: position.company_profit });
    }
    
    // Income breakdown
    if (position.total_income !== undefined) {
        fields.push({ label: 'Total Income', value: position.total_income, bold: true });
    }
    
    // Tax breakdown
    if (position.income_tax !== undefined) {
        fields.push({ label: 'Income Tax', value: position.income_tax, tax: true });
    }
    if (position.national_insurance !== undefined) {
        fields.push({ label: 'National Insurance', value: position.national_insurance, tax: true });
    }
    if (position.dividend_tax !== undefined) {
        fields.push({ label: 'Dividend Tax', value: position.dividend_tax, tax: true });
    }
    if (position.corporation_tax !== undefined) {
        fields.push({ label: 'Corporation Tax', value: position.corporation_tax, tax: true });
    }
    
    // Total tax
    if (position.total_tax !== undefined) {
        fields.push({ label: 'Total Tax', value: position.total_tax, bold: true, highlight: true });
    }
    
    // Net income
    if (position.net_income !== undefined) {
        fields.push({ label: 'Net Income', value: position.net_income, bold: true, success: true });
    }
    
    // Render fields
    fields.forEach(field => {
        const row = document.createElement('div');
        row.className = 'flex justify-between items-center py-2 border-b border-gray-200';
        
        let labelClass = 'text-gray-700';
        let valueClass = 'text-gray-900';
        
        if (field.bold) {
            labelClass += ' font-bold';
            valueClass += ' font-bold';
        }
        
        if (field.highlight) {
            valueClass += ' text-red-600';
        }
        
        if (field.success) {
            valueClass += ' text-green-600';
        }
        
        row.innerHTML = `
            <span class="${labelClass}">${field.label}</span>
            <span class="${valueClass}">${formatCurrency(field.value)}</span>
        `;
        
        container.appendChild(row);
    });
}

/**
 * Display recommendations
 */
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';
    
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p class="text-gray-600">No recommendations available.</p>';
        return;
    }
    
    recommendations.forEach((rec, index) => {
        const recCard = document.createElement('div');
        recCard.className = 'border-l-4 p-4 rounded-lg bg-gray-50';
        
        // Set border color based on priority
        let borderColor = 'border-blue-500';
        let priorityBadgeColor = 'bg-blue-500';
        
        if (rec.priority === 'high') {
            borderColor = 'border-red-500';
            priorityBadgeColor = 'bg-red-500';
        } else if (rec.priority === 'medium') {
            borderColor = 'border-yellow-500';
            priorityBadgeColor = 'bg-yellow-500';
        } else {
            borderColor = 'border-green-500';
            priorityBadgeColor = 'bg-green-500';
        }
        
        recCard.classList.add(borderColor);
        
        recCard.innerHTML = `
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="${priorityBadgeColor} text-white text-xs font-bold px-2 py-1 rounded uppercase">
                            ${rec.priority} Priority
                        </span>
                        <h4 class="text-lg font-bold text-gray-800">${rec.title}</h4>
                    </div>
                    <p class="text-gray-700 mb-2">${rec.description}</p>
                    ${rec.potential_saving > 0 ? `
                        <p class="text-green-600 font-semibold">
                            <i class="fas fa-piggy-bank mr-1"></i>
                            Potential Saving: ${formatCurrency(rec.potential_saving)}
                        </p>
                    ` : ''}
                </div>
            </div>
        `;
        
        container.appendChild(recCard);
    });
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'GBP',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

/**
 * Show loading indicator
 */
function showLoading() {
    document.getElementById('loadingIndicator').classList.remove('hidden');
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    document.getElementById('loadingIndicator').classList.add('hidden');
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorMessage').classList.remove('hidden');
    
    // Scroll to error
    document.getElementById('errorMessage').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
    });
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('errorMessage').classList.add('hidden');
}

/**
 * Hide results section
 */
function hideResults() {
    document.getElementById('resultsSection').classList.add('hidden');
}

/**
 * Reset form and UI
 */
function resetForm() {
    // Reset current form
    if (currentUserType) {
        const formMap = {
            'director': 'directorForm',
            'sole-trader': 'soleTraderForm',
            'company-owner': 'companyOwnerForm',
            'landlord': 'landlordForm'
        };
        
        const formId = formMap[currentUserType];
        if (formId) {
            document.getElementById(formId).reset();
        }
    }
    
    // Hide results and errors
    hideResults();
    hideError();
}

/**
 * Sample scenarios for testing
 */
const sampleScenarios = {
    director: {
        salary: 30000,
        dividends: 20000,
        company_profit: 60000,
        pension_contribution: 0
    },
    soleTrader: {
        trading_income: 50000,
        allowable_expenses: 8000,
        pension_contribution: 3000,
        capital_allowances: 2000
    },
    companyOwner: {
        company_profit: 100000,
        salary: 30000,
        dividends: 40000,
        r_and_d_expenditure: 15000,
        capital_investment: 20000
    },
    landlord: {
        rental_income: 30000,
        mortgage_interest: 8000,
        other_expenses: 5000,
        is_furnished: true,
        number_of_properties: 2
    }
};

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatCurrency,
        sampleScenarios
    };
}
