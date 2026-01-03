/**
 * Tax Calculator API Client
 * Provides frontend integration with backend services
 * Uses localStorage for session management and simulates API calls
 */

class TaxCalculatorAPIClient {
    constructor() {
        this.sessionKey = 'taxcalc_session';
        this.storagePrefix = 'taxcalc_';
        this.initializeStorage();
    }

    /**
     * Initialize localStorage structure
     */
    initializeStorage() {
        if (!localStorage.getItem(this.storagePrefix + 'users')) {
            localStorage.setItem(this.storagePrefix + 'users', JSON.stringify({}));
        }
        if (!localStorage.getItem(this.storagePrefix + 'businesses')) {
            localStorage.setItem(this.storagePrefix + 'businesses', JSON.stringify({}));
        }
        if (!localStorage.getItem(this.storagePrefix + 'sessions')) {
            localStorage.setItem(this.storagePrefix + 'sessions', JSON.stringify({}));
        }
        if (!localStorage.getItem(this.storagePrefix + 'transactions')) {
            localStorage.setItem(this.storagePrefix + 'transactions', JSON.stringify({}));
        }
    }

    /**
     * Hash password (simple implementation for demo)
     * Note: For production, use proper crypto library like bcrypt
     */
    hashPassword(password) {
        // Add simple salt for basic protection
        const salt = 'taxcalc_salt_2024';
        const salted = salt + password + salt;
        
        // Simple hash implementation (not production-ready)
        let hash = 0;
        for (let i = 0; i < salted.length; i++) {
            const char = salted.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return hash.toString(36);
    }

    /**
     * Generate UUID
     */
    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Register a new user
     */
    register(username, password, email, fullName = '') {
        const users = JSON.parse(localStorage.getItem(this.storagePrefix + 'users'));
        
        if (users[username]) {
            return { success: false, error: 'Username already exists' };
        }

        const userId = this.generateUUID();
        users[username] = {
            user_id: userId,
            username: username,
            password: this.hashPassword(password),
            email: email,
            full_name: fullName,
            created_at: new Date().toISOString(),
            businesses: []
        };

        localStorage.setItem(this.storagePrefix + 'users', JSON.stringify(users));

        return {
            success: true,
            user_id: userId,
            username: username,
            email: email,
            full_name: fullName
        };
    }

    /**
     * Login user
     */
    login(username, password) {
        const users = JSON.parse(localStorage.getItem(this.storagePrefix + 'users'));
        
        if (!users[username]) {
            return { success: false, error: 'Invalid credentials' };
        }

        const user = users[username];
        if (user.password !== this.hashPassword(password)) {
            return { success: false, error: 'Invalid credentials' };
        }

        // Create session
        const sessionToken = this.generateUUID();
        const sessions = JSON.parse(localStorage.getItem(this.storagePrefix + 'sessions'));
        
        const expiresAt = new Date();
        expiresAt.setHours(expiresAt.getHours() + 24);

        sessions[sessionToken] = {
            user_id: user.user_id,
            username: username,
            created_at: new Date().toISOString(),
            expires_at: expiresAt.toISOString()
        };

        localStorage.setItem(this.storagePrefix + 'sessions', JSON.stringify(sessions));
        localStorage.setItem(this.sessionKey, sessionToken);

        // Get user's businesses
        const businesses = JSON.parse(localStorage.getItem(this.storagePrefix + 'businesses'));
        const userBusinesses = Object.values(businesses).filter(b => 
            b.users && b.users.includes(user.user_id)
        );

        return {
            success: true,
            session_token: sessionToken,
            user: {
                user_id: user.user_id,
                username: username,
                email: user.email,
                full_name: user.full_name,
                businesses: userBusinesses
            }
        };
    }

    /**
     * Logout user
     */
    logout() {
        const sessionToken = localStorage.getItem(this.sessionKey);
        if (sessionToken) {
            const sessions = JSON.parse(localStorage.getItem(this.storagePrefix + 'sessions'));
            delete sessions[sessionToken];
            localStorage.setItem(this.storagePrefix + 'sessions', JSON.stringify(sessions));
            localStorage.removeItem(this.sessionKey);
        }
        return { success: true };
    }

    /**
     * Validate current session
     */
    validateSession() {
        const sessionToken = localStorage.getItem(this.sessionKey);
        if (!sessionToken) {
            return { success: false, error: 'No active session' };
        }

        const sessions = JSON.parse(localStorage.getItem(this.storagePrefix + 'sessions'));
        if (!sessions[sessionToken]) {
            localStorage.removeItem(this.sessionKey);
            return { success: false, error: 'Invalid session' };
        }

        const session = sessions[sessionToken];
        const expiresAt = new Date(session.expires_at);

        if (new Date() > expiresAt) {
            delete sessions[sessionToken];
            localStorage.setItem(this.storagePrefix + 'sessions', JSON.stringify(sessions));
            localStorage.removeItem(this.sessionKey);
            return { success: false, error: 'Session expired' };
        }

        return {
            success: true,
            user_id: session.user_id,
            username: session.username
        };
    }

    /**
     * Get current user
     */
    getCurrentUser() {
        const validation = this.validateSession();
        if (!validation.success) {
            return null;
        }

        const users = JSON.parse(localStorage.getItem(this.storagePrefix + 'users'));
        const user = users[validation.username];
        
        if (!user) {
            return null;
        }

        // Get user's businesses
        const businesses = JSON.parse(localStorage.getItem(this.storagePrefix + 'businesses'));
        const userBusinesses = Object.values(businesses).filter(b => 
            b.users && b.users.includes(user.user_id)
        );

        return {
            user_id: user.user_id,
            username: user.username,
            email: user.email,
            full_name: user.full_name,
            businesses: userBusinesses
        };
    }

    /**
     * Create a new business
     */
    createBusiness(name, businessType = 'Sole Trader', taxNumber = '', address = '') {
        const validation = this.validateSession();
        if (!validation.success) {
            return validation;
        }

        const businessId = this.generateUUID();
        const businesses = JSON.parse(localStorage.getItem(this.storagePrefix + 'businesses'));

        businesses[businessId] = {
            business_id: businessId,
            name: name,
            owner_id: validation.user_id,
            business_type: businessType,
            tax_number: taxNumber,
            address: address,
            created_at: new Date().toISOString(),
            users: [validation.user_id],
            settings: {
                tax_year: '2024/25',
                vat_registered: false,
                accounting_period_end: '31-03'
            }
        };

        localStorage.setItem(this.storagePrefix + 'businesses', JSON.stringify(businesses));

        // Add business to user
        const users = JSON.parse(localStorage.getItem(this.storagePrefix + 'users'));
        if (users[validation.username]) {
            if (!users[validation.username].businesses.includes(businessId)) {
                users[validation.username].businesses.push(businessId);
                localStorage.setItem(this.storagePrefix + 'users', JSON.stringify(users));
            }
        }

        return {
            success: true,
            business_id: businessId,
            business: businesses[businessId]
        };
    }

    /**
     * Get user's businesses
     */
    getUserBusinesses() {
        const validation = this.validateSession();
        if (!validation.success) {
            return validation;
        }

        const businesses = JSON.parse(localStorage.getItem(this.storagePrefix + 'businesses'));
        const userBusinesses = Object.values(businesses).filter(b => 
            b.users && b.users.includes(validation.user_id)
        );

        return {
            success: true,
            businesses: userBusinesses
        };
    }

    /**
     * Get specific business
     */
    getBusiness(businessId) {
        const validation = this.validateSession();
        if (!validation.success) {
            return validation;
        }

        const businesses = JSON.parse(localStorage.getItem(this.storagePrefix + 'businesses'));
        const business = businesses[businessId];

        if (!business) {
            return { success: false, error: 'Business not found' };
        }

        if (!business.users || !business.users.includes(validation.user_id)) {
            return { success: false, error: 'Access denied' };
        }

        return { success: true, business: business };
    }

    /**
     * Parse and upload bank transaction CSV
     */
    uploadBankTransactions(businessId, csvContent) {
        const validation = this.validateSession();
        if (!validation.success) {
            return validation;
        }

        const business = this.getBusiness(businessId);
        if (!business.success) {
            return business;
        }

        // Parse CSV
        const transactions = [];
        const lines = csvContent.trim().split('\n');
        
        if (lines.length < 2) {
            return { success: false, error: 'CSV must contain headers and at least one transaction' };
        }

        const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
        
        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',').map(v => v.trim());
            const transaction = {};
            
            headers.forEach((header, idx) => {
                transaction[header] = values[idx] || '';
            });

            // Process transaction
            const amount = parseFloat(transaction.amount || transaction.debit || transaction.credit || 0);
            const category = this.categorizeTransaction(transaction.description || '', amount);

            transactions.push({
                date: this.parseDate(transaction.date),
                description: transaction.description || '',
                amount: amount,
                category: category,
                business_id: businessId,
                reference: transaction.reference || '',
                imported_at: new Date().toISOString()
            });
        }

        // Save transactions
        const allTransactions = JSON.parse(localStorage.getItem(this.storagePrefix + 'transactions'));
        if (!allTransactions[businessId]) {
            allTransactions[businessId] = [];
        }
        allTransactions[businessId].push(...transactions);
        localStorage.setItem(this.storagePrefix + 'transactions', JSON.stringify(allTransactions));

        // Generate summary
        const summary = this.generateTransactionSummary(transactions);

        return {
            success: true,
            transactions_count: transactions.length,
            transactions: transactions,
            summary: summary
        };
    }

    /**
     * Categorize transaction based on description
     * Note: Uses keyword matching - patterns are case-insensitive
     */
    categorizeTransaction(description, amount) {
        const desc = description.toLowerCase();
        
        // Income patterns (spaces properly escaped)
        if (desc.match(/(payment|deposit|credit|invoice|sale)/)) return 'Sales';
        if (desc.match(/transfer\s+in/)) return 'Sales';
        if (desc.match(/(interest|dividend)/)) return 'Interest Income';
        
        // Expense patterns
        if (desc.match(/(rent|lease|landlord)/)) return 'Rent';
        if (desc.match(/(electric|gas|water|utility|utilities)/)) return 'Utilities';
        if (desc.match(/(salary|salaries|wage|payroll|paye)/)) return 'Salaries';
        if (desc.match(/(insurance|policy)/)) return 'Insurance';
        if (desc.match(/(stationery|supplies|office)/)) return 'Office Supplies';
        if (desc.match(/(accountant|lawyer|consultant|professional)/)) return 'Professional Fees';
        if (desc.match(/(travel|hotel|flight|train|taxi|uber)/)) return 'Travel';
        if (desc.match(/(advertising|marketing|promotion)/)) return 'Marketing';
        if (desc.match(/(equipment|computer|software|hardware)/)) return 'Equipment';
        
        // Tax patterns
        if (desc.match(/(vat|value added tax)/)) return 'VAT Payment';
        if (desc.match(/(corporation tax|ct600)/)) return 'Corporation Tax';
        if (desc.match(/(self assessment|sa)/)) return 'Self Assessment';
        
        // Default based on amount
        if (amount > 0) return 'Sales';
        if (amount < 0) return 'Other Expenses';
        return 'Uncategorized';
    }

    /**
     * Parse date string
     */
    parseDate(dateStr) {
        const formats = [
            /^(\d{4})-(\d{2})-(\d{2})$/,  // YYYY-MM-DD
            /^(\d{2})\/(\d{2})\/(\d{4})$/,  // DD/MM/YYYY
            /^(\d{2})-(\d{2})-(\d{4})$/   // DD-MM-YYYY
        ];

        for (const format of formats) {
            const match = dateStr.match(format);
            if (match) {
                if (match[1].length === 4) {
                    // YYYY-MM-DD
                    return dateStr;
                } else {
                    // DD/MM/YYYY or DD-MM-YYYY
                    return `${match[3]}-${match[2]}-${match[1]}`;
                }
            }
        }
        return new Date().toISOString().split('T')[0];
    }

    /**
     * Generate transaction summary
     */
    generateTransactionSummary(transactions) {
        const totalIncome = transactions.filter(t => t.amount > 0).reduce((sum, t) => sum + t.amount, 0);
        const totalExpenses = Math.abs(transactions.filter(t => t.amount < 0).reduce((sum, t) => sum + t.amount, 0));
        
        const categories = {};
        transactions.forEach(t => {
            if (!categories[t.category]) {
                categories[t.category] = 0;
            }
            categories[t.category] += Math.abs(t.amount);
        });

        return {
            total_transactions: transactions.length,
            total_income: Math.round(totalIncome * 100) / 100,
            total_expenses: Math.round(totalExpenses * 100) / 100,
            net_amount: Math.round((totalIncome - totalExpenses) * 100) / 100,
            categories: categories
        };
    }

    /**
     * Get transactions for a business
     */
    getTransactions(businessId, startDate = null, endDate = null, category = null) {
        const validation = this.validateSession();
        if (!validation.success) {
            return validation;
        }

        const business = this.getBusiness(businessId);
        if (!business.success) {
            return business;
        }

        const allTransactions = JSON.parse(localStorage.getItem(this.storagePrefix + 'transactions'));
        let transactions = allTransactions[businessId] || [];

        // Apply filters
        if (startDate) {
            transactions = transactions.filter(t => t.date >= startDate);
        }
        if (endDate) {
            transactions = transactions.filter(t => t.date <= endDate);
        }
        if (category) {
            transactions = transactions.filter(t => t.category === category);
        }

        return {
            success: true,
            transactions: transactions,
            count: transactions.length
        };
    }

    /**
     * Check if user is logged in
     */
    isLoggedIn() {
        const validation = this.validateSession();
        return validation.success;
    }
}

// Create global instance
const taxCalcAPI = new TaxCalculatorAPIClient();
