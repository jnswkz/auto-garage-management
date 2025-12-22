# src/presentation/views/pages/bao_cao_ton_kho_page.py

from __future__ import annotations

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QLineEdit,
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


class BaoCaoTonPage(QWidget):
    """BM6: Báo cáo tồn kho (UI-only)."""

    PAGE_ID = "bao_cao_ton_kho"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE)

        self._setup_ui()
        self._init_default_month_year()

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

        title = QLabel("BÁO CÁO TỒN KHO")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Chọn tháng/năm để lập báo cáo tồn kho vật tư/phụ tùng.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setObjectName("pageSubtitle")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        # --- Filter ---
        group_filter = QGroupBox("Tham số báo cáo")
        grid = QGridLayout(group_filter)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        self.cb_month = QComboBox()
        self.cb_month.addItems([str(i) for i in range(1, 13)])

        self.inp_year = QLineEdit()
        self.inp_year.setPlaceholderText("Năm (VD: 2026)")
        self.inp_year.setValidator(QIntValidator(2000, 2100, self))

        self.btn_build = QPushButton("Lập báo cáo")
        self.btn_build.setObjectName("btnPrimary")
        self.btn_build.clicked.connect(self._on_build_clicked)

        self.btn_clear = QPushButton("Làm mới")
        self.btn_clear.setObjectName("btnReset")
        self.btn_clear.clicked.connect(self._on_clear_clicked)

        self.btn_print = QPushButton("In báo cáo")
        self.btn_print.setObjectName("btnPrint")
        self.btn_print.clicked.connect(self._on_print_clicked)

        grid.addWidget(QLabel("Tháng *"), 0, 0)
        grid.addWidget(self.cb_month, 0, 1)
        grid.addWidget(QLabel("Năm *"), 0, 2)
        grid.addWidget(self.inp_year, 0, 3)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(self.btn_build)
        btn_row.addWidget(self.btn_clear)
        btn_row.addWidget(self.btn_print)

        grid.addLayout(btn_row, 1, 0, 1, 4)
        container_layout.addWidget(group_filter)

        # --- Result ---
        group_result = QGroupBox("Kết quả báo cáo")
        result_layout = QVBoxLayout(group_result)
        result_layout.setSpacing(10)

        self.table = QTableWidget(0, 6, self)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(
            ["STT", "Vật tư/Phụ tùng", "Tồn đầu", "Nhập", "Xuất", "Tồn cuối"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        result_layout.addWidget(self.table)

        bottom = QHBoxLayout()
        self.lbl_count = QLabel("0 dòng")
        self.lbl_count.setObjectName("hintText")

        self.lbl_note = QLabel("Gợi ý: Tồn cuối = Tồn đầu + Nhập - Xuất")
        self.lbl_note.setObjectName("hintText")

        bottom.addWidget(self.lbl_note)
        bottom.addStretch(1)
        bottom.addWidget(self.lbl_count)

        result_layout.addLayout(bottom)

        container_layout.addWidget(group_result)

        root.addWidget(container)
        root.addStretch(1)

    def _init_default_month_year(self):
        today = QDate.currentDate()
        self.cb_month.setCurrentIndex(today.month() - 1)
        self.inp_year.setText(str(today.year()))

    # ---------------- Actions ----------------
    def _on_build_clicked(self):
        year_text = self.inp_year.text().strip()
        if not year_text:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập năm.")
            return

        month = int(self.cb_month.currentText())
        year = int(year_text)

        # UI-only: mock report data
        rows = self._mock_inventory_report(month, year)
        self._render(rows)

    def _on_clear_clicked(self):
        self._init_default_month_year()
        self.table.setRowCount(0)
        self.lbl_count.setText("0 dòng")

    def _on_print_clicked(self):
        if self.table.rowCount() == 0:
            QMessageBox.information(self, "In báo cáo (demo)", "Chưa có dữ liệu để in. Hãy lập báo cáo trước.")
            return
        QMessageBox.information(self, "In báo cáo (demo)", "Chức năng in báo cáo tồn kho sẽ làm sau (QPrinter).")

    # ---------------- Render ----------------
    def _render(self, rows: list[dict]):
        self.table.setRowCount(0)

        for i, r in enumerate(rows, start=1):
            row = self.table.rowCount()
            self.table.insertRow(row)

            ton_cuoi = r["opening"] + r["in"] - r["out"]

            self._set_item(row, 0, str(i), align_right=True)
            self._set_item(row, 1, r["name"])
            self._set_item(row, 2, str(r["opening"]), align_right=True)
            self._set_item(row, 3, str(r["in"]), align_right=True)
            self._set_item(row, 4, str(r["out"]), align_right=True)
            self._set_item(row, 5, str(ton_cuoi), align_right=True)

        self.lbl_count.setText(f"{len(rows)} dòng")

    def _set_item(self, row: int, col: int, text: str, align_right: bool = False):
        item = QTableWidgetItem(text)
        if align_right:
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, col, item)

    # ---------------- Mock data ----------------
    def _mock_inventory_report(self, month: int, year: int) -> list[dict]:
        """
        TODO (DB thật):
        - opening: tồn cuối tháng trước
        - in: tổng nhập trong tháng (phiếu nhập / phát sinh)
        - out: tổng xuất trong tháng (dựa theo phiếu sửa chữa dùng vật tư)
        """
        seed = (year * 100 + month) % 5

        base = [
            {"name": "Dầu nhớt", "opening": 30 + seed * 2, "in": 20 + seed, "out": 25 + seed},
            {"name": "Lọc gió", "opening": 18 + seed, "in": 10 + seed, "out": 12 + seed},
            {"name": "Bugi", "opening": 40 + seed * 3, "in": 15 + seed, "out": 20 + seed},
            {"name": "Má phanh", "opening": 12 + seed, "in": 6 + seed, "out": 5 + seed},
        ]
        return base
