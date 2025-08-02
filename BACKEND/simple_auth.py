import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta

class SimpleAuth:
    def __init__(self, users_file="users.json", sessions_file="sessions.json"):
        self.users_file = users_file
        self.sessions_file = sessions_file
        self.load_users()
        self.load_sessions()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            # Create a default admin user
            self.users["admin@example.com"] = {
                "password": self.hash_password("admin123"),
                "name": "Admin User",
                "created_at": datetime.now().isoformat()
            }
            self.save_users()
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def load_sessions(self):
        """Load active sessions from JSON file"""
        if os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'r') as f:
                self.sessions = json.load(f)
        else:
            self.sessions = {}
    
    def save_sessions(self):
        """Save sessions to JSON file"""
        with open(self.sessions_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email, password, name):
        """Register a new user"""
        if email in self.users:
            return {"success": False, "message": "User already exists"}
        
        self.users[email] = {
            "password": self.hash_password(password),
            "name": name,
            "created_at": datetime.now().isoformat()
        }
        self.save_users()
        return {"success": True, "message": "User registered successfully"}
    
    def login_user(self, email, password):
        """Login a user"""
        if email not in self.users:
            return {"success": False, "message": "Invalid email or password"}
        
        user = self.users[email]
        if user["password"] != self.hash_password(password):
            return {"success": False, "message": "Invalid email or password"}
        
        # Create session
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "email": email,
            "name": user["name"],
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        self.save_sessions()
        
        return {
            "success": True,
            "message": "Login successful",
            "session_id": session_id,
            "user": {
                "email": email,
                "name": user["name"]
            }
        }
    
    def validate_session(self, session_id):
        """Validate a session"""
        if session_id not in self.sessions:
            return {"valid": False, "message": "Invalid session"}
        
        session = self.sessions[session_id]
        expires_at = datetime.fromisoformat(session["expires_at"])
        
        if datetime.now() > expires_at:
            # Remove expired session
            del self.sessions[session_id]
            self.save_sessions()
            return {"valid": False, "message": "Session expired"}
        
        return {
            "valid": True,
            "user": {
                "email": session["email"],
                "name": session["name"]
            }
        }
    
    def logout_user(self, session_id):
        """Logout a user"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()
        return {"success": True, "message": "Logout successful"}
    
    def get_all_users(self):
        """Get all users (for admin purposes)"""
        return {
            email: {
                "name": user["name"],
                "created_at": user["created_at"]
            }
            for email, user in self.users.items()
        }

# Example usage
if __name__ == "__main__":
    auth = SimpleAuth()
    
    # Register a new user
    result = auth.register_user("test@example.com", "password123", "Test User")
    print("Register:", result)
    
    # Login
    result = auth.login_user("test@example.com", "password123")
    print("Login:", result)
    
    # Validate session
    if result["success"]:
        session_id = result["session_id"]
        validation = auth.validate_session(session_id)
        print("Session validation:", validation) 