# src/main.py
"""
Auto Garage Management System
Main entry point for the PyQt6 desktop application.

Run with: cd src && python main.py
"""

import sys
import os

# Add src directory to Python path for absolute imports
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from presentation.controllers.main_controller import MainController


def main():
    """Main entry point for the application."""
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Auto Garage Management")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Garage Co.")
    
    # Set global application style
    app.setStyleSheet("""
        QWidget {
            font-family: "Segoe UI", Arial, sans-serif;
        }
        QMessageBox {
            background-color: white;
        }
        QMessageBox QLabel {
            color: #2c3e50;
            font-size: 13px;
        }
        QMessageBox QPushButton {
            padding: 6px 20px;
            min-width: 60px;
        }
    """)
    
    # Create and start main controller
    controller = MainController()
    
    if not controller.start():
        # User cancelled login
        sys.exit(0)
    
    # Run application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
