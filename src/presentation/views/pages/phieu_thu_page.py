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

from utils.style import STYLE


class PhieuThuPage(QWidget):
    """BM4: Phiếu thu tiền (UI-only, mock)."""

    PAGE_ID = "phieu_thu"

    def __init__(self, parent=None):
        super().__init__(parent)
        # Nếu bạn apply STYLE toàn app rồi thì có thể bỏ dòng này
        self.setStyleSheet(STYLE)

        self._mock_db = self._mock_debts()
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

    # ---------------- Logic (UI-only) ----------------
    def _on_load_clicked(self):
        plate = self.inp_plate.text().strip().upper()
        if not plate:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập biển số.")
            return

        info = self._mock_db.get(plate)
        if not info:
            self._apply_view_state(empty=True)
            QMessageBox.information(self, "Không tìm thấy", "Không tìm thấy xe hoặc chưa có công nợ (demo).")
            return

        self._apply_view_state(empty=False)
        self.out_owner.setText(info["owner"])
        self.out_phone.setText(info["phone"])
        self.out_address.setText(info["address"])
        self._set_debt(info["debt"])

        self.lbl_debt_hint.setText("Quy định: Tiền thu không vượt quá tiền nợ.")
        self._on_amount_changed()

    def _on_amount_changed(self):
        debt = self._get_debt()
        amount = int(self.inp_amount.text() or "0")
        after = max(0, debt - amount)
        self.lbl_after.setText(f"Còn nợ sau thu: {self._fmt_money(after)}")

    def _on_save_clicked(self):
        plate = self.inp_plate.text().strip().upper()
        if not plate:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập biển số và tải thông tin.")
            return

        info = self._mock_db.get(plate)
        if not info:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng bấm 'Tải thông tin' và chọn xe hợp lệ.")
            return

        debt = self._get_debt()
        amount = int(self.inp_amount.text() or "0")
        if amount <= 0:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập số tiền thu > 0.")
            return

        # QĐ4: Tiền thu <= tiền nợ
        if amount > debt:
            QMessageBox.warning(
                self,
                "Sai quy định",
                f"Số tiền thu không được vượt quá tiền nợ.\n"
                f"Tiền nợ: {self._fmt_money(debt)}\n"
                f"Tiền thu: {self._fmt_money(amount)}"
            )
            return

        # UI-only: giả lập cập nhật công nợ
        new_debt = debt - amount
        self._mock_db[plate]["debt"] = new_debt
        self._set_debt(new_debt)
        self._on_amount_changed()

        QMessageBox.information(
            self,
            "OK",
            "Đã lập phiếu thu (demo, chưa lưu DB).\n\n"
            f"Biển số: {plate}\n"
            f"Ngày thu: {self.receipt_date.date().toString('yyyy-MM-dd')}\n"
            f"Tiền thu: {self._fmt_money(amount)}\n"
            f"Còn nợ: {self._fmt_money(new_debt)}"
        )

    def _on_print_clicked(self):
        # MVP: preview/in thật làm sau
        plate = self.inp_plate.text().strip().upper()
        if not plate or plate not in self._mock_db:
            QMessageBox.information(self, "In phiếu", "Vui lòng tải thông tin xe trước.")
            return
        QMessageBox.information(self, "In phiếu", f"Sẽ in phiếu thu cho xe: {plate}")

    def _on_reset_clicked(self):
        self.inp_plate.clear()
        self.inp_amount.clear()
        self.receipt_date.setDate(QDate.currentDate())
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

    def _mock_debts(self) -> dict:
        # TODO: thay bằng query DB: CAR + CAR_RECEPTION.Debt
        return {
            "51F-123.45": {"owner": "Nguyễn Văn A", "phone": "0912345678", "address": "Q1, TP.HCM", "debt": 1200000},
            "51G-456.78": {"owner": "Phạm Minh D", "phone": "0987654321", "address": "Thủ Đức, TP.HCM", "debt": 9800000},
            "59A-111.22": {"owner": "Lê Văn C", "phone": "0900111222", "address": "Q5, TP.HCM", "debt": 350000},
        }
