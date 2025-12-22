STYLE = """
        QWidget#pageContainer {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
        }

        QLabel#pageTitle {
            font-size: 18px;
            font-weight: 700;
            color: #111827;
            padding-top: 4px;
        }

        QLabel#pageSubtitle {
            color: #6b7280;
            padding-bottom: 6px;
        }

        QGroupBox {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            margin-top: 20px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            top: 0px;
            padding: 0 6px;
            color: #374151;
            font-weight: 600;
        }

        QLabel {
            color: #374151;
        }

        QLineEdit, QTextEdit, QComboBox {
            background: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 6px 8px;
            color: #000000;
        }

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border: 1px solid #2563eb;
        }

        QLineEdit, QTextEdit, QComboBox QAbstractItemView {
            background: #ffffff;
            color: #111827;          /* màu chữ trong dropdown */
            selection-background-color: #2563eb;
            selection-color: #ffffff;
            outline: 0;
        }

        QPushButton {
            border: none;
            border-radius: 6px;
            padding: 7px 14px;
            color: #ffffff;
            background: #2563eb;
        }
        QPushButton#btnReset { background: #6b7280; }
        QPushButton#btnPrint { background: #059669; }

        QPushButton:hover { opacity: 0.92; }

        QDateEdit {
            background: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 6px 8px;
            color: #111827;
        }

        QDateEdit:focus {
            border: 1px solid #2563eb;
        }

        /* ===== Calendar popup ===== */
        QCalendarWidget {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
        }

        /* Header (tháng/năm) */
        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
        }

        QCalendarWidget QToolButton {
            background: transparent;
            color: #111827;
            font-weight: 600;
            padding: 4px 8px;
        }

        QCalendarWidget QToolButton:hover {
            background: #e5e7eb;
            border-radius: 4px;
        }

        /* Bảng ngày */
        QCalendarWidget QTableView {
            background: #ffffff;
            selection-background-color: #2563eb;
            selection-color: #ffffff;
            outline: 0;
        }

        /* Ngày thường */
        QCalendarWidget QTableView::item {
            color: #111827;
            padding: 6px;
        }

        /* Cuối tuần */
        QCalendarWidget QTableView::item:!enabled {
            color: #9ca3af;
        }

        QCalendarWidget QTableView::item:selected {
            background: #2563eb;
            color: #ffffff;
            border-radius: 4px;
        }

        /* Chủ nhật / Thứ bảy (đừng quá đỏ) */
        QCalendarWidget QHeaderView::section {
            background: #f9fafb;
            color: #374151;
            padding: 4px;
            border: none;
        }

        /* Tháng khác (ngày mờ) */
        QCalendarWidget QTableView::item:disabled {
            color: #d1d5db;
        }

        QCalendarWidget QMenu {
            background: #ffffff;
            border: 1px solid #e5e7eb;
        }

        QCalendarWidget QMenu::item {
            padding: 6px 12px;
            color: #111827;
        }

        QCalendarWidget QMenu::item:selected {
            background: #2563eb;
            color: #ffffff;
        }
        QCalendarWidget QSpinBox#qt_calendar_yearedit {
            background: #ffffff;
            color: #111827;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 2px 6px;
            min-width: 56px;
        }

        QCalendarWidget QSpinBox#qt_calendar_yearedit:focus {
            border: 1px solid #2563eb;
        }

        QCalendarWidget QSpinBox#qt_calendar_yearedit QLineEdit {
            background: transparent;
            color: #111827;
            font-weight: 600;
            selection-background-color: #2563eb;
            selection-color: #ffffff;
        }
        QTableWidget#dataTable {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            gridline-color: #e5e7eb;
            background: #ffffff;
            alternate-background-color: #f9fafb;
            color: #111827;
        }

        QHeaderView::section {
            background: #f9fafb;
            color: #374151;
            padding: 8px;
            border: none;
            border-bottom: 1px solid #e5e7eb;
            font-weight: 600;
        }

        /* Hint text (optional) */
        QLabel#hintText {
            color: #6b7280;
        }
        """