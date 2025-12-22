# src/presentation/views/pages/phieu_sua_chua_page.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QDateEdit,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
import logging

from utils.style import STYLE
from services.repair_service import RepairService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SupplyItem:
    name: str
    price: int


@dataclass(frozen=True)
class WageItem:
    name: str
    value: int


class PhieuSuaChuaPage(QWidget):
    """BM2: Phiếu sửa chữa (UI-only)."""

    PAGE_ID = "phieu_sua_chua"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = RepairService()
        self._supplies = []
        self._wages = []

        self._setup_ui()
        self._apply_style()
        self._load_supplies_and_wages()
        self._recalc_total()

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

        title = QLabel("PHIẾU SỬA CHỮA (BM2)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Nhập thông tin phiếu và chi tiết vật tư/phụ tùng, tiền công.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setObjectName("pageSubtitle")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        # --- Top form (2 cột) ---
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        # Cột trái: thông tin phiếu
        group_info = QGroupBox("Thông tin phiếu")
        grid_info = QGridLayout(group_info)
        grid_info.setHorizontalSpacing(12)
        grid_info.setVerticalSpacing(10)

        self.license_plate = QLineEdit()
        self.license_plate.setPlaceholderText("Biển số xe * (VD: 51F-123.45)")
        self.license_plate.textChanged.connect(self._uppercase_plate)

        self.repair_date = QDateEdit()
        self.repair_date.setCalendarPopup(True)
        self.repair_date.setDate(QDate.currentDate())

        self.note = QLineEdit()
        self.note.setPlaceholderText("Ghi chú (tuỳ chọn)")

        grid_info.addWidget(QLabel("Biển số xe *"), 0, 0)
        grid_info.addWidget(self.license_plate, 0, 1)
        grid_info.addWidget(QLabel("Ngày sửa chữa *"), 1, 0)
        grid_info.addWidget(self.repair_date, 1, 1)
        grid_info.addWidget(QLabel("Ghi chú"), 2, 0)
        grid_info.addWidget(self.note, 2, 1)

        # Cột phải: tổng tiền
        group_total = QGroupBox("Tổng tiền")
        grid_total = QGridLayout(group_total)
        grid_total.setHorizontalSpacing(12)
        grid_total.setVerticalSpacing(10)

        self.lbl_total = QLabel("0")
        self.lbl_total.setObjectName("moneyBig")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        grid_total.addWidget(QLabel("Tổng cộng:"), 0, 0)
        grid_total.addWidget(self.lbl_total, 0, 1)

        hint = QLabel("Thành tiền từng dòng = (Số lượng × Đơn giá) + Tiền công")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #6b7280;")
        grid_total.addWidget(hint, 1, 0, 1, 2)

        top_row.addWidget(group_info, 3)
        top_row.addWidget(group_total, 2)

        container_layout.addLayout(top_row)

        # --- Table details ---
        group_details = QGroupBox("Chi tiết sửa chữa")
        details_layout = QVBoxLayout(group_details)
        details_layout.setSpacing(10)

        self.table = QTableWidget(0, 7, self)
        self.table.setHorizontalHeaderLabels(
            ["Nội dung", "Vật tư/Phụ tùng", "Số lượng", "Đơn giá", "Tiền công", "Thành tiền", ""]
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        details_layout.addWidget(self.table)

        # Buttons row for details
        detail_btns = QHBoxLayout()
        detail_btns.addStretch(1)

        self.btn_add_row = QPushButton("Thêm dòng")
        self.btn_remove_row = QPushButton("Xóa dòng")
        self.btn_add_row.clicked.connect(self._add_row)
        self.btn_remove_row.clicked.connect(self._remove_selected_row)

        detail_btns.addWidget(self.btn_add_row)
        detail_btns.addWidget(self.btn_remove_row)
        details_layout.addLayout(detail_btns)

        container_layout.addWidget(group_details)

        # --- Bottom actions ---
        actions = QHBoxLayout()
        actions.addStretch(1)

        self.btn_save = QPushButton("Lưu phiếu")
        self.btn_reset = QPushButton("Làm mới")
        self.btn_print = QPushButton("In phiếu")

        self.btn_save.setObjectName("btnSave")
        self.btn_reset.setObjectName("btnReset")
        self.btn_print.setObjectName("btnPrint")

        self.btn_save.clicked.connect(self._on_save_clicked)
        self.btn_reset.clicked.connect(self._on_reset_clicked)
        self.btn_print.clicked.connect(self._on_print_clicked)

        actions.addWidget(self.btn_save)
        actions.addWidget(self.btn_reset)
        actions.addWidget(self.btn_print)

        container_layout.addLayout(actions)

        root.addWidget(container)
        root.addStretch(1)

        # Add first empty row
        self._add_row()

    def _apply_style(self):
        # Local QSS so it won't look washed out under global stylesheet
        self.setStyleSheet(STYLE)
    # ---------------- Table row helpers ----------------
    def _add_row(self):
        r = self.table.rowCount()
        self.table.insertRow(r)

        # 0: Content (QLineEdit)
        content = QLineEdit()
        content.setPlaceholderText("VD: Thay dầu, thay lọc gió...")
        content.textChanged.connect(lambda _=None, row=r: self._recalc_row(row))
        self.table.setCellWidget(r, 0, content)

        # 1: Supplies combobox
        cb_supply = QComboBox()
        cb_supply.addItem("-- Chọn vật tư --")
        for s in self._supplies:
            cb_supply.addItem(s.name)
        cb_supply.currentIndexChanged.connect(lambda _=None, row=r: self._recalc_row(row))
        self.table.setCellWidget(r, 1, cb_supply)

        # 2: Quantity
        qty = QLineEdit("1")
        qty.setValidator(QIntValidator(0, 999999, self))
        qty.textChanged.connect(lambda _=None, row=r: self._recalc_row(row))
        self.table.setCellWidget(r, 2, qty)

        # 3: Unit price (read-only text)
        price_item = QTableWidgetItem("0")
        price_item.setFlags(price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(r, 3, price_item)

        # 4: Wage combobox
        cb_wage = QComboBox()
        cb_wage.addItem("-- Chọn tiền công --")
        for w in self._wages:
            cb_wage.addItem(w.name)
        cb_wage.currentIndexChanged.connect(lambda _=None, row=r: self._recalc_row(row))
        self.table.setCellWidget(r, 4, cb_wage)

        # 5: Line total (read-only)
        total_item = QTableWidgetItem("0")
        total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(r, 5, total_item)

        # 6: remove button per row
        btn_del = QPushButton("Xóa")
        btn_del.setStyleSheet("background:#ef4444;")
        btn_del.clicked.connect(lambda _=None, row=r: self._remove_row(row))
        self.table.setCellWidget(r, 6, btn_del)

        # Recalc new row
        self._recalc_row(r)

    def _remove_row(self, row: int):
        if row < 0 or row >= self.table.rowCount():
            return
        self.table.removeRow(row)
        self._rebind_row_callbacks()
        self._recalc_total()

    def _remove_selected_row(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Xóa dòng", "Vui lòng chọn 1 dòng để xóa.")
            return
        self._remove_row(row)

    def _rebind_row_callbacks(self):
        # After removing rows, lambdas created with row index become stale.
        # Rebind all signals using current row indices.
        for r in range(self.table.rowCount()):
            content: QLineEdit = self.table.cellWidget(r, 0)
            cb_supply: QComboBox = self.table.cellWidget(r, 1)
            qty: QLineEdit = self.table.cellWidget(r, 2)
            cb_wage: QComboBox = self.table.cellWidget(r, 4)
            btn_del: QPushButton = self.table.cellWidget(r, 6)

            # Disconnect safely (Qt doesn't give easy safe disconnect; try/except)
            for w in (content, cb_supply, qty, cb_wage):
                try:
                    w.blockSignals(True)
                    w.blockSignals(False)
                except Exception:
                    pass

            # Reconnect with correct r
            content.textChanged.connect(lambda _=None, row=r: self._recalc_row(row))
            cb_supply.currentIndexChanged.connect(lambda _=None, row=r: self._recalc_row(row))
            qty.textChanged.connect(lambda _=None, row=r: self._recalc_row(row))
            cb_wage.currentIndexChanged.connect(lambda _=None, row=r: self._recalc_row(row))

            btn_del.clicked.disconnect()
            btn_del.clicked.connect(lambda _=None, row=r: self._remove_row(row))

    # ---------------- Calculation ----------------
    def _recalc_row(self, row: int):
        if row < 0 or row >= self.table.rowCount():
            return

        cb_supply: QComboBox = self.table.cellWidget(row, 1)
        qty_edit: QLineEdit = self.table.cellWidget(row, 2)
        cb_wage: QComboBox = self.table.cellWidget(row, 4)

        qty = int(qty_edit.text() or "0")

        # Supply price
        supply_price = 0
        if cb_supply.currentIndex() > 0:
            name = cb_supply.currentText()
            supply_price = self._find_supply_price(name)

        # Wage value
        wage_value = 0
        if cb_wage.currentIndex() > 0:
            wage_name = cb_wage.currentText()
            wage_value = self._find_wage_value(wage_name)

        line_total = qty * supply_price + wage_value

        # Update table items
        self.table.item(row, 3).setText(self._fmt_money(supply_price))
        self.table.item(row, 5).setText(self._fmt_money(line_total))

        self._recalc_total()

    def _recalc_total(self):
        total = 0
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 5)
            if not item:
                continue
            total += self._parse_money(item.text())
        self.lbl_total.setText(self._fmt_money(total))

    # ---------------- Data Loading ----------------
    def _load_supplies_and_wages(self):
        """Load danh sách vật tư và tiền công từ database."""
        try:
            # Load supplies
            db_supplies = self.service.get_all_supplies()
            self._supplies = [
                SupplyItem(s['SuppliesName'], int(s['SuppliesPrice']))
                for s in db_supplies
            ]
            
            # Load wages
            db_wages = self.service.get_all_wages()
            self._wages = [
                WageItem(w['WageName'], int(w['WageValue']))
                for w in db_wages
            ]
            
            logger.info(f"Loaded {len(self._supplies)} supplies and {len(self._wages)} wages")
            
            # Refresh comboboxes in all existing rows
            for r in range(self.table.rowCount()):
                self._refresh_row_combos(r)
                
        except Exception as e:
            logger.error(f"Failed to load supplies and wages: {e}")
            QMessageBox.warning(
                self,
                "Cảnh báo",
                "Không thể tải danh sách vật tư và tiền công từ database.\n"
                "Vui lòng kiểm tra kết nối database."
            )
    
    def _refresh_row_combos(self, row: int):
        """Refresh combobox items in a specific row."""
        if row < 0 or row >= self.table.rowCount():
            return
        
        # Refresh supplies combobox
        cb_supply: QComboBox = self.table.cellWidget(row, 1)
        if cb_supply:
            current_text = cb_supply.currentText()
            cb_supply.clear()
            cb_supply.addItem("-- Chọn vật tư --")
            for s in self._supplies:
                cb_supply.addItem(s.name)
            # Restore selection if it still exists
            idx = cb_supply.findText(current_text)
            if idx >= 0:
                cb_supply.setCurrentIndex(idx)
        
        # Refresh wages combobox
        cb_wage: QComboBox = self.table.cellWidget(row, 4)
        if cb_wage:
            current_text = cb_wage.currentText()
            cb_wage.clear()
            cb_wage.addItem("-- Chọn tiền công --")
            for w in self._wages:
                cb_wage.addItem(w.name)
            # Restore selection if it still exists
            idx = cb_wage.findText(current_text)
            if idx >= 0:
                cb_wage.setCurrentIndex(idx)

    # ---------------- Actions ----------------
    def _uppercase_plate(self):
        txt = self.license_plate.text()
        upper = txt.upper()
        if txt != upper:
            pos = self.license_plate.cursorPosition()
            self.license_plate.blockSignals(True)
            self.license_plate.setText(upper)
            self.license_plate.setCursorPosition(pos)
            self.license_plate.blockSignals(False)

    def get_form_data(self) -> dict:
        details = []
        for r in range(self.table.rowCount()):
            content: QLineEdit = self.table.cellWidget(r, 0)
            cb_supply: QComboBox = self.table.cellWidget(r, 1)
            qty_edit: QLineEdit = self.table.cellWidget(r, 2)
            cb_wage: QComboBox = self.table.cellWidget(r, 4)

            details.append({
                "content": content.text().strip(),
                "supply": cb_supply.currentText(),
                "qty": int(qty_edit.text() or "0"),
                "unit_price": self._parse_money(self.table.item(r, 3).text()),
                "wage": cb_wage.currentText(),
                "line_total": self._parse_money(self.table.item(r, 5).text()),
            })

        return {
            "license_plate": self.license_plate.text().strip(),
            "repair_date": self.repair_date.date().toString("yyyy-MM-dd"),
            "note": self.note.text().strip(),
            "total": self._parse_money(self.lbl_total.text()),
            "details": details,
        }

    def _on_save_clicked(self):
        """Xử lý khi người dùng nhấn nút Lưu phiếu."""
        data = self.get_form_data()

        # Validate dữ liệu đầu vào
        missing = []
        if not data["license_plate"]:
            missing.append("Biển số xe")
        if self.table.rowCount() == 0:
            missing.append("Ít nhất 1 dòng chi tiết")

        if missing:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập:\n- " + "\n- ".join(missing))
            return
        
        # Validate chi tiết sửa chữa
        for idx, detail in enumerate(data['details'], 1):
            if not detail['content']:
                QMessageBox.warning(self, "Thiếu thông tin", f"Vui lòng nhập nội dung cho dòng {idx}")
                return
            if detail['supply'] == "-- Chọn vật tư --":
                QMessageBox.warning(self, "Thiếu thông tin", f"Vui lòng chọn vật tư cho dòng {idx}")
                return
            if detail['qty'] <= 0:
                QMessageBox.warning(self, "Thông tin không hợp lệ", f"Số lượng phải > 0 cho dòng {idx}")
                return
        
        try:
            # 1. Tìm phiếu tiếp nhận xe theo biển số
            reception = self.service.get_latest_reception_by_license_plate(data['license_plate'])
            
            if not reception:
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    f"Không tìm thấy phiếu tiếp nhận cho xe {data['license_plate']}.\n"
                    "Vui lòng tiếp nhận xe trước khi tạo phiếu sửa chữa."
                )
                return
            
            # 2. Kiểm tra tồn kho vật tư
            for detail in data['details']:
                check = self.service.check_supply_inventory(
                    detail['supply'],
                    detail['qty']
                )
                if not check['available']:
                    QMessageBox.warning(
                        self,
                        "Không đủ tồn kho",
                        check['message']
                    )
                    return
            
            # 3. Chuẩn bị dữ liệu chi tiết
            repair_details = []
            for detail in data['details']:
                repair_details.append({
                    'content': detail['content'],
                    'supply_name': detail['supply'],
                    'supply_amount': detail['qty'],
                    'wage_name': detail['wage'] if detail['wage'] != "-- Chọn tiền công --" else None
                })
            
            # 4. Tạo phiếu sửa chữa
            result = self.service.create_repair_ticket(
                reception_id=reception['ReceptionId'],
                repair_date=data['repair_date'],
                repair_money=data['total'],
                details=repair_details
            )
            
            if result['success']:
                # Hiển thị thông báo thành công
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Thành công")
                msg.setText(result['message'])
                msg.setInformativeText(
                    f"Mã phiếu sửa chữa: {result['repair_id']}\n"
                    f"Biển số xe: {data['license_plate']}\n"
                    f"Chủ xe: {reception['OwnerName']}\n"
                    f"Ngày sửa: {data['repair_date']}\n"
                    f"Tổng tiền: {self._fmt_money(data['total'])}\n"
                    f"Số dòng chi tiết: {len(data['details'])}"
                )
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                
                # Lưu repair_id để có thể in phiếu
                self.last_repair_id = result['repair_id']
                
                # Reset form sau khi lưu thành công
                self._on_reset_clicked()
            else:
                # Hiển thị lỗi
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    f"Không thể tạo phiếu sửa chữa:\n{result['message']}"
                )
        except Exception as e:
            logger.error(f"Error saving repair ticket: {e}")
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Đã xảy ra lỗi khi lưu dữ liệu:\n{str(e)}"
            )

    def _on_reset_clicked(self):
        """Reset tất cả các trường nhập liệu về trạng thái ban đầu."""
        self.license_plate.clear()
        self.note.clear()
        self.repair_date.setDate(QDate.currentDate())

        self.table.setRowCount(0)
        self._add_row()
        self._recalc_total()
        self.last_repair_id = None

    def _on_print_clicked(self):
        # MVP: preview dialog (làm sau). Hiện tại show thông tin ngắn.
        data = self.get_form_data()
        QMessageBox.information(
            self,
            "In phiếu (demo)",
            f"Phiếu sửa chữa\nBiển số: {data['license_plate']}\nNgày: {data['repair_date']}\nTổng: {self._fmt_money(data['total'])}"
        )

    # ---------------- Mock data ----------------
    def _mock_supplies(self) -> list[SupplyItem]:
        return [
            SupplyItem("Dầu nhớt", 120000),
            SupplyItem("Lọc gió", 80000),
            SupplyItem("Bugi", 90000),
            SupplyItem("Má phanh", 350000),
        ]

    def _mock_wages(self) -> list[WageItem]:
        return [
            WageItem("Thay dầu", 50000),
            WageItem("Vệ sinh lọc gió", 30000),
            WageItem("Thay bugi", 60000),
            WageItem("Kiểm tra tổng quát", 100000),
        ]

    def _find_supply_price(self, name: str) -> int:
        for s in self._supplies:
            if s.name == name:
                return s.price
        return 0

    def _find_wage_value(self, name: str) -> int:
        for w in self._wages:
            if w.name == name:
                return w.value
        return 0

    # ---------------- Money helpers ----------------
    def _fmt_money(self, v: int) -> str:
        # format 1200000 -> 1,200,000
        return f"{v:,}"

    def _parse_money(self, s: str) -> int:
        try:
            return int((s or "0").replace(",", "").strip())
        except ValueError:
            return 0
