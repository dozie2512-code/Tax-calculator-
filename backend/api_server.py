"""
Simple HTTP API Server for Tax Calculator

This provides a lightweight HTTP API to connect the frontend with backend services.
Uses only Python standard library (http.server) for minimal dependencies.

Author: Tax Calculator System
Date: 2024
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from xero_api import XeroAPIClient, DataSyncManager
from tax_optimizer import TaxOptimizer, AllowableExpenses, EntityType


class TaxCalculatorAPIHandler(BaseHTTPRequestHandler):
    """
    HTTP Request Handler for Tax Calculator API
    """
    
    def __init__(self, *args, **kwargs):
        self.xero_client = XeroAPIClient()
        self.sync_manager = DataSyncManager(self.xero_client)
        self.tax_optimizer = TaxOptimizer()
        super().__init__(*args, **kwargs)
    
    def _set_cors_headers(self):
        """Set CORS headers to allow frontend access"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        """
        Send JSON response
        
        Args:
            data: Dictionary to send as JSON
            status_code: HTTP status code
        """
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_error_response(self, message: str, status_code: int = 400):
        """
        Send error response
        
        Args:
            message: Error message
            status_code: HTTP status code
        """
        self._send_json_response({
            'success': False,
            'error': message
        }, status_code)
    
    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS preflight"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route handling
        if path == '/api/health':
            self._handle_health()
        elif path == '/api/xero/status':
            self._handle_xero_status()
        elif path == '/api/xero/invoices':
            self._handle_get_invoices()
        elif path == '/api/xero/expenses':
            self._handle_get_expenses()
        elif path == '/api/xero/accounts':
            self._handle_get_accounts()
        elif path.startswith('/api/allowable-expenses/'):
            entity_type = path.split('/')[-1]
            self._handle_get_allowable_expenses(entity_type)
        else:
            self._send_error_response('Endpoint not found', 404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_error_response('Invalid JSON in request body')
            return
        
        # Route handling
        if path == '/api/xero/connect':
            self._handle_xero_connect(data)
        elif path == '/api/xero/sync':
            self._handle_xero_sync(data)
        elif path == '/api/tax/optimize':
            self._handle_tax_optimize(data)
        elif path == '/api/tax/calculate':
            self._handle_tax_calculate(data)
        else:
            self._send_error_response('Endpoint not found', 404)
    
    def _handle_health(self):
        """Health check endpoint"""
        self._send_json_response({
            'status': 'healthy',
            'service': 'Tax Calculator API',
            'version': '1.0.0'
        })
    
    def _handle_xero_status(self):
        """Get Xero connection status"""
        self._send_json_response({
            'success': True,
            'connected': self.xero_client.connected,
            'last_sync': self.sync_manager.last_sync
        })
    
    def _handle_xero_connect(self, data: Dict[str, Any]):
        """
        Connect to Xero
        
        Args:
            data: Request data (can contain client_id, client_secret)
        """
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        
        if client_id and client_secret:
            self.xero_client = XeroAPIClient(client_id, client_secret)
            self.sync_manager = DataSyncManager(self.xero_client)
        
        result = self.xero_client.authenticate()
        self._send_json_response(result)
    
    def _handle_xero_sync(self, data: Dict[str, Any]):
        """
        Sync data from Xero
        
        Args:
            data: Request data (can contain data_types array)
        """
        if not self.xero_client.connected:
            self._send_error_response('Not connected to Xero. Please connect first.')
            return
        
        save_to_file = data.get('save_to_file', True)
        result = self.sync_manager.sync_all(save_to_file=save_to_file)
        self._send_json_response(result)
    
    def _handle_get_invoices(self):
        """Get invoices from Xero"""
        if not self.xero_client.connected:
            self._send_error_response('Not connected to Xero. Please connect first.')
            return
        
        result = self.xero_client.fetch_invoices()
        self._send_json_response(result)
    
    def _handle_get_expenses(self):
        """Get expenses from Xero"""
        if not self.xero_client.connected:
            self._send_error_response('Not connected to Xero. Please connect first.')
            return
        
        result = self.xero_client.fetch_expenses()
        self._send_json_response(result)
    
    def _handle_get_accounts(self):
        """Get chart of accounts from Xero"""
        if not self.xero_client.connected:
            self._send_error_response('Not connected to Xero. Please connect first.')
            return
        
        result = self.xero_client.fetch_accounts()
        self._send_json_response(result)
    
    def _handle_get_allowable_expenses(self, entity_type: str):
        """
        Get allowable expenses for entity type
        
        Args:
            entity_type: Type of entity (sole_trader, company, landlord, employee)
        """
        expenses_map = {
            'sole_trader': AllowableExpenses.get_sole_trader_expenses,
            'company': AllowableExpenses.get_company_expenses,
            'landlord': AllowableExpenses.get_landlord_expenses,
            'employee': AllowableExpenses.get_employee_expenses
        }
        
        if entity_type not in expenses_map:
            self._send_error_response(f'Invalid entity type: {entity_type}')
            return
        
        expenses = expenses_map[entity_type]()
        self._send_json_response({
            'success': True,
            'entity_type': entity_type,
            'expenses': expenses
        })
    
    def _handle_tax_optimize(self, data: Dict[str, Any]):
        """
        Get tax optimization suggestions
        
        Args:
            data: Request data containing entity type and financial data
        """
        entity_type = data.get('entity_type')
        
        if not entity_type:
            self._send_error_response('entity_type is required')
            return
        
        try:
            if entity_type == 'sole_trader':
                income = float(data.get('income', 0))
                expenses = float(data.get('expenses', 0))
                result = self.tax_optimizer.optimize_sole_trader(income, expenses)
            
            elif entity_type == 'company':
                profit = float(data.get('profit', 0))
                salary = float(data.get('salary', 0))
                dividends = float(data.get('dividends', 0))
                result = self.tax_optimizer.optimize_company(profit, salary, dividends)
            
            elif entity_type == 'landlord':
                rental_income = float(data.get('rental_income', 0))
                expenses = float(data.get('expenses', 0))
                mortgage_interest = float(data.get('mortgage_interest', 0))
                result = self.tax_optimizer.optimize_landlord(
                    rental_income, expenses, mortgage_interest
                )
            
            elif entity_type == 'employee':
                salary = float(data.get('salary', 0))
                bonus = float(data.get('bonus', 0))
                other_income = float(data.get('other_income', 0))
                result = self.tax_optimizer.optimize_employee(salary, bonus, other_income)
            
            else:
                self._send_error_response(f'Invalid entity type: {entity_type}')
                return
            
            self._send_json_response({
                'success': True,
                'optimization': result
            })
        
        except Exception as e:
            self._send_error_response(f'Optimization failed: {str(e)}', 500)
    
    def _handle_tax_calculate(self, data: Dict[str, Any]):
        """
        Calculate tax for given inputs
        
        Args:
            data: Request data containing entity type and financial data
        """
        entity_type = data.get('entity_type')
        
        if not entity_type:
            self._send_error_response('entity_type is required')
            return
        
        # This endpoint can be expanded to provide detailed tax calculations
        # For now, redirect to optimization which includes calculations
        self._handle_tax_optimize(data)
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(host: str = 'localhost', port: int = 8080):
    """
    Run the HTTP API server
    
    Args:
        host: Host to bind to
        port: Port to bind to
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, TaxCalculatorAPIHandler)
    
    print("=" * 60)
    print("Tax Calculator API Server")
    print("=" * 60)
    print(f"\nServer running on http://{host}:{port}")
    print("\nAvailable endpoints:")
    print("  GET  /api/health                      - Health check")
    print("  GET  /api/xero/status                 - Xero connection status")
    print("  POST /api/xero/connect                - Connect to Xero")
    print("  POST /api/xero/sync                   - Sync data from Xero")
    print("  GET  /api/xero/invoices               - Get invoices")
    print("  GET  /api/xero/expenses               - Get expenses")
    print("  GET  /api/xero/accounts               - Get accounts")
    print("  GET  /api/allowable-expenses/{type}   - Get allowable expenses")
    print("  POST /api/tax/optimize                - Get tax optimization")
    print("  POST /api/tax/calculate               - Calculate tax")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("Server stopped.")


if __name__ == '__main__':
    # Parse command line arguments
    import sys
    
    host = 'localhost'
    port = 8080
    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    run_server(host, port)
