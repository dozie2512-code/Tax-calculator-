"""
Business Management Module
Handles business entity management and business-user associations
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class BusinessManager:
    """Manages business entities and their associations with users"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize business manager
        
        Args:
            data_dir: Directory to store business data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.businesses_file = self.data_dir / "businesses.json"
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage files if they don't exist"""
        if not self.businesses_file.exists():
            self._save_json(self.businesses_file, {})
    
    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON data from file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, filepath: Path, data: Dict):
        """Save JSON data to file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_business(self, name: str, owner_id: str, 
                       business_type: str = "Sole Trader",
                       tax_number: str = "",
                       address: str = "") -> Dict[str, Any]:
        """
        Create a new business
        
        Args:
            name: Business name
            owner_id: User ID of the business owner
            business_type: Type of business (Sole Trader, Limited Company, etc.)
            tax_number: Tax identification number (UTR, VAT number, etc.)
            address: Business address
            
        Returns:
            Dict with business information
        """
        businesses = self._load_json(self.businesses_file)
        
        business_id = str(uuid.uuid4())
        businesses[business_id] = {
            "business_id": business_id,
            "name": name,
            "owner_id": owner_id,
            "business_type": business_type,
            "tax_number": tax_number,
            "address": address,
            "created_at": datetime.now().isoformat(),
            "users": [owner_id],  # Owner is automatically added as a user
            "settings": {
                "tax_year": "2024/25",
                "vat_registered": False,
                "accounting_period_end": "31-03"
            }
        }
        
        self._save_json(self.businesses_file, businesses)
        
        return {
            "success": True,
            "business_id": business_id,
            "business": businesses[business_id]
        }
    
    def get_business(self, business_id: str) -> Optional[Dict[str, Any]]:
        """
        Get business information
        
        Args:
            business_id: Business ID
            
        Returns:
            Business information dict or None
        """
        businesses = self._load_json(self.businesses_file)
        return businesses.get(business_id)
    
    def get_user_businesses(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all businesses associated with a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of business information dicts
        """
        businesses = self._load_json(self.businesses_file)
        user_businesses = []
        
        for business_id, business in businesses.items():
            if user_id in business.get("users", []):
                user_businesses.append(business)
        
        return user_businesses
    
    def add_user_to_business(self, business_id: str, user_id: str) -> Dict[str, Any]:
        """
        Add a user to a business
        
        Args:
            business_id: Business ID
            user_id: User ID to add
            
        Returns:
            Dict with success status
        """
        businesses = self._load_json(self.businesses_file)
        
        if business_id not in businesses:
            return {"success": False, "error": "Business not found"}
        
        if user_id not in businesses[business_id]["users"]:
            businesses[business_id]["users"].append(user_id)
            self._save_json(self.businesses_file, businesses)
        
        return {"success": True}
    
    def update_business(self, business_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update business information
        
        Args:
            business_id: Business ID
            updates: Dict of fields to update
            
        Returns:
            Dict with success status and updated business
        """
        businesses = self._load_json(self.businesses_file)
        
        if business_id not in businesses:
            return {"success": False, "error": "Business not found"}
        
        # Update allowed fields
        allowed_fields = ["name", "business_type", "tax_number", "address", "settings"]
        for field in allowed_fields:
            if field in updates:
                if field == "settings":
                    businesses[business_id]["settings"].update(updates["settings"])
                else:
                    businesses[business_id][field] = updates[field]
        
        businesses[business_id]["updated_at"] = datetime.now().isoformat()
        self._save_json(self.businesses_file, businesses)
        
        return {
            "success": True,
            "business": businesses[business_id]
        }
    
    def delete_business(self, business_id: str, user_id: str) -> Dict[str, Any]:
        """
        Delete a business (only owner can delete)
        
        Args:
            business_id: Business ID
            user_id: User ID requesting deletion (must be owner)
            
        Returns:
            Dict with success status
        """
        businesses = self._load_json(self.businesses_file)
        
        if business_id not in businesses:
            return {"success": False, "error": "Business not found"}
        
        if businesses[business_id]["owner_id"] != user_id:
            return {"success": False, "error": "Only owner can delete business"}
        
        del businesses[business_id]
        self._save_json(self.businesses_file, businesses)
        
        return {"success": True}


# Demo function for testing
if __name__ == "__main__":
    manager = BusinessManager()
    
    # Create demo businesses
    print("Creating demo businesses...")
    
    business1 = manager.create_business(
        name="Tech Solutions Ltd",
        owner_id="user-123",
        business_type="Limited Company",
        tax_number="UTR123456789",
        address="123 High Street, London, UK"
    )
    print(f"Business 1: {business1}")
    
    business2 = manager.create_business(
        name="Freelance Consulting",
        owner_id="user-123",
        business_type="Sole Trader",
        tax_number="UTR987654321",
        address="456 Main Road, Manchester, UK"
    )
    print(f"Business 2: {business2}")
    
    # Get user businesses
    print("\nGetting user businesses...")
    user_businesses = manager.get_user_businesses("user-123")
    print(f"Found {len(user_businesses)} businesses for user-123")
    
    for business in user_businesses:
        print(f"  - {business['name']} ({business['business_type']})")
