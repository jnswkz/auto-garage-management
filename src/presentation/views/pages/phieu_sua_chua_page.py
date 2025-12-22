# src/presentation/views/pages/phieu_sua_chua_page.py
"""
Phieu Sua Chua (Repair Order) page.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from utils.messages import Messages


class PhieuSuaChuaPage(QWidget):
    """Page for creating repair orders."""
    
    PAGE_ID = "phieu_sua_chua"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Title label
        title_label = QLabel(Messages.PAGE_PHIEU_SUA_CHUA_TITLE)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 20px 0;
            }
        """)
        layout.addWidget(title_label)
        
        # Description label
        desc_label = QLabel(Messages.PAGE_PHIEU_SUA_CHUA_DESC)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                padding-bottom: 20px;
            }
        """)
        layout.addWidget(desc_label)
        
        # Placeholder content
        placeholder = QLabel("[ Noi dung trang Phieu sua chua se duoc phat trien o day ]")
        placeholder.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #95a5a6;
                font-style: italic;
                padding: 40px;
                background-color: #ecf0f1;
                border-radius: 8px;
            }
        """)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        layout.addStretch()
