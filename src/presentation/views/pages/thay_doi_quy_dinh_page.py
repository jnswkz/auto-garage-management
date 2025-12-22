# src/presentation/views/pages/thay_doi_quy_dinh_page.py

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout,
    QGroupBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QSpinBox
)

from utils.style import STYLE


class ThayDoiQuyDinhPage(QWidget):
    """
    QĐ6 - Thay đổi quy định hệ thống:
      - QĐ6.1: số xe sửa chữa tối đa/ngày + danh sách hiệu xe
      - QĐ6.2: danh mục vật tư (tên + đơn giá) + danh mục tiền công (tên + giá)
    """

    PAGE_ID = "thay_doi_quy_dinh"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE)

        # UI-only mock data (sau này load từ DB PARAMETER, CAR_BRAND, SUPPLIES, WAGE)
        self._brands = ["Toyota", "Honda", "Suzuki", "Ford", "Kia", "Hyundai"]
        self._max_cars_per_day = 30
        self._supplies = [
            ("Dầu nhớt", 120000),
            ("Lọc gió", 80000),
            ("Bugi", 90000),
        ]
        self._wages = [
            ("Thay dầu", 50000),
            ("Vệ sinh lọc gió", 30000),
            ("Kiểm tra tổng quát", 100000),
        ]

        self._setup_ui()
        self._render_all()

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

        title = QLabel("THAY ĐỔI QUY ĐỊNH")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Điều chỉnh quy định hệ thống: hiệu xe, số xe tối đa/ngày, vật tư và tiền công.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setObjectName("pageSubtitle")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("ruleTabs")

        self.tabs.addTab(self._build_tab_qd61(), "Hiệu xe & giới hạn")
        self.tabs.addTab(self._build_tab_supplies(), "Vật tư/Phụ tùng")
        self.tabs.addTab(self._build_tab_wages(), "Tiền công")

        container_layout.addWidget(self.tabs)

        # Bottom actions
        actions = QHBoxLayout()
        actions.addStretch(1)

        self.btn_apply = QPushButton("Áp dụng thay đổi")
        self.btn_apply.setObjectName("btnPrimary")
        self.btn_apply.clicked.connect(self._on_apply_clicked)

        self.btn_reset = QPushButton("Hoàn tác (UI)")
        self.btn_reset.setObjectName("btnReset")
        self.btn_reset.clicked.connect(self._on_reset_clicked)

        actions.addWidget(self.btn_apply)
        actions.addWidget(self.btn_reset)

        container_layout.addLayout(actions)

        root.addWidget(container)
        root.addStretch(1)

    # ---------------- Tabs ----------------
    def _build_tab_qd61(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setSpacing(12)

        group = QGroupBox("Thiết lập")
        grid = QGridLayout(group)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        self.spin_max_cars = QSpinBox()
        self.spin_max_cars.setRange(1, 9999)
        self.spin_max_cars.setValue(self._max_cars_per_day)

        grid.addWidget(QLabel("Số xe sửa chữa tối đa trong ngày *"), 0, 0)
        grid.addWidget(self.spin_max_cars, 0, 1)

        lay.addWidget(group)

        # Brands table
        group2 = QGroupBox("Danh sách hiệu xe")
        v = QVBoxLayout(group2)
        v.setSpacing(10)

        self.tbl_brands = QTableWidget(0, 2)
        self.tbl_brands.setObjectName("dataTable")
        self.tbl_brands.setHorizontalHeaderLabels(["STT", "Hiệu xe"])
        self.tbl_brands.verticalHeader().setVisible(False)
        self.tbl_brands.setAlternatingRowColors(True)

        h = self.tbl_brands.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        v.addWidget(self.tbl_brands)

        row = QHBoxLayout()
        row.addStretch(1)
        self.btn_add_brand = QPushButton("Thêm hiệu xe")
        self.btn_del_brand = QPushButton("Xóa hiệu xe")
        self.btn_del_brand.setObjectName("btnDanger")
        self.btn_add_brand.clicked.connect(self._add_brand)
        self.btn_del_brand.clicked.connect(self._delete_brand)
        row.addWidget(self.btn_add_brand)
        row.addWidget(self.btn_del_brand)
        v.addLayout(row)

        lay.addWidget(group2)
        lay.addStretch(1)
        return tab

    def _build_tab_supplies(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setSpacing(12)

        group = QGroupBox("Danh mục vật tư/phụ tùng (Tên + Đơn giá)")
        v = QVBoxLayout(group)
        v.setSpacing(10)

        self.tbl_supplies = QTableWidget(0, 3)
        self.tbl_supplies.setObjectName("dataTable")
        self.tbl_supplies.setHorizontalHeaderLabels(["Tên vật tư", "Đơn giá", ""])
        self.tbl_supplies.verticalHeader().setVisible(False)
        self.tbl_supplies.setAlternatingRowColors(True)

        h = self.tbl_supplies.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.tbl_supplies.setColumnWidth(2, 96)

        self.tbl_supplies.verticalHeader().setDefaultSectionSize(64)
        v.addWidget(self.tbl_supplies)

        row = QHBoxLayout()
        row.addStretch(1)
        self.btn_add_supply = QPushButton("Thêm vật tư")
        self.btn_add_supply.clicked.connect(self._add_supply_row)
        row.addWidget(self.btn_add_supply)
        v.addLayout(row)

        lay.addWidget(group)
        lay.addStretch(1)
        return tab

    def _build_tab_wages(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setSpacing(12)

        group = QGroupBox("Danh mục tiền công (Tên + Giá)")
        v = QVBoxLayout(group)
        v.setSpacing(10)

        self.tbl_wages = QTableWidget(0, 3)
        self.tbl_wages.setObjectName("dataTable")
        self.tbl_wages.setHorizontalHeaderLabels(["Tên tiền công", "Giá", ""])
        self.tbl_wages.verticalHeader().setVisible(False)
        self.tbl_wages.setAlternatingRowColors(True)

        h = self.tbl_wages.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.tbl_wages.setColumnWidth(2, 96)
        self.tbl_wages.verticalHeader().setDefaultSectionSize(64)
        v.addWidget(self.tbl_wages)

        row = QHBoxLayout()
        row.addStretch(1)
        self.btn_add_wage = QPushButton("Thêm tiền công")
        self.btn_add_wage.clicked.connect(self._add_wage_row)
        row.addWidget(self.btn_add_wage)
        v.addLayout(row)

        lay.addWidget(group)
        lay.addStretch(1)
        return tab

    # ---------------- Render ----------------
    def _render_all(self):
        self._render_brands()
        self._render_supplies()
        self._render_wages()

    def _render_brands(self):
        self.tbl_brands.setRowCount(0)
        for i, name in enumerate(self._brands, start=1):
            r = self.tbl_brands.rowCount()
            self.tbl_brands.insertRow(r)

            it0 = QTableWidgetItem(str(i))
            it0.setFlags(it0.flags() & ~Qt.ItemFlag.ItemIsEditable)
            it0.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            it1 = QTableWidgetItem(name)

            self.tbl_brands.setItem(r, 0, it0)
            self.tbl_brands.setItem(r, 1, it1)

    def _render_supplies(self):
        self.tbl_supplies.setRowCount(0)
        for name, price in self._supplies:
            self._append_supply_row(name, price)

    def _render_wages(self):
        self.tbl_wages.setRowCount(0)
        for name, value in self._wages:
            self._append_wage_row(name, value)

    # ---------------- Row add/remove helpers ----------------
    def _add_brand(self):
        name, ok = self._prompt_text("Thêm hiệu xe", "Nhập tên hiệu xe:")
        if not ok:
            return
        name = name.strip()
        if not name:
            QMessageBox.warning(self, "Lỗi", "Tên hiệu xe không được rỗng.")
            return
        if name in self._brands:
            QMessageBox.warning(self, "Lỗi", "Hiệu xe đã tồn tại.")
            return
        self._brands.append(name)
        self._render_brands()

    def _delete_brand(self):
        row = self.tbl_brands.currentRow()
        if row < 0:
            QMessageBox.information(self, "Xóa hiệu xe", "Vui lòng chọn 1 dòng để xóa.")
            return
        name = self.tbl_brands.item(row, 1).text()
        self._brands = [b for b in self._brands if b != name]
        self._render_brands()

    def _add_supply_row(self):
        self._append_supply_row("", 0)

    def _append_supply_row(self, name: str, price: int):
        r = self.tbl_supplies.rowCount()
        self.tbl_supplies.insertRow(r)

        name_item = QTableWidgetItem(name)
        price_item = QTableWidgetItem(str(price))
        price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.tbl_supplies.setItem(r, 0, name_item)
        self.tbl_supplies.setItem(r, 1, price_item)

        btn = QPushButton("Xóa")
        btn.setObjectName("btnDanger")
        btn.setFixedSize(64, 32)

        wrap = QWidget()
        wrap_lay = QHBoxLayout(wrap)
        wrap_lay.setContentsMargins(8, 8, 8, 8)
        wrap_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wrap_lay.addWidget(btn)

        self.tbl_supplies.setCellWidget(r, 2, wrap)
        self.tbl_supplies.setRowHeight(r, 64)

        btn.clicked.connect(lambda _=None, row=r: self._delete_supply_row(row))


    def _delete_supply_row(self, row: int):
        if row < 0 or row >= self.tbl_supplies.rowCount():
            return
        self.tbl_supplies.removeRow(row)
        self._rebind_supply_delete_buttons()

    def _rebind_supply_delete_buttons(self):
        for r in range(self.tbl_supplies.rowCount()):
            wrap = self.tbl_supplies.cellWidget(r, 2)
            btn = wrap.findChild(QPushButton)
            if btn:
                try:
                    btn.clicked.disconnect()
                except Exception:
                    pass
                btn.clicked.connect(lambda _=None, row=r: self._delete_supply_row(row))

    def _add_wage_row(self):
        self._append_wage_row("", 0)

    def _append_wage_row(self, name: str, value: int):
        r = self.tbl_wages.rowCount()
        self.tbl_wages.insertRow(r)

        name_item = QTableWidgetItem(name)
        value_item = QTableWidgetItem(str(value))
        value_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.tbl_wages.setItem(r, 0, name_item)
        self.tbl_wages.setItem(r, 1, value_item)

        btn = QPushButton("Xóa")
        btn.setObjectName("btnDanger")
        btn.setFixedSize(64, 32)
        
        btn.clicked.connect(lambda _=None, row=r: self._delete_wage_row(row))
        self.tbl_wages.setCellWidget(r, 2, self._wrap_btn(btn))

    def _delete_wage_row(self, row: int):
        if row < 0 or row >= self.tbl_wages.rowCount():
            return
        self.tbl_wages.removeRow(row)
        self._rebind_wage_delete_buttons()

    def _rebind_wage_delete_buttons(self):
        for r in range(self.tbl_wages.rowCount()):
            wrap = self.tbl_wages.cellWidget(r, 2)
            btn = wrap.findChild(QPushButton)
            if btn:
                try:
                    btn.clicked.disconnect()
                except Exception:
                    pass
                btn.clicked.connect(lambda _=None, row=r: self._delete_wage_row(row))

    def _wrap_btn(self, btn: QPushButton) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(8, 6, 8, 6)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(btn)
        return w

    # ---------------- Apply/Reset ----------------
    def _on_apply_clicked(self):
        # Validate QĐ6.1
        max_cars = int(self.spin_max_cars.value())
        if max_cars <= 0:
            QMessageBox.warning(self, "Lỗi", "Số xe tối đa/ngày phải > 0.")
            return

        # Validate brands unique & not empty
        brands = []
        for r in range(self.tbl_brands.rowCount()):
            name = self.tbl_brands.item(r, 1).text().strip()
            if not name:
                QMessageBox.warning(self, "Lỗi", f"Hiệu xe dòng {r+1} bị rỗng.")
                return
            if name in brands:
                QMessageBox.warning(self, "Lỗi", f"Hiệu xe '{name}' bị trùng.")
                return
            brands.append(name)

        # Validate supplies (name unique, price > 0)
        supplies = []
        for r in range(self.tbl_supplies.rowCount()):
            name = (self.tbl_supplies.item(r, 0).text() if self.tbl_supplies.item(r, 0) else "").strip()
            price_str = (self.tbl_supplies.item(r, 1).text() if self.tbl_supplies.item(r, 1) else "0").strip()
            if not name:
                QMessageBox.warning(self, "Lỗi", f"Vật tư dòng {r+1} bị rỗng.")
                return
            try:
                price = int(price_str.replace(",", ""))
            except ValueError:
                QMessageBox.warning(self, "Lỗi", f"Đơn giá vật tư dòng {r+1} không hợp lệ.")
                return
            if price <= 0:
                QMessageBox.warning(self, "Lỗi", f"Đơn giá vật tư dòng {r+1} phải > 0.")
                return
            if any(s[0] == name for s in supplies):
                QMessageBox.warning(self, "Lỗi", f"Vật tư '{name}' bị trùng.")
                return
            supplies.append((name, price))

        # Validate wages (name unique, value > 0)
        wages = []
        for r in range(self.tbl_wages.rowCount()):
            name = (self.tbl_wages.item(r, 0).text() if self.tbl_wages.item(r, 0) else "").strip()
            value_str = (self.tbl_wages.item(r, 1).text() if self.tbl_wages.item(r, 1) else "0").strip()
            if not name:
                QMessageBox.warning(self, "Lỗi", f"Tiền công dòng {r+1} bị rỗng.")
                return
            try:
                value = int(value_str.replace(",", ""))
            except ValueError:
                QMessageBox.warning(self, "Lỗi", f"Giá tiền công dòng {r+1} không hợp lệ.")
                return
            if value <= 0:
                QMessageBox.warning(self, "Lỗi", f"Giá tiền công dòng {r+1} phải > 0.")
                return
            if any(w[0] == name for w in wages):
                QMessageBox.warning(self, "Lỗi", f"Tiền công '{name}' bị trùng.")
                return
            wages.append((name, value))

        # UI-only: commit to in-memory
        self._max_cars_per_day = max_cars
        self._brands = brands
        self._supplies = supplies
        self._wages = wages

        QMessageBox.information(
            self,
            "OK",
            "Đã áp dụng thay đổi thành công."
        )

    def _on_reset_clicked(self):
        QMessageBox.information(self, "Hoàn tác (UI)", "UI demo: bạn có thể reload lại từ DB sau.")
        self._render_all()

    # ---------------- Helpers ----------------
    def _prompt_text(self, title: str, label: str):
        # simple input dialog without importing QInputDialog for minimal dependencies
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(label + "\n\n(Chức năng nhập nhanh demo: mở rộng sau)")
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.exec()
        return "", False
