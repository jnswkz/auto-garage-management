# src/presentation/views/main_window.py
"""
Main application window with navigation and content pages.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QLabel,
    QMessageBox,
    QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSignal

from utils.messages import Messages
from presentation.permissions import can_access, PagePermissions
from presentation.views.pages import (
    TiepNhanXePage,
    PhieuSuaChuaPage,
    TraCuuXePage,
    PhieuThuPage,
    BaoCaoDoanhSoPage,
    BaoCaoTonPage,
    QuanLyDanhMucPage,
    ThayDoiQuyDinhPage,
    # QuanLyUserPage,
)


class MainWindow(QMainWindow):
    """Main application window with navigation sidebar and content area."""
    
    # Signal emitted when user requests logout
    logout_requested = pyqtSignal()
    
    # Navigation items: (display_name, page_id, page_class)
    NAV_ITEMS = [
        (Messages.NAV_TIEP_NHAN_XE, PagePermissions.TIEP_NHAN_XE, TiepNhanXePage),
        (Messages.NAV_PHIEU_SUA_CHUA, PagePermissions.PHIEU_SUA_CHUA, PhieuSuaChuaPage),
        (Messages.NAV_TRA_CUU_XE, PagePermissions.TRA_CUU_XE, TraCuuXePage),
        (Messages.NAV_PHIEU_THU, PagePermissions.PHIEU_THU, PhieuThuPage),
        (Messages.NAV_BAO_CAO_DOANH_SO, PagePermissions.BAO_CAO_DOANH_SO, BaoCaoDoanhSoPage),
        (Messages.NAV_BAO_CAO_TON, PagePermissions.BAO_CAO_TON, BaoCaoTonPage),
        (Messages.NAV_QUAN_LY_DANH_MUC, PagePermissions.QUAN_LY_DANH_MUC, QuanLyDanhMucPage),
        (Messages.NAV_THAY_DOI_QUY_DINH, PagePermissions.THAY_DOI_QUY_DINH, ThayDoiQuyDinhPage),
#         (Messages.NAV_QUAN_LY_USER, PagePermissions.QUAN_LY_USER, QuanLyUserPage),
    ]
    
    def __init__(self, role: str, username: str, parent=None):
        super().__init__(parent)
        self._role = role
        self._username = username
        self._page_indices = {}  # page_id -> stack index
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        # Window settings
        self.setWindowTitle(f"{Messages.APP_TITLE} - [{self._role}] {self._username}")
        self.setMinimumSize(1236, 760)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left navigation panel
        nav_widget = self._create_navigation_panel()
        main_layout.addWidget(nav_widget)
        
        # Right content area
        content_widget = self._create_content_area()
        main_layout.addWidget(content_widget, 1)
    
    def _create_navigation_panel(self) -> QWidget:
        """Create the left navigation panel."""
        nav_widget = QWidget()
        nav_widget.setFixedWidth(220)
        nav_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
        """)
        
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        
        # App title in navigation
        title_label = QLabel("GARAGE")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 20px;
                background-color: #1a252f;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(title_label)
        
        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                border: none;
                outline: none;
            }
            QListWidget::item {
                color: #bdc3c7;
                padding: 15px 20px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:hover {
                background-color: #34495e;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # Add navigation items (only show items user can access)
        for display_name, page_id, _ in self.NAV_ITEMS:
            if can_access(self._role, page_id):
                item = QListWidgetItem(display_name)
                item.setData(Qt.ItemDataRole.UserRole, page_id)
                self.nav_list.addItem(item)
        
        self.nav_list.currentRowChanged.connect(self._on_navigation_changed)
        nav_layout.addWidget(self.nav_list)
        
        # User info at bottom
        user_label = QLabel(f"User: {self._username}")
        user_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 11px;
                padding: 15px;
                background-color: #1a252f;
            }
        """)
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(user_label)
        
        # Logout button
        self.logout_button = QPushButton("Đăng xuất")
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 12px 20px;
                border: none;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.logout_button.clicked.connect(self._on_logout_clicked)
        nav_layout.addWidget(self.logout_button)
        
        return nav_widget
    
    def _on_logout_clicked(self):
        """Handle logout button click."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Xac nhan dang xuat")
        msg_box.setText("Ban co chac chan muon dang xuat?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-size: 12px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
            QMessageBox QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
    
    def _create_content_area(self) -> QWidget:
        """Create the right content area with stacked pages."""
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
            }
        """)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked widget for pages
        self.page_stack = QStackedWidget()
        self.page_stack.setStyleSheet("""
            QStackedWidget {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        # Create and add pages (only for accessible pages)
        stack_index = 0
        for _, page_id, page_class in self.NAV_ITEMS:
            if can_access(self._role, page_id):
                page = page_class()
                self.page_stack.addWidget(page)
                self._page_indices[page_id] = stack_index
                stack_index += 1
        
        content_layout.addWidget(self.page_stack)
        
        return content_widget
    
    def _on_navigation_changed(self, index: int):
        """Handle navigation item selection change."""
        if index < 0:
            return
        
        item = self.nav_list.item(index)
        if item is None:
            return
        
        page_id = item.data(Qt.ItemDataRole.UserRole)
        
        # Double-check permission (defense in depth)
        if not can_access(self._role, page_id):
            QMessageBox.warning(
                self,
                Messages.ACCESS_DENIED,
                Messages.ACCESS_DENIED_MSG
            )
            return
        
        # Switch to the page
        if page_id in self._page_indices:
            self.page_stack.setCurrentIndex(self._page_indices[page_id])
    
    def select_first_page(self):
        """Select the first available navigation item."""
        if self.nav_list.count() > 0:
            self.nav_list.setCurrentRow(0)
