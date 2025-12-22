# src/presentation/views/pages/nhap_vat_tu_page.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QDateEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from utils.style import STYLE


@dataclass(frozen=True)
class SupplyRow:
    name: str
    price: int
    stock: int


class NhapVatTuPage(QWidget):
    """Page nhập vật tư (UI-only)."""

    PAGE_ID = "nhap_vat_tu"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE)

        # TODO: thay bằng service load từ DB (SUPPLIES)
        self._supplies: List[SupplyRow] = self._mock_supplies()

        self._setup_ui()
        self._render_table()

    # ---------------- UI ----------------
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

        title = QLabel("NHẬP VẬT TƯ / PHỤ TÙNG")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Chọn vật tư và nhập số lượng cần nhập (phiếu nhập).")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setObjectName("pageSubtitle")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        # --- Info row ---
        group_info = QGroupBox("Thông tin phiếu nhập")
        grid = QGridLayout(group_info)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        self.import_date = QDateEdit()
        self.import_date.setCalendarPopup(True)
        self.import_date.setDate(QDate.currentDate())



        self.lbl_selected = QLabel("0 dòng nhập")
        self.lbl_selected.setObjectName("hintText")
        self.lbl_selected.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        grid.addWidget(QLabel("Ngày nhập *"), 0, 0)
        grid.addWidget(self.import_date, 0, 1)
        grid.addWidget(self.lbl_selected, 0, 2, 1, 1)

        container_layout.addWidget(group_info)

        # --- Table ---
        group_table = QGroupBox("Danh sách vật tư")
        table_layout = QVBoxLayout(group_table)
        table_layout.setSpacing(10)

        # columns: STT | Tên | Đơn giá | Tồn hiện tại | SL nhập | (optional) Thành tiền nhập
        self.table = QTableWidget(0, 5, self)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(["STT", "Vật tư/Phụ tùng", "Đơn giá", "Tồn hiện tại", "Số lượng nhập"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 140)

        self.table.verticalHeader().setDefaultSectionSize(56)

        table_layout.addWidget(self.table)

        # hint
        hint = QLabel("Nhập số lượng > 0 ở cột “Số lượng nhập”, rồi bấm Lưu phiếu nhập.")
        hint.setObjectName("hintText")
        hint.setWordWrap(True)
        table_layout.addWidget(hint)

        container_layout.addWidget(group_table)

        # --- Actions ---
        actions = QHBoxLayout()
        actions.addStretch(1)

        self.btn_save = QPushButton("Lưu phiếu nhập")
        self.btn_save.setObjectName("btnPrimary")
        self.btn_save.clicked.connect(self._on_save_clicked)

        self.btn_reset = QPushButton("Làm mới")
        self.btn_reset.setObjectName("btnReset")
        self.btn_reset.clicked.connect(self._on_reset_clicked)

        actions.addWidget(self.btn_save)
        actions.addWidget(self.btn_reset)

        container_layout.addLayout(actions)

        root.addWidget(container)
        root.addStretch(1)

    # ---------------- Render ----------------
    def _render_table(self):
        self.table.setRowCount(0)

        for i, s in enumerate(self._supplies, start=1):
            r = self.table.rowCount()
            self.table.insertRow(r)

            # STT
            it_stt = QTableWidgetItem(str(i))
            it_stt.setFlags(it_stt.flags() & ~Qt.ItemFlag.ItemIsEditable)
            it_stt.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(r, 0, it_stt)

            # Name
            it_name = QTableWidgetItem(s.name)
            it_name.setFlags(it_name.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(r, 1, it_name)

            # Price
            it_price = QTableWidgetItem(self._fmt_money(s.price))
            it_price.setFlags(it_price.flags() & ~Qt.ItemFlag.ItemIsEditable)
            it_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(r, 2, it_price)

            # Stock
            it_stock = QTableWidgetItem(str(s.stock))
            it_stock.setFlags(it_stock.flags() & ~Qt.ItemFlag.ItemIsEditable)
            it_stock.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(r, 3, it_stock)

            # Import qty (editable widget)
            qty = QLineEdit("0")
            qty.setValidator(QIntValidator(0, 999999, self))
            qty.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            qty.textChanged.connect(self._update_selected_count)

            self.table.setCellWidget(r, 4, qty)
            self.table.setRowHeight(r, 56)

        self._update_selected_count()

    # ---------------- Data helpers ----------------
    def get_import_lines(self) -> list[dict]:
        """Lấy các dòng có số lượng nhập > 0."""
        lines = []
        for r in range(self.table.rowCount()):
            name = self.table.item(r, 1).text()
            price = self._parse_money(self.table.item(r, 2).text())
            stock = int(self.table.item(r, 3).text() or "0")

            qty_edit: QLineEdit = self.table.cellWidget(r, 4)
            qty = int(qty_edit.text() or "0")

            if qty > 0:
                lines.append(
                    {
                        "name": name,
                        "price": price,
                        "stock_before": stock,
                        "import_qty": qty,
                        "stock_after": stock + qty,
                        "line_money": qty * price,
                    }
                )
        return lines

    def _update_selected_count(self):
        count = len(self.get_import_lines())
        self.lbl_selected.setText(f"{count} dòng nhập")

    # ---------------- Actions ----------------
    def _on_save_clicked(self):
        lines = self.get_import_lines()
        if not lines:
            QMessageBox.information(self, "Lưu phiếu nhập", "Chưa có dòng nào có số lượng nhập > 0.")
            return

        # UI-only preview
        total_money = sum(x["line_money"] for x in lines)
        text_lines = []
        for i, x in enumerate(lines, start=1):
            text_lines.append(
                f"{i}. {x['name']} | SL nhập: {x['import_qty']} | Tồn: {x['stock_before']} -> {x['stock_after']} | Tiền: {self._fmt_money(x['line_money'])}"
            )

        QMessageBox.information(
            self,
            "Phiếu nhập (demo)",
            "Ngày nhập: "
            + self.import_date.date().toString("yyyy-MM-dd")
            + "\n\n"
            + "\n".join(text_lines)
            + f"\n\nTổng tiền nhập: {self._fmt_money(total_money)}",
        )

        # TODO (DB thật):
        # - tạo PhiếuNhập (ImportTicket)
        # - insert chi tiết phiếu nhập
        # - update tồn kho SUPPLIES (SuppliesAmount += qty)

    def _on_reset_clicked(self):
        self.import_date.setDate(QDate.currentDate())
        for r in range(self.table.rowCount()):
            qty_edit: QLineEdit = self.table.cellWidget(r, 4)
            if qty_edit:
                qty_edit.setText("0")
        self._update_selected_count()

    # ---------------- Mock ----------------
    def _mock_supplies(self) -> list[SupplyRow]:
        return [
            SupplyRow("Dầu nhớt", 120000, 30),
            SupplyRow("Lọc gió", 80000, 18),
            SupplyRow("Bugi", 90000, 40),
            SupplyRow("Má phanh", 350000, 12),
        ]

    # ---------------- Money helpers ----------------
    def _fmt_money(self, v: int) -> str:
        return f"{v:,}"

    def _parse_money(self, s: str) -> int:
        try:
            return int((s or "0").replace(",", "").strip())
        except ValueError:
            return 0
