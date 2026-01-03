"""
Simple API Layer for Tax Calculator
Provides backend services for authentication, business management, and bank transactions
This is a simple file-based API for browser-based frontend integration
"""

import json
from typing import Dict, Any
from pathlib import Path
from auth import AuthenticationSystem
from business_manager import BusinessManager
from bank_transactions import BankTransactionParser


class TaxCalculatorAPI:
    """Main API class for Tax Calculator application"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize API with all required components
        
        Args:
            data_dir: Directory to store all data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.auth = AuthenticationSystem(data_dir)
        self.business_manager = BusinessManager(data_dir)
        self.transaction_parser = BankTransactionParser(data_dir)
    
    # Authentication endpoints
    
    def register(self, username: str, password: str, email: str, 
                full_name: str = "") -> Dict[str, Any]:
        """Register a new user"""
        return self.auth.register_user(username, password, email, full_name)
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login user and return session token"""
        login_result = self.auth.login(username, password)
        
        if login_result["success"]:
            # Add user's businesses to the response
            user_id = login_result["user"]["user_id"]
            businesses = self.business_manager.get_user_businesses(user_id)
            login_result["user"]["businesses"] = businesses
        
        return login_result
    
    def logout(self, session_token: str) -> Dict[str, Any]:
        """Logout user"""
        return self.auth.logout(session_token)
    
    def validate_session(self, session_token: str) -> Dict[str, Any]:
        """Validate user session"""
        return self.auth.validate_session(session_token)
    
    # Business management endpoints
    
    def create_business(self, session_token: str, name: str, 
                       business_type: str = "Sole Trader",
                       tax_number: str = "", address: str = "") -> Dict[str, Any]:
        """Create a new business for authenticated user"""
        # Validate session
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        username = validation["username"]
        
        # Create business
        result = self.business_manager.create_business(
            name, user_id, business_type, tax_number, address
        )
        
        if result["success"]:
            # Associate business with user
            business_id = result["business_id"]
            self.auth.add_business_to_user(username, business_id)
        
        return result
    
    def get_user_businesses(self, session_token: str) -> Dict[str, Any]:
        """Get all businesses for authenticated user"""
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        businesses = self.business_manager.get_user_businesses(user_id)
        
        return {
            "success": True,
            "businesses": businesses
        }
    
    def get_business(self, session_token: str, business_id: str) -> Dict[str, Any]:
        """Get specific business details"""
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        business = self.business_manager.get_business(business_id)
        
        if not business:
            return {"success": False, "error": "Business not found"}
        
        # Check if user has access to this business
        if user_id not in business.get("users", []):
            return {"success": False, "error": "Access denied"}
        
        return {"success": True, "business": business}
    
    def update_business(self, session_token: str, business_id: str, 
                       updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update business information"""
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        business = self.business_manager.get_business(business_id)
        
        if not business:
            return {"success": False, "error": "Business not found"}
        
        # Check if user has access
        if user_id not in business.get("users", []):
            return {"success": False, "error": "Access denied"}
        
        return self.business_manager.update_business(business_id, updates)
    
    # Bank transaction endpoints
    
    def upload_bank_transactions(self, session_token: str, business_id: str,
                                 csv_content: str) -> Dict[str, Any]:
        """Upload and parse bank transaction CSV"""
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        business = self.business_manager.get_business(business_id)
        
        if not business:
            return {"success": False, "error": "Business not found"}
        
        # Check if user has access
        if user_id not in business.get("users", []):
            return {"success": False, "error": "Access denied"}
        
        return self.transaction_parser.parse_csv(csv_content, business_id)
    
    def get_transactions(self, session_token: str, business_id: str,
                        start_date: str = None, end_date: str = None,
                        category: str = None) -> Dict[str, Any]:
        """Get transactions for a business"""
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        business = self.business_manager.get_business(business_id)
        
        if not business:
            return {"success": False, "error": "Business not found"}
        
        # Check if user has access
        if user_id not in business.get("users", []):
            return {"success": False, "error": "Access denied"}
        
        transactions = self.transaction_parser.get_business_transactions(
            business_id, start_date, end_date, category
        )
        
        return {
            "success": True,
            "transactions": transactions,
            "count": len(transactions)
        }
    
    def update_transaction_category(self, session_token: str, business_id: str,
                                   transaction_idx: int, new_category: str) -> Dict[str, Any]:
        """Update transaction category"""
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        business = self.business_manager.get_business(business_id)
        
        if not business:
            return {"success": False, "error": "Business not found"}
        
        # Check if user has access
        if user_id not in business.get("users", []):
            return {"success": False, "error": "Access denied"}
        
        return self.transaction_parser.update_transaction_category(
            business_id, transaction_idx, new_category
        )
    
    def get_available_categories(self) -> Dict[str, Any]:
        """Get available transaction categories"""
        return {
            "success": True,
            "categories": self.transaction_parser.categories
        }
    
    # Tax computation endpoints (integrating with existing tax calculations)
    
    def save_tax_computation(self, session_token: str, business_id: str,
                           computation_type: str, computation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save tax computation for a business"""
        validation = self.auth.validate_session(session_token)
        if not validation["success"]:
            return validation
        
        user_id = validation["user_id"]
        business = self.business_manager.get_business(business_id)
        
        if not business:
            return {"success": False, "error": "Business not found"}
        
        # Check if user has access
        if user_id not in business.get("users", []):
            return {"success": False, "error": "Access denied"}
        
        # Save computation
        computations_dir = self.data_dir / "computations"
        computations_dir.mkdir(exist_ok=True)
        
        filename = computations_dir / f"{business_id}_{computation_type}.json"
        
        computation_record = {
            "business_id": business_id,
            "computation_type": computation_type,
            "data": computation_data,
            "computed_by": user_id,
            "computed_at": json.dumps({"timestamp": "now"}),  # Simplified
        }
        
        # Load existing computations
        existing = []
        if filename.exists():
            with open(filename, 'r') as f:
                existing = json.load(f)
        
        existing.append(computation_record)
        
        with open(filename, 'w') as f:
            json.dump(existing, f, indent=2)
        
        return {"success": True, "computation_id": len(existing) - 1}


# For frontend integration via JavaScript
def create_api_bridge(data_dir: str = "data"):
    """
    Create API bridge file that frontend can use
    This writes API responses to JSON files that frontend can read
    """
    api = TaxCalculatorAPI(data_dir)
    bridge_dir = Path(data_dir) / "api_bridge"
    bridge_dir.mkdir(exist_ok=True)
    
    return api


if __name__ == "__main__":
    # Demo usage
    api = TaxCalculatorAPI()
    
    print("=== Tax Calculator API Demo ===\n")
    
    # Register user
    print("1. Registering user...")
    register_result = api.register("demo_user", "demo_pass", "demo@example.com", "Demo User")
    print(f"   Result: {register_result}\n")
    
    # Login
    print("2. Logging in...")
    login_result = api.login("demo_user", "demo_pass")
    if login_result["success"]:
        token = login_result["session_token"]
        print(f"   Success! Token: {token[:20]}...\n")
        
        # Create business
        print("3. Creating business...")
        business_result = api.create_business(
            token, "Demo Business Ltd", "Limited Company", "UTR123456"
        )
        if business_result["success"]:
            business_id = business_result["business_id"]
            print(f"   Success! Business ID: {business_id}\n")
            
            # Upload transactions
            print("4. Uploading bank transactions...")
            csv_data = """date,description,amount
2024-01-15,Customer payment,5000.00
2024-01-16,Rent payment,-1500.00
2024-01-17,Office supplies,-120.00"""
            
            tx_result = api.upload_bank_transactions(token, business_id, csv_data)
            if tx_result["success"]:
                print(f"   Uploaded {tx_result['transactions_count']} transactions")
                print(f"   Total Income: £{tx_result['summary']['total_income']}")
                print(f"   Total Expenses: £{tx_result['summary']['total_expenses']}\n")
            
            # Get businesses
            print("5. Getting user businesses...")
            businesses_result = api.get_user_businesses(token)
            if businesses_result["success"]:
                print(f"   Found {len(businesses_result['businesses'])} business(es)\n")
        
        # Logout
        print("6. Logging out...")
        logout_result = api.logout(token)
        print(f"   Result: {logout_result}")
