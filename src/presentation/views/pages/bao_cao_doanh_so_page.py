# src/presentation/views/pages/bao_cao_doanh_so_page.py

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
from services.revenue_report_service import RevenueReportService


class BaoCaoDoanhSoPage(QWidget):
    """BM5: Báo cáo doanh thu tháng."""

    PAGE_ID = "bao_cao_doanh_so"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE)
        
        self.service = RevenueReportService()

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

        title = QLabel("BÁO CÁO DOANH THU THÁNG")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Chọn tháng/năm để lập báo cáo doanh thu theo hiệu xe.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # --- Results ---
        group_result = QGroupBox("Kết quả báo cáo")
        result_layout = QVBoxLayout(group_result)
        result_layout.setSpacing(10)

        self.table = QTableWidget(0, 5, self)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(["STT", "Hiệu xe", "Số lượt sửa", "Thành tiền", "Tỷ lệ (%)"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        result_layout.addWidget(self.table)

        # Total revenue
        total_row = QHBoxLayout()
        total_row.addStretch(1)

        self.lbl_total_title = QLabel("Tổng doanh thu:")
        self.lbl_total_title.setObjectName("hintText")

        self.lbl_total_value = QLabel("0")
        self.lbl_total_value.setObjectName("moneyBig")
        self.lbl_total_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        total_row.addWidget(self.lbl_total_title)
        total_row.addWidget(self.lbl_total_value)

        result_layout.addLayout(total_row)

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
        
        try:
            # Get or create report from database
            report = self.service.get_or_create_monthly_report(month, year)
            
            # Transform data for rendering
            data = [
                {
                    'brand': detail['brand_name'],
                    'count': detail['count'],
                    'amount': detail['total_money']
                }
                for detail in report['details']
            ]
            
            self._render_report(data)
            
            if not data:
                QMessageBox.information(
                    self,
                    "Thông báo",
                    f"Không có dữ liệu sửa chữa trong tháng {month}/{year}."
                )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể lập báo cáo: {str(e)}"
            )

    def _on_clear_clicked(self):
        self._init_default_month_year()
        self.table.setRowCount(0)
        self.lbl_total_value.setText("0")

    def _on_print_clicked(self):
        if self.table.rowCount() == 0:
            QMessageBox.information(self, "In báo cáo (demo)", "Chưa có dữ liệu để in. Hãy lập báo cáo trước.")
            return
        QMessageBox.information(self, "In báo cáo (demo)", "Chức năng in báo cáo sẽ làm sau (QPrinter).")

    # ---------------- Render ----------------
    def _render_report(self, rows: list[dict]):
        self.table.setRowCount(0)

        total = sum(r["amount"] for r in rows) if rows else 0

        for i, r in enumerate(rows, start=1):
            row = self.table.rowCount()
            self.table.insertRow(row)

            ratio = 0.0
            if total > 0:
                ratio = (r["amount"] / total) * 100.0

            self._set_item(row, 0, str(i), align_right=True)
            self._set_item(row, 1, r["brand"])
            self._set_item(row, 2, str(r["count"]), align_right=True)
            self._set_item(row, 3, self._fmt_money(r["amount"]), align_right=True)
            self._set_item(row, 4, f"{ratio:.2f}", align_right=True)

        self.lbl_total_value.setText(self._fmt_money(total))

    def _set_item(self, row: int, col: int, text: str, align_right: bool = False):
        item = QTableWidgetItem(text)
        if align_right:
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, col, item)

    def _fmt_money(self, v: int) -> str:
        return f"{v:,}"
