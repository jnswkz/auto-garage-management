# src/presentation/views/login_dialog.py
"""
Login dialog for user authentication.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
)
from PyQt6.QtCore import Qt

from utils.messages import Messages


class LoginDialog(QDialog):
    """Dialog for user login with username and password fields."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._username = ""
        self._password = ""
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(Messages.LOGIN_TITLE)
        self.setFixedSize(550, 300)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel(Messages.APP_TITLE)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tên đăng nhập")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow(Messages.LOGIN_USERNAME, self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow(Messages.LOGIN_PASSWORD, self.password_input)
        
        main_layout.addLayout(form_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Login button
        self.login_button = QPushButton(Messages.LOGIN_BUTTON)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 30px;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.login_button.clicked.connect(self._on_login_clicked)
        button_layout.addWidget(self.login_button)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Enter key triggers login
        self.password_input.returnPressed.connect(self._on_login_clicked)
        self.username_input.returnPressed.connect(self._on_login_clicked)
    
    def _on_login_clicked(self):
        """Handle login button click."""
        self._username = self.username_input.text().strip()
        self._password = self.password_input.text()
        self.accept()
    
    def get_credentials(self) -> tuple:
        """
        Get the entered credentials.
        
        Returns:
            Tuple of (username, password)
        """
        return self._username, self._password
    
    def clear_password(self):
        """Clear the password field."""
        self.password_input.clear()
        self.password_input.setFocus()
