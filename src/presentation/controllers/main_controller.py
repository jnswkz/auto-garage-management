# src/presentation/controllers/main_controller.py
"""
Main controller for coordinating the application flow.
"""

from typing import Optional

from PyQt6.QtWidgets import QApplication, QMessageBox

from app.session import current_session
from presentation.views.login_dialog import LoginDialog
from presentation.views.main_window import MainWindow
from presentation.controllers.login_controller import LoginController
from utils.messages import Messages


class MainController:
    """
    Main application controller.
    Handles the flow between login and main window.
    """
    
    def __init__(self):
        self._login_controller = LoginController()
        self._main_window: Optional[MainWindow] = None
    
    def start(self) -> bool:
        """
        Start the application.
        Shows login dialog and then main window on success.
        
        Returns:
            True if application should continue, False to exit.
        """
        # Show login dialog
        if not self._show_login():
            return False
        
        # Show main window
        self._show_main_window()
        return True
    
    def _show_login(self) -> bool:
        """
        Show login dialog and authenticate user.
        
        Returns:
            True if login successful, False if user cancelled.
        """
        while True:
            login_dialog = LoginDialog()
            result = login_dialog.exec()
            
            # User closed dialog
            if result != LoginDialog.DialogCode.Accepted:
                return False
            
            # Get credentials
            username, password = login_dialog.get_credentials()
            
            # Validate inputs
            if not username or not password:
                QMessageBox.warning(
                    None,
                    Messages.LOGIN_FAILED,
                    "Vui long nhap day du ten dang nhap va mat khau!"
                )
                continue
            
            # Attempt authentication
            success, error_message = self._login_controller.authenticate(
                username, password
            )
            
            if success:
                return True
            else:
                QMessageBox.warning(
                    None,
                    Messages.LOGIN_FAILED,
                    error_message or Messages.LOGIN_FAILED_MSG
                )
                # Continue loop to show login dialog again
    
    def _show_main_window(self):
        """Show the main application window."""
        role = self._login_controller.get_current_role()
        username = self._login_controller.get_current_username()
        
        if role is None or username is None:
            raise RuntimeError("User not logged in")
        
        self._main_window = MainWindow(role=role, username=username)
        self._main_window.logout_requested.connect(self._on_logout)
        self._main_window.select_first_page()
        self._main_window.show()
    
    def _on_logout(self):
        """Handle logout request from main window."""
        # Close main window
        if self._main_window:
            self._main_window.close()
            self._main_window = None
        
        # Clear session
        self._login_controller.logout()
        
        # Show login dialog again
        if self._show_login():
            self._show_main_window()
        else:
            # User cancelled login, quit application
            QApplication.quit()
    
    def get_main_window(self) -> Optional[MainWindow]:
        """Get the main window instance."""
        return self._main_window
