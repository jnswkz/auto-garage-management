# src/presentation/views/pages/phieu_thu_page.py
"""
Phieu Thu (Payment Receipt) page.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from utils.messages import Messages


class PhieuThuPage(QWidget):
    """Page for creating payment receipts."""
    
    PAGE_ID = "phieu_thu"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Title label
        title_label = QLabel(Messages.PAGE_PHIEU_THU_TITLE)
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
        desc_label = QLabel(Messages.PAGE_PHIEU_THU_DESC)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                padding-bottom: 20px;
            }
        """)
        layout.addWidget(desc_label)
        
        # Placeholder content
        placeholder = QLabel("[ Noi dung trang Phieu thu tien se duoc phat trien o day ]")
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
