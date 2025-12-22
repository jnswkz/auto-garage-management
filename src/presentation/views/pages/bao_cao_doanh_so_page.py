# src/presentation/views/pages/bao_cao_doanh_so_page.py
"""
Bao Cao Doanh So (Revenue Report) page.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from utils.messages import Messages


class BaoCaoDoanhSoPage(QWidget):
    """Page for viewing revenue reports."""
    
    PAGE_ID = "bao_cao_doanh_so"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Title label
        title_label = QLabel(Messages.PAGE_BAO_CAO_DOANH_SO_TITLE)
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
        desc_label = QLabel(Messages.PAGE_BAO_CAO_DOANH_SO_DESC)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                padding-bottom: 20px;
            }
        """)
        layout.addWidget(desc_label)
        
        # Placeholder content
        placeholder = QLabel("[ Noi dung trang Bao cao doanh so se duoc phat trien o day ]")
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
