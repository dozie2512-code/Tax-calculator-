"""
Authentication and User Management Module
Handles user authentication, session management, and user-business associations
"""

import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path


class AuthenticationSystem:
    """Manages user authentication and session management"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize authentication system
        
        Args:
            data_dir: Directory to store user and session data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.users_file = self.data_dir / "users.json"
        self.sessions_file = self.data_dir / "sessions.json"
        
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage files if they don't exist"""
        if not self.users_file.exists():
            self._save_json(self.users_file, {})
        
        if not self.sessions_file.exists():
            self._save_json(self.sessions_file, {})
    
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
    
    def _hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256 with salt
        Note: For production use, consider bcrypt, scrypt, or Argon2
        """
        # Add a simple salt for basic protection (still not production-ready)
        salt = "taxcalc_salt_2024"  # In production, use per-user random salt
        salted = salt + password + salt
        return hashlib.sha256(salted.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str, 
                     full_name: str = "") -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            username: Unique username
            password: User password
            email: User email address
            full_name: User's full name
            
        Returns:
            Dict with user information or error
        """
        users = self._load_json(self.users_file)
        
        if username in users:
            return {"success": False, "error": "Username already exists"}
        
        user_id = str(uuid.uuid4())
        users[username] = {
            "user_id": user_id,
            "username": username,
            "password": self._hash_password(password),
            "email": email,
            "full_name": full_name,
            "created_at": datetime.now().isoformat(),
            "businesses": []
        }
        
        self._save_json(self.users_file, users)
        
        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name
        }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and create session
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Dict with session token or error
        """
        users = self._load_json(self.users_file)
        
        if username not in users:
            return {"success": False, "error": "Invalid credentials"}
        
        user = users[username]
        if user["password"] != self._hash_password(password):
            return {"success": False, "error": "Invalid credentials"}
        
        # Create session
        session_token = str(uuid.uuid4())
        sessions = self._load_json(self.sessions_file)
        
        sessions[session_token] = {
            "user_id": user["user_id"],
            "username": username,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        self._save_json(self.sessions_file, sessions)
        
        return {
            "success": True,
            "session_token": session_token,
            "user": {
                "user_id": user["user_id"],
                "username": username,
                "email": user["email"],
                "full_name": user["full_name"],
                "businesses": user["businesses"]
            }
        }
    
    def logout(self, session_token: str) -> Dict[str, Any]:
        """
        Logout user and invalidate session
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            Dict with success status
        """
        sessions = self._load_json(self.sessions_file)
        
        if session_token in sessions:
            del sessions[session_token]
            self._save_json(self.sessions_file, sessions)
        
        return {"success": True}
    
    def validate_session(self, session_token: str) -> Dict[str, Any]:
        """
        Validate session token
        
        Args:
            session_token: Session token to validate
            
        Returns:
            Dict with user information or error
        """
        sessions = self._load_json(self.sessions_file)
        
        if session_token not in sessions:
            return {"success": False, "error": "Invalid session"}
        
        session = sessions[session_token]
        expires_at = datetime.fromisoformat(session["expires_at"])
        
        if datetime.now() > expires_at:
            del sessions[session_token]
            self._save_json(self.sessions_file, sessions)
            return {"success": False, "error": "Session expired"}
        
        return {
            "success": True,
            "user_id": session["user_id"],
            "username": session["username"]
        }
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user information
        
        Args:
            username: Username to retrieve
            
        Returns:
            User information dict or None
        """
        users = self._load_json(self.users_file)
        
        if username not in users:
            return None
        
        user = users[username].copy()
        user.pop("password", None)  # Remove password from response
        return user
    
    def add_business_to_user(self, username: str, business_id: str) -> Dict[str, Any]:
        """
        Associate a business with a user
        
        Args:
            username: Username
            business_id: Business ID to associate
            
        Returns:
            Dict with success status
        """
        users = self._load_json(self.users_file)
        
        if username not in users:
            return {"success": False, "error": "User not found"}
        
        if business_id not in users[username]["businesses"]:
            users[username]["businesses"].append(business_id)
            self._save_json(self.users_file, users)
        
        return {"success": True}


# Demo function for testing
if __name__ == "__main__":
    auth = AuthenticationSystem()
    
    # Register demo users
    print("Registering demo users...")
    result = auth.register_user("john_doe", "password123", "john@example.com", "John Doe")
    print(f"User 1: {result}")
    
    result = auth.register_user("jane_smith", "password456", "jane@example.com", "Jane Smith")
    print(f"User 2: {result}")
    
    # Test login
    print("\nTesting login...")
    login_result = auth.login("john_doe", "password123")
    print(f"Login result: {login_result}")
    
    if login_result["success"]:
        token = login_result["session_token"]
        
        # Validate session
        print("\nValidating session...")
        validation = auth.validate_session(token)
        print(f"Validation result: {validation}")
        
        # Logout
        print("\nLogging out...")
        logout_result = auth.logout(token)
        print(f"Logout result: {logout_result}")
