# src/app/session.py
"""
Session management module.
Stores the current user session information.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UserSession:
    """Represents a user session with username and role."""
    username: str
    role: str  # "ADMIN" or "STAFF"


class SessionManager:
    """
    Manages the current user session.
    Singleton-like pattern using module-level instance.
    """
    
    def __init__(self):
        self._current_user: Optional[UserSession] = None
    
    @property
    def current_user(self) -> Optional[UserSession]:
        """Get the current logged-in user."""
        return self._current_user
    
    @current_user.setter
    def current_user(self, user: Optional[UserSession]):
        """Set the current logged-in user."""
        self._current_user = user
    
    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self._current_user is not None
    
    def get_role(self) -> Optional[str]:
        """Get the role of the current user."""
        if self._current_user:
            return self._current_user.role
        return None
    
    def logout(self):
        """Clear the current session."""
        self._current_user = None


# Global session instance
current_session = SessionManager()
