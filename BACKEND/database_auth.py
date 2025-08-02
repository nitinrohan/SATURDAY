import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta

class DatabaseAuth:
    def __init__(self, db_file="users.db"):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user if not exists
        cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@example.com',))
        if not cursor.fetchone():
            admin_password_hash = self.hash_password("admin123")
            cursor.execute('''
                INSERT INTO users (email, password_hash, name, created_at)
                VALUES (?, ?, ?, ?)
            ''', ('admin@example.com', admin_password_hash, 'Admin User', datetime.now()))
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256 with salt"""
        salt = "SATURDAY_SALT_2024"  # In production, use unique salt per user
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register_user(self, email, password, name):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                return {"success": False, "message": "User already exists"}
            
            # Create new user
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (email, password_hash, name, created_at)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, name, datetime.now()))
            
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "User registered successfully"}
            
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def login_user(self, email, password):
        """Login a user"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Find user
            cursor.execute('SELECT id, password_hash, name FROM users WHERE email = ? AND is_active = 1', (email,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return {"success": False, "message": "Invalid email or password"}
            
            user_id, stored_password_hash, name = user_data
            
            # Verify password
            if stored_password_hash != self.hash_password(password):
                return {"success": False, "message": "Invalid email or password"}
            
            # Update last login
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', (datetime.now(), user_id))
            
            # Create session
            session_id = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            cursor.execute('''
                INSERT INTO sessions (session_id, user_id, expires_at)
                VALUES (?, ?, ?)
            ''', (session_id, user_id, expires_at))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": "Login successful",
                "session_id": session_id,
                "user": {
                    "id": user_id,
                    "email": email,
                    "name": name
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Login failed: {str(e)}"}
    
    def validate_session(self, session_id):
        """Validate a session"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Find session
            cursor.execute('''
                SELECT s.id, s.expires_at, u.id, u.email, u.name
                FROM sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.session_id = ? AND u.is_active = 1
            ''', (session_id,))
            
            session_data = cursor.fetchone()
            
            if not session_data:
                return {"valid": False, "message": "Invalid session"}
            
            session_db_id, expires_at, user_id, email, name = session_data
            expires_at = datetime.fromisoformat(expires_at)
            
            if datetime.now() > expires_at:
                # Remove expired session
                cursor.execute('DELETE FROM sessions WHERE id = ?', (session_db_id,))
                conn.commit()
                conn.close()
                return {"valid": False, "message": "Session expired"}
            
            conn.close()
            
            return {
                "valid": True,
                "user": {
                    "id": user_id,
                    "email": email,
                    "name": name
                }
            }
            
        except Exception as e:
            return {"valid": False, "message": f"Session validation failed: {str(e)}"}
    
    def logout_user(self, session_id):
        """Logout a user"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "Logout successful"}
            
        except Exception as e:
            return {"success": False, "message": f"Logout failed: {str(e)}"}
    
    def get_user_profile(self, user_id):
        """Get user profile information"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, name, created_at, last_login
                FROM users WHERE id = ? AND is_active = 1
            ''', (user_id,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if not user_data:
                return {"success": False, "message": "User not found"}
            
            user_id, email, name, created_at, last_login = user_data
            
            return {
                "success": True,
                "user": {
                    "id": user_id,
                    "email": email,
                    "name": name,
                    "created_at": created_at,
                    "last_login": last_login
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Failed to get profile: {str(e)}"}
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM sessions WHERE expires_at < ?', (datetime.now(),))
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            return {"success": True, "deleted_sessions": deleted_count}
            
        except Exception as e:
            return {"success": False, "message": f"Cleanup failed: {str(e)}"}

# Example usage
if __name__ == "__main__":
    auth = DatabaseAuth()
    
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
        
        # Get user profile
        user_id = result["user"]["id"]
        profile = auth.get_user_profile(user_id)
        print("Profile:", profile) 