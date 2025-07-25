"""
Authentication and multi-tenancy support.
"""
import os
import hashlib
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    tenant_id: str
    permissions: Dict[str, bool]

class AuthManager:
    """Simple authentication and multi-tenancy manager."""
    
    def __init__(self):
        self.api_keys: Dict[str, User] = {}
        self.setup_default_user()
    
    def setup_default_user(self):
        """Setup default user for development."""
        default_key = os.environ.get("API_KEY", "dev-key")
        self.api_keys[default_key] = User(
            user_id="default",
            tenant_id="default",
            permissions={"read": True, "write": True, "deploy": True}
        )
    
    def authenticate(self, api_key: str) -> Optional[User]:
        """Authenticate user by API key."""
        return self.api_keys.get(api_key)
    
    def add_user(self, api_key: str, user_id: str, tenant_id: str, 
                permissions: Dict[str, bool]) -> None:
        """Add a new user."""
        self.api_keys[api_key] = User(
            user_id=user_id,
            tenant_id=tenant_id,
            permissions=permissions
        )
    
    def check_permission(self, user: User, permission: str) -> bool:
        """Check if user has specific permission."""
        return user.permissions.get(permission, False)

# Global auth manager instance
auth_manager = AuthManager()