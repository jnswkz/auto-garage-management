# src/presentation/views/pages/tra_cuu_xe_page.py
"""
Tra Cuu Xe (Vehicle Lookup) page - BM3 (UI only).
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)

from utils.style import STYLE


class TraCuuXePage(QWidget):
    """BM3: Tra cứu xe (UI-only, mock data)."""

    PAGE_ID = "tra_cuu_xe"

    def __init__(self, parent=None):
        super().__init__(parent)
        # Nếu bạn apply STYLE ở mức app rồi thì có thể bỏ dòng dưới
        self.setStyleSheet(STYLE)

        self._setup_ui()
        self._load_mock_data()
        self._apply_filter()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)
        root.setAlignment(Qt.AlignmentFlag.AlignTop)

        container = QWidget(self)
        container.setObjectName("pageContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(18, 18, 18, 18)
        container_layout.setSpacing(12)

        title = QLabel("TRA CỨU XE (BM3)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Tra cứu theo biển số / chủ xe / hiệu xe. Kết quả hiển thị tiền nợ hiện tại.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setObjectName("pageSubtitle")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        # --- Filter panel ---
        group_filter = QGroupBox("Bộ lọc")
        grid = QGridLayout(group_filter)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        self.inp_plate = QLineEdit()
        self.inp_plate.setPlaceholderText("Biển số (vd: 51F-123.45)")

        self.inp_owner = QLineEdit()
        self.inp_owner.setPlaceholderText("Tên chủ xe")

        self.cb_brand = QComboBox()
        self.cb_brand.addItems(["-- Tất cả hiệu xe --", "Toyota", "Honda", "Suzuki", "Ford", "Kia", "Hyundai"])  # TODO: load DB

        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_search.setObjectName("btnPrimary")
        self.btn_search.clicked.connect(self._apply_filter)

        self.btn_clear = QPushButton("Xóa lọc")
        self.btn_clear.setObjectName("btnReset")
        self.btn_clear.clicked.connect(self._clear_filter)

        self.btn_print = QPushButton("In danh sách")
        self.btn_print.setObjectName("btnPrint")
        self.btn_print.clicked.connect(self._on_print_clicked)

        grid.addWidget(QLabel("Biển số"), 0, 0)
        grid.addWidget(self.inp_plate, 0, 1)
        grid.addWidget(QLabel("Chủ xe"), 0, 2)
        grid.addWidget(self.inp_owner, 0, 3)

        grid.addWidget(QLabel("Hiệu xe"), 1, 0)
        grid.addWidget(self.cb_brand, 1, 1)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(self.btn_search)
        btn_row.addWidget(self.btn_clear)
        btn_row.addWidget(self.btn_print)

        grid.addLayout(btn_row, 1, 2, 1, 2)

        container_layout.addWidget(group_filter)

        # --- Table results ---
        group_result = QGroupBox("Kết quả")
        result_layout = QVBoxLayout(group_result)
        result_layout.setSpacing(10)

        self.table = QTableWidget(0, 5, self)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(["STT", "Biển số", "Hiệu xe", "Chủ xe", "Tiền nợ"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        result_layout.addWidget(self.table)

        self.lbl_count = QLabel("0 kết quả")
        self.lbl_count.setObjectName("hintText")
        result_layout.addWidget(self.lbl_count, alignment=Qt.AlignmentFlag.AlignRight)

        container_layout.addWidget(group_result)

        root.addWidget(container)
        root.addStretch(1)

    # ---------------- Mock + filter ----------------
    def _load_mock_data(self):
        # TODO: thay bằng data từ DB (CAR + CAR_RECEPTION Debt)
        self._rows = [
            {"plate": "51F-123.45", "brand": "Toyota", "owner": "Nguyễn Văn A", "debt": 1200000},
            {"plate": "50H-888.99", "brand": "Honda", "owner": "Trần Thị B", "debt": 0},
            {"plate": "59A-111.22", "brand": "Ford", "owner": "Lê Văn C", "debt": 350000},
            {"plate": "51G-456.78", "brand": "Kia", "owner": "Phạm Minh D", "debt": 9800000},
        ]

    def _apply_filter(self):
        plate_q = self.inp_plate.text().strip().upper()
        owner_q = self.inp_owner.text().strip().lower()
        brand_q = self.cb_brand.currentText()

        filtered = []
        for r in self._rows:
            if plate_q and plate_q not in r["plate"].upper():
                continue
            if owner_q and owner_q not in r["owner"].lower():
                continue
            if brand_q != "-- Tất cả hiệu xe --" and brand_q != r["brand"]:
                continue
            filtered.append(r)

        self._render_table(filtered)

    def _render_table(self, data: list[dict]):
        self.table.setRowCount(0)

        for i, r in enumerate(data, start=1):
            row = self.table.rowCount()
            self.table.insertRow(row)

            self._set_item(row, 0, str(i), align_right=True)
            self._set_item(row, 1, r["plate"])
            self._set_item(row, 2, r["brand"])
            self._set_item(row, 3, r["owner"])
            self._set_item(row, 4, self._fmt_money(r["debt"]), align_right=True)

        self.lbl_count.setText(f"{len(data)} kết quả")

    def _set_item(self, row: int, col: int, text: str, align_right: bool = False):
        item = QTableWidgetItem(text)
        if align_right:
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, col, item)

    def _clear_filter(self):
        self.inp_plate.clear()
        self.inp_owner.clear()
        self.cb_brand.setCurrentIndex(0)
        self._apply_filter()

    def _on_print_clicked(self):
        # MVP: preview print (sau này thay QPrinter)
        QMessageBox.information(self, "In danh sách (demo)", "Chức năng in danh sách sẽ làm sau.")

    def _fmt_money(self, v: int) -> str:
        return f"{v:,}"
