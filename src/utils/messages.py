# src/utils/messages.py
"""
Message constants for the application.
Contains all user-facing messages in Vietnamese.
"""


class Messages:
    """Container for all application messages."""
    
    # Login messages
    LOGIN_TITLE = "Đăng nhập"
    LOGIN_USERNAME = "Tên đăng nhập:"
    LOGIN_PASSWORD = "Mật khẩu:"
    LOGIN_BUTTON = "Đăng nhập"
    LOGIN_FAILED = "Đăng nhập thất bại"
    LOGIN_FAILED_MSG = "Tên đăng nhập hoặc mật khẩu không đúng!"
    
    # Main window messages
    APP_TITLE = "Hệ thống Quản lý Garage Ôtô"
    ACCESS_DENIED = "Từ chối truy cập"
    ACCESS_DENIED_MSG = "Bạn không có quyền truy cập chức năng này!"
    
    # Navigation items
    NAV_TIEP_NHAN_XE = "Tiếp nhận xe"
    NAV_PHIEU_SUA_CHUA = "Phiếu sửa chữa"
    NAV_TRA_CUU_XE = "Tra cứu xe"
    NAV_PHIEU_THU = "Phiếu thu tiền"
    NAV_BAO_CAO_DOANH_SO = "Báo cáo doanh số"
    NAV_BAO_CAO_TON = "Báo cáo tồn"
    NAV_QUAN_LY_DANH_MUC = "Quản lý danh mục"
    NAV_THAY_DOI_QUY_DINH = "Thay đổi quy định"
    NAV_QUAN_LY_USER = "Quản lý người dùng"
    
    # Page titles
    PAGE_TIEP_NHAN_XE_TITLE = "TIẾP NHẬN XE"
    PAGE_TIEP_NHAN_XE_DESC = "Tiếp nhận xe của khách hàng vào garage để sửa chữa, bảo dưỡng."
    
    PAGE_PHIEU_SUA_CHUA_TITLE = "LẬP PHIẾU SỬA CHỮA"
    PAGE_PHIEU_SUA_CHUA_DESC = "Tạo phiếu sửa chữa cho xe đã được tiếp nhận."
    
    PAGE_TRA_CUU_XE_TITLE = "TRA CỨU XE"
    PAGE_TRA_CUU_XE_DESC = "Tìm kiếm thông tin xe trong hệ thống."
    
    PAGE_PHIEU_THU_TITLE = "LẬP PHIẾU THU TIỀN"
    PAGE_PHIEU_THU_DESC = "Tạo phiếu thu tiền cho khách hàng."
    
    PAGE_BAO_CAO_DOANH_SO_TITLE = "BÁO CÁO DOANH SỐ"
    PAGE_BAO_CAO_DOANH_SO_DESC = "Xem báo cáo doanh số theo tháng."
    
    PAGE_BAO_CAO_TON_TITLE = "BÁO CÁO TỒN"
    PAGE_BAO_CAO_TON_DESC = "Xem báo cáo tồn kho vật tư, phụ tùng."
    
    PAGE_QUAN_LY_DANH_MUC_TITLE = "QUẢN LÝ DANH MỤC"
    PAGE_QUAN_LY_DANH_MUC_DESC = "Quản lý danh mục hiệu xe, vật tư, tiền công."
    
    PAGE_THAY_DOI_QUY_DINH_TITLE = "THAY ĐỔI QUY ĐỊNH"
    PAGE_THAY_DOI_QUY_DINH_DESC = "Cấu hình các quy định của hệ thống."
    
    PAGE_QUAN_LY_USER_TITLE = "QUẢN LÝ NGƯỜI DÙNG"
    PAGE_QUAN_LY_USER_DESC = "Quản lý tài khoản người dùng trong hệ thống."

    NAV_NHAP_VAT_TU = "Nhập vật tư"
    PAGE_NHAP_VAT_TU_TITLE = "NHẬP VẬT TƯ"
    PAGE_NHAP_VAT_TU_DESC = "Tạo phiếu nhập vật tư vào kho."

