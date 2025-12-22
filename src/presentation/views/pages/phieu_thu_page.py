# src/presentation/views/pages/phieu_thu_page.py

from __future__ import annotations

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
)
import logging

from utils.style import STYLE
from services.receipt_service import ReceiptService

logger = logging.getLogger(__name__)


class PhieuThuPage(QWidget):
    """BM4: Phiếu thu tiền (UI-only, mock)."""

    PAGE_ID = "phieu_thu"

    def __init__(self, parent=None):
        super().__init__(parent)
        # Nếu bạn apply STYLE toàn app rồi thì có thể bỏ dòng này
        self.setStyleSheet(STYLE)
        
        self.service = ReceiptService()
        self.current_reception_id = None  # Lưu ReceptionId hiện tại để tạo phiếu thu

        self._setup_ui()
        self._apply_view_state(empty=True)

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

        title = QLabel("PHIẾU THU TIỀN (BM4)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Nhập biển số để lấy tiền nợ, sau đó lập phiếu thu. (Tiền thu không vượt quá tiền nợ)")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setObjectName("pageSubtitle")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        # ---- Group: Tra cứu xe ----
        group_lookup = QGroupBox("Tra cứu xe")
        grid_lookup = QGridLayout(group_lookup)
        grid_lookup.setHorizontalSpacing(12)
        grid_lookup.setVerticalSpacing(10)

        self.inp_plate = QLineEdit()
        self.inp_plate.setPlaceholderText("Biển số xe * (vd: 51F-123.45)")
        self.inp_plate.textChanged.connect(self._uppercase_plate)

        self.btn_load = QPushButton("Tải thông tin")
        self.btn_load.setObjectName("btnPrimary")
        self.btn_load.clicked.connect(self._on_load_clicked)

        grid_lookup.addWidget(QLabel("Biển số *"), 0, 0)
        grid_lookup.addWidget(self.inp_plate, 0, 1)
        grid_lookup.addWidget(self.btn_load, 0, 2)

        container_layout.addWidget(group_lookup)

        # ---- Group: Thông tin xe + công nợ ----
        group_info = QGroupBox("Thông tin xe & công nợ")
        grid_info = QGridLayout(group_info)
        grid_info.setHorizontalSpacing(12)
        grid_info.setVerticalSpacing(10)

        self.out_owner = QLineEdit()
        self.out_owner.setReadOnly(True)
        self.out_owner.setObjectName("readOnlyField")

        self.out_phone = QLineEdit()
        self.out_phone.setReadOnly(True)
        self.out_phone.setObjectName("readOnlyField")

        self.out_address = QLineEdit()
        self.out_address.setReadOnly(True)
        self.out_address.setObjectName("readOnlyField")

        self.out_debt = QLineEdit()
        self.out_debt.setReadOnly(True)
        self.out_debt.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.out_debt.setObjectName("readOnlyMoney")

        grid_info.addWidget(QLabel("Chủ xe"), 0, 0)
        grid_info.addWidget(self.out_owner, 0, 1)
        grid_info.addWidget(QLabel("Điện thoại"), 0, 2)
        grid_info.addWidget(self.out_phone, 0, 3)

        grid_info.addWidget(QLabel("Địa chỉ"), 1, 0)
        grid_info.addWidget(self.out_address, 1, 1, 1, 3)

        grid_info.addWidget(QLabel("Tiền nợ hiện tại"), 2, 0)
        grid_info.addWidget(self.out_debt, 2, 1)

        self.lbl_debt_hint = QLabel("")
        self.lbl_debt_hint.setObjectName("hintText")
        grid_info.addWidget(self.lbl_debt_hint, 2, 2, 1, 2)

        container_layout.addWidget(group_info)

        # ---- Group: Lập phiếu thu ----
        group_receipt = QGroupBox("Lập phiếu thu")
        grid_r = QGridLayout(group_receipt)
        grid_r.setHorizontalSpacing(12)
        grid_r.setVerticalSpacing(10)

        self.receipt_date = QDateEdit()
        self.receipt_date.setCalendarPopup(True)
        self.receipt_date.setDate(QDate.currentDate())

        self.inp_amount = QLineEdit()
        self.inp_amount.setPlaceholderText("Số tiền thu *")
        self.inp_amount.setValidator(QIntValidator(0, 2_000_000_000, self))
        self.inp_amount.textChanged.connect(self._on_amount_changed)

        self.lbl_after = QLabel("Còn nợ sau thu: 0")
        self.lbl_after.setObjectName("moneyHint")
        self.lbl_after.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        grid_r.addWidget(QLabel("Ngày thu *"), 0, 0)
        grid_r.addWidget(self.receipt_date, 0, 1)
        grid_r.addWidget(QLabel("Số tiền thu *"), 1, 0)
        grid_r.addWidget(self.inp_amount, 1, 1)
        grid_r.addWidget(self.lbl_after, 1, 2, 1, 2)

        container_layout.addWidget(group_receipt)

        # ---- Actions ----
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

    # ---------------- Logic ----------------
    def _on_load_clicked(self):
        """Tải thông tin xe và nợ từ database."""
        plate = self.inp_plate.text().strip().upper()
        if not plate:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập biển số.")
            return
        
        try:
            # Lấy thông tin xe và tổng nợ
            info = self.service.get_vehicle_debt_info(plate)
            if not info:
                self._apply_view_state(empty=True)
                self.current_reception_id = None
                QMessageBox.information(
                    self,
                    "Không tìm thấy",
                    f"Không tìm thấy xe có biển số {plate} trong hệ thống."
                )
                return
            
            total_debt = float(info['TotalDebt']) if info['TotalDebt'] else 0
            
            if total_debt <= 0:
                self._apply_view_state(empty=False)
                self.out_owner.setText(info['OwnerName'])
                self.out_phone.setText(info['PhoneNumber'] or '')
                self.out_address.setText(info['Address'] or '')
                self._set_debt(0)
                self.lbl_debt_hint.setText("Xe này không có nợ.")
                self.current_reception_id = None
                QMessageBox.information(
                    self,
                    "Không có nợ",
                    f"Xe {plate} không có công nợ."
                )
                return
            
            # Lấy phiếu tiếp nhận mới nhất có nợ
            reception = self.service.get_latest_reception_with_debt(plate)
            if not reception:
                self._apply_view_state(empty=True)
                self.current_reception_id = None
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Không tìm thấy phiếu tiếp nhận có nợ cho xe này."
                )
                return
            
            # Hiển thị thông tin
            self._apply_view_state(empty=False)
            self.out_owner.setText(info['OwnerName'])
            self.out_phone.setText(info['PhoneNumber'] or '')
            self.out_address.setText(info['Address'] or '')
            self._set_debt(int(total_debt))
            self.current_reception_id = reception['ReceptionId']
            
            self.lbl_debt_hint.setText("Quy định: Tiền thu không vượt quá tiền nợ.")
            self._on_amount_changed()
            
            logger.info(f"Loaded debt info for {plate}: {total_debt}")
            
        except Exception as e:
            logger.error(f"Error loading vehicle debt info: {e}")
            self._apply_view_state(empty=True)
            self.current_reception_id = None
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Đã xảy ra lỗi khi tải thông tin:\n{str(e)}"
            )

    def _on_amount_changed(self):
        debt = self._get_debt()
        amount = int(self.inp_amount.text() or "0")
        after = max(0, debt - amount)
        self.lbl_after.setText(f"Còn nợ sau thu: {self._fmt_money(after)}")

    def _on_save_clicked(self):
        """Lưu phiếu thu vào database."""
        plate = self.inp_plate.text().strip().upper()
        if not plate:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập biển số và tải thông tin.")
            return
        
        if not self.current_reception_id:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng bấm 'Tải thông tin' trước.")
            return

        debt = self._get_debt()
        amount = int(self.inp_amount.text() or "0")
        if amount <= 0:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập số tiền thu > 0.")
            return

        # QĐ4: Tiền thu <= tiền nợ (kiểm tra trước)
        if amount > debt:
            QMessageBox.warning(
                self,
                "Sai quy định",
                f"Số tiền thu không được vượt quá tiền nợ.\n"
                f"Tiền nợ: {self._fmt_money(debt)}\n"
                f"Tiền thu: {self._fmt_money(amount)}"
            )
            return
        
        try:
            # Tạo phiếu thu
            result = self.service.create_receipt(
                reception_id=self.current_reception_id,
                receipt_date=self.receipt_date.date().toString('yyyy-MM-dd'),
                money_amount=amount
            )
            
            if result['success']:
                remaining_debt = result.get('remaining_debt', 0)
                
                # Hiển thị thông báo thành công
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Thành công")
                msg.setText(result['message'])
                msg.setInformativeText(
                    f"Mã phiếu thu: {result['receipt_id']}\n"
                    f"Biển số: {plate}\n"
                    f"Ngày thu: {self.receipt_date.date().toString('yyyy-MM-dd')}\n"
                    f"Tiền thu: {self._fmt_money(amount)}\n"
                    f"Còn nợ: {self._fmt_money(int(remaining_debt))}"
                )
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                
                # Lưu receipt_id để có thể in phiếu
                self.last_receipt_id = result['receipt_id']
                
                # Cập nhật hiển thị nợ mới
                self._set_debt(int(remaining_debt))
                self.inp_amount.clear()
                self._on_amount_changed()
                
                # Nếu hết nợ, reset form
                if remaining_debt <= 0:
                    QMessageBox.information(
                        self,
                        "Thông báo",
                        "Xe đã thanh toán hết nợ!"
                    )
                    self._on_reset_clicked()
            else:
                # Hiển thị lỗi
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    f"Không thể tạo phiếu thu:\n{result['message']}"
                )
        except Exception as e:
            logger.error(f"Error saving receipt: {e}")
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Đã xảy ra lỗi khi lưu phiếu thu:\n{str(e)}"
            )

    def _on_print_clicked(self):
        """In phiếu thu (demo)."""
        plate = self.inp_plate.text().strip().upper()
        if not plate or not self.current_reception_id:
            QMessageBox.information(self, "In phiếu", "Vui lòng tải thông tin xe trước.")
            return
        
        amount = self.inp_amount.text().strip()
        if not amount or int(amount or "0") <= 0:
            QMessageBox.information(self, "In phiếu", "Vui lòng nhập số tiền thu trước khi in.")
            return
        
        QMessageBox.information(
            self,
            "In phiếu (demo)",
            f"Sẽ in phiếu thu cho xe: {plate}\n"
            f"Số tiền: {self._fmt_money(int(amount))}"
        )

    def _on_reset_clicked(self):
        """Reset form về trạng thái ban đầu."""
        self.inp_plate.clear()
        self.inp_amount.clear()
        self.receipt_date.setDate(QDate.currentDate())
        self.current_reception_id = None
        self.last_receipt_id = None
        self._apply_view_state(empty=True)

    def _apply_view_state(self, *, empty: bool):
        if empty:
            self.out_owner.clear()
            self.out_phone.clear()
            self.out_address.clear()
            self._set_debt(0)
            self.lbl_debt_hint.setText("")
            self.lbl_after.setText("Còn nợ sau thu: 0")

    def _uppercase_plate(self):
        txt = self.inp_plate.text()
        upper = txt.upper()
        if txt != upper:
            pos = self.inp_plate.cursorPosition()
            self.inp_plate.blockSignals(True)
            self.inp_plate.setText(upper)
            self.inp_plate.setCursorPosition(pos)
            self.inp_plate.blockSignals(False)

    # ---------------- Helpers ----------------
    def _set_debt(self, v: int):
        self.out_debt.setText(self._fmt_money(v))

    def _get_debt(self) -> int:
        try:
            return int((self.out_debt.text() or "0").replace(",", "").strip())
        except ValueError:
            return 0

    def _fmt_money(self, v: int) -> str:
        return f"{v:,}"
