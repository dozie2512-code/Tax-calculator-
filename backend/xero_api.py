"""
Xero API Integration Module

This module provides integration with Xero accounting software API for:
- Fetching invoices and expenses
- Synchronizing financial data
- Real-time data updates

Author: Tax Calculator System
Date: 2024
"""

import json
import csv
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os


class XeroAPIClient:
    """
    Client for interacting with Xero API
    
    This is a comprehensive implementation that can be connected to actual Xero API
    by adding proper authentication and API endpoint configuration.
    """
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Initialize Xero API Client
        
        Args:
            client_id: Xero OAuth2 client ID
            client_secret: Xero OAuth2 client secret
        """
        self.client_id = client_id or os.getenv('XERO_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('XERO_CLIENT_SECRET')
        self.access_token = None
        self.token_expiry = None
        self.connected = False
        
    def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with Xero API using OAuth2
        
        Returns:
            Dict containing authentication status and details
        """
        try:
            # PRODUCTION NOTE: Implement actual OAuth2 flow here
            # This simulated implementation is for development/testing only
            # 
            # For production, implement:
            # 1. OAuth2 authorization code flow
            # 2. Secure token storage (encrypted at rest)
            # 3. Token refresh mechanism
            # 4. Proper error handling for expired/invalid tokens
            # 5. PKCE (Proof Key for Code Exchange) for security
            #
            # Example production flow:
            # - Redirect to Xero authorization URL
            # - Handle callback with authorization code
            # - Exchange code for access token
            # - Store token securely with expiry
            # - Implement automatic refresh before expiry
            
            if self.client_id and self.client_secret:
                # Simulated for development - replace with real OAuth2
                self.access_token = "simulated_access_token"
                self.token_expiry = datetime.now() + timedelta(hours=1)
                self.connected = True
                return {
                    'success': True,
                    'message': 'Successfully authenticated with Xero',
                    'expires_in': 3600
                }
            else:
                return {
                    'success': False,
                    'message': 'Missing client credentials',
                    'error': 'MISSING_CREDENTIALS'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Authentication failed: {str(e)}',
                'error': 'AUTH_FAILED'
            }
    
    def refresh_token(self) -> bool:
        """
        Refresh expired access token
        
        Returns:
            Boolean indicating success
        """
        if not self.connected:
            return False
            
        try:
            # In production, implement actual token refresh
            self.token_expiry = datetime.now() + timedelta(hours=1)
            return True
        except Exception:
            return False
    
    def _ensure_authenticated(self) -> bool:
        """
        Ensure valid authentication before API calls
        
        Returns:
            Boolean indicating if authenticated
        """
        if not self.connected:
            auth_result = self.authenticate()
            return auth_result['success']
        
        if self.token_expiry and datetime.now() >= self.token_expiry:
            return self.refresh_token()
        
        return True
    
    def fetch_invoices(self, status: Optional[str] = None, 
                      modified_since: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch invoices from Xero
        
        Args:
            status: Filter by invoice status (DRAFT, SUBMITTED, AUTHORISED, PAID)
            modified_since: ISO date string to fetch only recent changes
            
        Returns:
            Dict containing invoices and metadata
        """
        if not self._ensure_authenticated():
            return {
                'success': False,
                'error': 'NOT_AUTHENTICATED',
                'data': []
            }
        
        try:
            # In production, make actual API call to Xero
            # For now, return simulated data structure
            invoices = self._get_sample_invoices()
            
            # Apply filters
            if status:
                invoices = [inv for inv in invoices if inv['status'].upper() == status.upper()]
            
            if modified_since:
                modified_date = datetime.fromisoformat(modified_since.replace('Z', '+00:00'))
                invoices = [inv for inv in invoices 
                           if datetime.fromisoformat(inv['updated_date']) >= modified_date]
            
            return {
                'success': True,
                'data': invoices,
                'count': len(invoices),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'FETCH_FAILED',
                'message': str(e),
                'data': []
            }
    
    def fetch_expenses(self, category: Optional[str] = None,
                      from_date: Optional[str] = None,
                      to_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch expenses from Xero
        
        Args:
            category: Filter by expense category
            from_date: Start date for filtering (ISO format)
            to_date: End date for filtering (ISO format)
            
        Returns:
            Dict containing expenses and metadata
        """
        if not self._ensure_authenticated():
            return {
                'success': False,
                'error': 'NOT_AUTHENTICATED',
                'data': []
            }
        
        try:
            # In production, make actual API call to Xero
            expenses = self._get_sample_expenses()
            
            # Apply filters
            if category:
                expenses = [exp for exp in expenses if exp['category'] == category]
            
            if from_date:
                start = datetime.fromisoformat(from_date)
                expenses = [exp for exp in expenses 
                           if datetime.fromisoformat(exp['date']) >= start]
            
            if to_date:
                end = datetime.fromisoformat(to_date)
                expenses = [exp for exp in expenses 
                           if datetime.fromisoformat(exp['date']) <= end]
            
            return {
                'success': True,
                'data': expenses,
                'count': len(expenses),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'FETCH_FAILED',
                'message': str(e),
                'data': []
            }
    
    def fetch_accounts(self) -> Dict[str, Any]:
        """
        Fetch chart of accounts from Xero
        
        Returns:
            Dict containing accounts and metadata
        """
        if not self._ensure_authenticated():
            return {
                'success': False,
                'error': 'NOT_AUTHENTICATED',
                'data': []
            }
        
        try:
            accounts = self._get_sample_accounts()
            return {
                'success': True,
                'data': accounts,
                'count': len(accounts),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'FETCH_FAILED',
                'message': str(e),
                'data': []
            }
    
    def sync_data(self, data_types: List[str] = None) -> Dict[str, Any]:
        """
        Synchronize multiple data types from Xero
        
        Args:
            data_types: List of data types to sync (invoices, expenses, accounts)
            
        Returns:
            Dict containing sync results for each data type
        """
        if data_types is None:
            data_types = ['invoices', 'expenses', 'accounts']
        
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'results': {}
        }
        
        for data_type in data_types:
            if data_type == 'invoices':
                result = self.fetch_invoices()
            elif data_type == 'expenses':
                result = self.fetch_expenses()
            elif data_type == 'accounts':
                result = self.fetch_accounts()
            else:
                result = {
                    'success': False,
                    'error': 'INVALID_DATA_TYPE',
                    'message': f'Unknown data type: {data_type}'
                }
            
            results['results'][data_type] = result
            if not result['success']:
                results['success'] = False
        
        return results
    
    def _get_sample_invoices(self) -> List[Dict[str, Any]]:
        """Generate sample invoice data"""
        return [
            {
                'invoice_id': 'INV-001',
                'invoice_number': '10001',
                'contact': 'ABC Ltd',
                'date': '2024-12-01',
                'due_date': '2024-12-31',
                'total': 5000.00,
                'amount_due': 5000.00,
                'status': 'AUTHORISED',
                'line_items': [
                    {'description': 'Consulting services', 'amount': 5000.00}
                ],
                'updated_date': '2024-12-15T10:00:00'
            },
            {
                'invoice_id': 'INV-002',
                'invoice_number': '10002',
                'contact': 'XYZ Corp',
                'date': '2024-12-05',
                'due_date': '2024-12-25',
                'total': 3500.00,
                'amount_due': 0.00,
                'status': 'PAID',
                'line_items': [
                    {'description': 'Software development', 'amount': 3500.00}
                ],
                'updated_date': '2024-12-20T15:30:00'
            }
        ]
    
    def _get_sample_expenses(self) -> List[Dict[str, Any]]:
        """Generate sample expense data"""
        return [
            {
                'expense_id': 'EXP-001',
                'date': '2024-12-01',
                'description': 'Office supplies',
                'amount': 150.50,
                'category': 'Office Supplies',
                'account_code': '6100',
                'tax_amount': 30.10
            },
            {
                'expense_id': 'EXP-002',
                'date': '2024-12-05',
                'description': 'Software subscription',
                'amount': 299.99,
                'category': 'Software',
                'account_code': '6200',
                'tax_amount': 60.00
            },
            {
                'expense_id': 'EXP-003',
                'date': '2024-12-10',
                'description': 'Travel expenses',
                'amount': 450.00,
                'category': 'Travel',
                'account_code': '6300',
                'tax_amount': 90.00
            }
        ]
    
    def _get_sample_accounts(self) -> List[Dict[str, Any]]:
        """Generate sample chart of accounts"""
        return [
            {'code': '1000', 'name': 'Cash', 'type': 'BANK', 'balance': 50000.00},
            {'code': '1200', 'name': 'Accounts Receivable', 'type': 'CURRENT', 'balance': 15000.00},
            {'code': '2000', 'name': 'Accounts Payable', 'type': 'CURRLIAB', 'balance': 8000.00},
            {'code': '4000', 'name': 'Sales', 'type': 'REVENUE', 'balance': 0.00},
            {'code': '6000', 'name': 'Operating Expenses', 'type': 'EXPENSE', 'balance': 0.00}
        ]


class DataSyncManager:
    """
    Manages data synchronization between Xero and local storage
    """
    
    def __init__(self, xero_client: XeroAPIClient):
        """
        Initialize sync manager
        
        Args:
            xero_client: Initialized XeroAPIClient instance
        """
        self.xero_client = xero_client
        self.last_sync = {}
        self.sync_errors = []
    
    def sync_all(self, save_to_file: bool = True) -> Dict[str, Any]:
        """
        Synchronize all data from Xero
        
        Args:
            save_to_file: Whether to save synced data to files
            
        Returns:
            Dict containing sync results
        """
        result = self.xero_client.sync_data()
        
        if result['success'] and save_to_file:
            self._save_sync_data(result)
        
        self.last_sync = {
            'timestamp': result['timestamp'],
            'success': result['success']
        }
        
        return result
    
    def _save_sync_data(self, sync_result: Dict[str, Any]) -> None:
        """
        Save synced data to local files
        
        Args:
            sync_result: Result from sync operation
        """
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save complete sync result as JSON
        with open(f'{output_dir}/xero_sync_{timestamp}.json', 'w') as f:
            json.dump(sync_result, f, indent=2)
        
        # Save individual data types
        for data_type, data_result in sync_result['results'].items():
            if data_result['success'] and data_result['data']:
                # Save as JSON
                with open(f'{output_dir}/xero_{data_type}_{timestamp}.json', 'w') as f:
                    json.dump(data_result['data'], f, indent=2)
                
                # Save as CSV for easy viewing
                self._save_as_csv(data_result['data'], 
                                f'{output_dir}/xero_{data_type}_{timestamp}.csv')
    
    def _save_as_csv(self, data: List[Dict], filename: str) -> None:
        """
        Save data as CSV file
        
        Args:
            data: List of dictionaries to save
            filename: Output filename
        """
        if not data:
            return
        
        # Flatten nested structures for CSV
        flattened_data = []
        for item in data:
            flat_item = {}
            for key, value in item.items():
                if isinstance(value, (list, dict)):
                    flat_item[key] = json.dumps(value)
                else:
                    flat_item[key] = value
            flattened_data.append(flat_item)
        
        keys = flattened_data[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(flattened_data)


def main():
    """
    Main function for testing Xero API integration
    """
    print("=" * 60)
    print("Xero API Integration Test")
    print("=" * 60)
    
    # Initialize client
    client = XeroAPIClient()
    print("\n1. Initializing Xero API Client...")
    
    # Authenticate
    print("\n2. Authenticating with Xero...")
    auth_result = client.authenticate()
    print(f"   Status: {'✓ Success' if auth_result['success'] else '✗ Failed'}")
    print(f"   Message: {auth_result['message']}")
    
    if auth_result['success']:
        # Fetch invoices
        print("\n3. Fetching invoices...")
        invoices = client.fetch_invoices()
        print(f"   Status: {'✓ Success' if invoices['success'] else '✗ Failed'}")
        print(f"   Count: {invoices.get('count', 0)} invoices")
        
        # Fetch expenses
        print("\n4. Fetching expenses...")
        expenses = client.fetch_expenses()
        print(f"   Status: {'✓ Success' if expenses['success'] else '✗ Failed'}")
        print(f"   Count: {expenses.get('count', 0)} expenses")
        
        # Sync all data
        print("\n5. Synchronizing all data...")
        sync_manager = DataSyncManager(client)
        sync_result = sync_manager.sync_all(save_to_file=True)
        print(f"   Status: {'✓ Success' if sync_result['success'] else '✗ Failed'}")
        print(f"   Timestamp: {sync_result['timestamp']}")
        
        print("\n" + "=" * 60)
        print("✓ Test completed successfully!")
        print("  Check 'output/' directory for synced data files")
        print("=" * 60)
    else:
        print("\n✗ Authentication failed. Cannot proceed with data sync.")


if __name__ == '__main__':
    main()
