# src/presentation/views/pages/tiep_nhan_xe_page.py

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTextEdit,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QMessageBox,
)
from PyQt6.QtCore import QDate, Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QDialog, QFrame, QFormLayout
import logging

from services.car_reception_service import CarReceptionService

logger = logging.getLogger(__name__)
from utils.style import STYLE

class BienNhanTiepNhanDialog(QDialog):
    """Dialog preview 'Biên nhận tiếp nhận xe' theo BM1."""

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Biên nhận tiếp nhận xe (BM1)")
        self.setModal(True)
        self.resize(520, 420)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        title = QLabel("BIÊN NHẬN TIẾP NHẬN XE SỬA (BM1)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #111827;")
        root.addWidget(title)

        sub = QLabel("Vui lòng kiểm tra thông tin trước khi in.")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("color: #6b7280;")
        root.addWidget(sub)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #e5e7eb;")
        root.addWidget(line)

        # Form content
        form_wrap = QWidget(self)
        form = QFormLayout(form_wrap)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)

        def val(x: str) -> str:
            return (x or "").strip()

        # Các field theo BM1
        form.addRow("Tên chủ xe:", QLabel(val(data.get("owner_name"))))
        form.addRow("Biển số:", QLabel(val(data.get("license_plate"))))
        form.addRow("Hiệu xe:", QLabel(val(data.get("brand"))))
        form.addRow("Địa chỉ:", QLabel(val(data.get("owner_address"))))
        form.addRow("Điện thoại:", QLabel(val(data.get("owner_phone"))))
        form.addRow("Ngày tiếp nhận:", QLabel(val(data.get("reception_date"))))

        # style text value
        for i in range(form.rowCount()):
            w = form.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
            if isinstance(w, QLabel):
                w.setStyleSheet("color: #111827; font-weight: 600;")

        root.addWidget(form_wrap)

        # Footer buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        self.btn_close = QPushButton("Đóng")
        self.btn_close.clicked.connect(self.reject)

        self.btn_fake_print = QPushButton("In")
        self.btn_fake_print.setObjectName("btnDialogPrint")
        self.btn_fake_print.clicked.connect(self._on_print)

        btn_row.addWidget(self.btn_fake_print)
        btn_row.addWidget(self.btn_close)
        root.addLayout(btn_row)

        # dialog style (nhẹ)
        self.setStyleSheet("""
            QDialog { background: #ffffff; }
            QLabel { color: #374151; }
            QPushButton { border-radius: 6px; padding: 7px 14px; }
            QPushButton#btnDialogPrint { background: #059669; color: white; border: none; }
            QPushButton#btnDialogPrint:hover { opacity: 0.92; }
        """)

    def _on_print(self):
        # MVP: chỉ thông báo (sau này bạn thay bằng QPrinter)
        QMessageBox.information(self, "In", "Đã in.")
        self.accept()


class TiepNhanXePage(QWidget):
    """Page for receiving vehicles into the garage (BM1)."""

    PAGE_ID = "tiep_nhan_xe"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CarReceptionService()
        self._setup_ui()
        self._apply_style()
        self._load_brands()

    def _setup_ui(self):
        # Root layout for page (embedded in stacked widget)
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)
        root.setAlignment(Qt.AlignmentFlag.AlignTop)

        # A white container card to match your app look
        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(18, 18, 18, 18)
        container_layout.setSpacing(12)

        # ===== Header =====
        title = QLabel("TIẾP NHẬN XE SỬA")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")

        subtitle = QLabel("Nhập thông tin chủ xe và xe để tiếp nhận.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("pageSubtitle")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        # ===== Inputs =====
        # Chủ xe
        self.owner_name = QLineEdit()
        self.owner_name.setPlaceholderText("Ví dụ: Nguyễn Văn A")

        self.owner_phone = QLineEdit()
        self.owner_phone.setPlaceholderText("10 chữ số")
        self.owner_phone.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d{0,10}$")))

        self.owner_address = QTextEdit()
        self.owner_address.setPlaceholderText("Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành")
        self.owner_address.setFixedHeight(70)

        # Xe
        self.license_plate = QLineEdit()
        self.license_plate.setPlaceholderText("Ví dụ: 51F-123.45")
        self.license_plate.textChanged.connect(self._uppercase_plate)

        self.brand = QComboBox()
        self.brand.addItem("-- Chọn hiệu xe --")  # Placeholder, sẽ load từ DB

        self.reception_date = QDateEdit()
        self.reception_date.setCalendarPopup(True)
        self.reception_date.setDate(QDate.currentDate())

        # ===== Groupboxes =====
        group_owner = QGroupBox("Thông tin chủ xe")
        grid_owner = QGridLayout(group_owner)
        grid_owner.setHorizontalSpacing(12)
        grid_owner.setVerticalSpacing(10)
        grid_owner.addWidget(QLabel("Tên chủ xe *"), 0, 0)
        grid_owner.addWidget(self.owner_name, 0, 1)
        grid_owner.addWidget(QLabel("Điện thoại *"), 1, 0)
        grid_owner.addWidget(self.owner_phone, 1, 1)
        grid_owner.addWidget(QLabel("Địa chỉ *"), 2, 0, Qt.AlignmentFlag.AlignTop)
        grid_owner.addWidget(self.owner_address, 2, 1)

        group_car = QGroupBox("Thông tin xe & tiếp nhận")
        grid_car = QGridLayout(group_car)
        grid_car.setHorizontalSpacing(12)
        grid_car.setVerticalSpacing(10)
        grid_car.addWidget(QLabel("Biển số *"), 0, 0)
        grid_car.addWidget(self.license_plate, 0, 1)
        grid_car.addWidget(QLabel("Hiệu xe *"), 1, 0)
        grid_car.addWidget(self.brand, 1, 1)
        grid_car.addWidget(QLabel("Ngày tiếp nhận *"), 2, 0)
        grid_car.addWidget(self.reception_date, 2, 1)

        body = QHBoxLayout()
        body.setSpacing(12)
        body.addWidget(group_owner, 1)
        body.addWidget(group_car, 1)
        container_layout.addLayout(body)

        # ===== Buttons =====
        self.btn_save = QPushButton("Lưu tiếp nhận")
        self.btn_reset = QPushButton("Làm mới")
        self.btn_print = QPushButton("In biên nhận")

        self.btn_save.setObjectName("btnSave")
        self.btn_reset.setObjectName("btnReset")
        self.btn_print.setObjectName("btnPrint")

        self.btn_save.clicked.connect(self._on_save_clicked)
        self.btn_reset.clicked.connect(self._on_reset_clicked)
        self.btn_print.clicked.connect(self._on_print_clicked)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_reset)
        btn_row.addWidget(self.btn_print)
        container_layout.addLayout(btn_row)

        # Put container in root layout
        container.setObjectName("pageContainer")
        root.addWidget(container)
        root.addStretch(1)

    def _apply_style(self):
        # Local QSS so it won't look washed out under global stylesheet
        self.setStyleSheet(STYLE)

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
        return {
            "owner_name": self.owner_name.text().strip(),
            "owner_phone": self.owner_phone.text().strip(),
            "owner_address": self.owner_address.toPlainText().strip(),
            "license_plate": self.license_plate.text().strip(),
            "brand": self.brand.currentText(),
            "reception_date": self.reception_date.date().toString("yyyy-MM-dd"),
        }

    def _on_save_clicked(self):
        """Xử lý khi người dùng nhấn nút Lưu tiếp nhận."""
        data = self.get_form_data()
        
        # Validate dữ liệu đầu vào
        missing = []
        if not data["owner_name"]:
            missing.append("Tên chủ xe")
        if not data["owner_phone"] or len(data["owner_phone"]) != 10:
            missing.append("Điện thoại (10 chữ số)")
        if not data["owner_address"]:
            missing.append("Địa chỉ")
        if not data["license_plate"]:
            missing.append("Biển số")
        if data["brand"] == "-- Chọn hiệu xe --":
            missing.append("Hiệu xe")

        if missing:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập:\n- " + "\n- ".join(missing))
            return
        
        # Gọi service để lưu vào database
        try:
            result = self.service.receive_car(
                license_plate=data["license_plate"],
                brand_name=data["brand"],
                owner_name=data["owner_name"],
                phone_number=data["owner_phone"],
                address=data["owner_address"],
                reception_date=data["reception_date"],
                email=None
            )
            
            if result['success']:
                # Hiển thị thông báo thành công
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Thành công")
                msg.setText(result['message'])
                msg.setInformativeText(
                    f"Mã tiếp nhận: {result['reception_id']}\n"
                    f"Biển số: {data['license_plate']}\n"
                    f"Chủ xe: {data['owner_name']}\n"
                    f"Ngày tiếp nhận: {data['reception_date']}"
                )
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                
                # Lưu reception_id để có thể in biên nhận
                self.last_reception_id = result['reception_id']
                
                # Reset form sau khi lưu thành công
                self._on_reset_clicked()
            else:
                # Hiển thị lỗi
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    f"Không thể tiếp nhận xe:\n{result['message']}"
                )
        except Exception as e:
            logger.error(f"Error saving car reception: {e}")
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Đã xảy ra lỗi khi lưu dữ liệu:\n{str(e)}"
            )

    def _on_reset_clicked(self):
        """Reset tất cả các trường nhập liệu về trạng thái ban đầu."""
        self.owner_name.clear()
        self.owner_phone.clear()
        self.owner_address.clear()
        self.license_plate.clear()
        self.brand.setCurrentIndex(0)
        self.reception_date.setDate(QDate.currentDate())
        self.last_reception_id = None
    
    def _load_brands(self):
        """Load danh sách hiệu xe từ database."""
        try:
            brands = self.service.get_all_brands()
            # Clear existing items except placeholder
            self.brand.clear()
            self.brand.addItem("-- Chọn hiệu xe --")
            
            # Add brands from database
            for brand in brands:
                self.brand.addItem(brand['BrandName'])
            
            logger.info(f"Loaded {len(brands)} car brands")
        except Exception as e:
            logger.error(f"Failed to load car brands: {e}")
            QMessageBox.warning(
                self,
                "Cảnh báo",
                "Không thể tải danh sách hiệu xe từ database.\n"
                "Vui lòng kiểm tra kết nối database."
            )

    def _on_print_clicked(self):
        data = self.get_form_data()

        missing = []
        if not data["owner_name"]:
            missing.append("Tên chủ xe")
        if not data["owner_phone"] or len(data["owner_phone"]) != 10:
            missing.append("Điện thoại (10 chữ số)")
        if not data["owner_address"]:
            missing.append("Địa chỉ")
        if not data["license_plate"]:
            missing.append("Biển số")
        if data["brand"] == "-- Chọn hiệu xe --":
            missing.append("Hiệu xe")

        if missing:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập:\n- " + "\n- ".join(missing))
            return

        dlg = BienNhanTiepNhanDialog(data, parent=self)
        dlg.exec()