# src/presentation/controllers/login_controller.py
"""
Login controller for handling authentication logic.
"""

from typing import Optional, Tuple

from app.session import current_session, UserSession
from presentation.permissions import Roles


# Temporary user database (no real DB)
TEMP_USERS = {
    "admin": {"password": "admin", "role": Roles.ADMIN},
    "staff": {"password": "staff", "role": Roles.STAFF},
}


class LoginController:
    """Controller for handling login authentication."""
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticate user with given credentials.
        
        Args:
            username: The username to authenticate
            password: The password to verify
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
            If successful, error_message is None.
            If failed, error_message contains the reason.
        """
        # Check if user exists
        if username not in TEMP_USERS:
            return False, "Ten dang nhap hoac mat khau khong dung!"
        
        user_data = TEMP_USERS[username]
        
        # Verify password
        if user_data["password"] != password:
            return False, "Ten dang nhap hoac mat khau khong dung!"
        
        # Create session
        user_session = UserSession(
            username=username,
            role=user_data["role"]
        )
        current_session.current_user = user_session
        
        return True, None
    
    def logout(self):
        """Log out the current user."""
        current_session.logout()
    
    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return current_session.is_logged_in()
    
    def get_current_role(self) -> Optional[str]:
        """Get the role of the current logged-in user."""
        return current_session.get_role()
    
    def get_current_username(self) -> Optional[str]:
        """Get the username of the current logged-in user."""
        if current_session.current_user:
            return current_session.current_user.username
        return None
