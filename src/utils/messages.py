# src/utils/messages.py
"""
Message constants for the application.
Contains all user-facing messages in Vietnamese.
"""


class Messages:
    """Container for all application messages."""
    
    # Login messages
    LOGIN_TITLE = "Dang nhap"
    LOGIN_USERNAME = "Ten dang nhap:"
    LOGIN_PASSWORD = "Mat khau:"
    LOGIN_BUTTON = "Dang nhap"
    LOGIN_FAILED = "Dang nhap that bai"
    LOGIN_FAILED_MSG = "Ten dang nhap hoac mat khau khong dung!"
    
    # Main window messages
    APP_TITLE = "He thong Quan ly Garage Oto"
    ACCESS_DENIED = "Tu choi truy cap"
    ACCESS_DENIED_MSG = "Ban khong co quyen truy cap chuc nang nay!"
    
    # Navigation items
    NAV_TIEP_NHAN_XE = "Tiep nhan xe"
    NAV_PHIEU_SUA_CHUA = "Phieu sua chua"
    NAV_TRA_CUU_XE = "Tra cuu xe"
    NAV_PHIEU_THU = "Phieu thu tien"
    NAV_BAO_CAO_DOANH_SO = "Bao cao doanh so"
    NAV_BAO_CAO_TON = "Bao cao ton"
    NAV_QUAN_LY_DANH_MUC = "Quan ly danh muc"
    NAV_THAY_DOI_QUY_DINH = "Thay doi quy dinh"
    NAV_QUAN_LY_USER = "Quan ly nguoi dung"
    
    # Page titles
    PAGE_TIEP_NHAN_XE_TITLE = "TIEP NHAN XE"
    PAGE_TIEP_NHAN_XE_DESC = "Tiep nhan xe cua khach hang vao garage de sua chua, bao duong."
    
    PAGE_PHIEU_SUA_CHUA_TITLE = "LAP PHIEU SUA CHUA"
    PAGE_PHIEU_SUA_CHUA_DESC = "Tao phieu sua chua cho xe da duoc tiep nhan."
    
    PAGE_TRA_CUU_XE_TITLE = "TRA CUU XE"
    PAGE_TRA_CUU_XE_DESC = "Tim kiem thong tin xe trong he thong."
    
    PAGE_PHIEU_THU_TITLE = "LAP PHIEU THU TIEN"
    PAGE_PHIEU_THU_DESC = "Tao phieu thu tien cho khach hang."
    
    PAGE_BAO_CAO_DOANH_SO_TITLE = "BAO CAO DOANH SO"
    PAGE_BAO_CAO_DOANH_SO_DESC = "Xem bao cao doanh so theo thang."
    
    PAGE_BAO_CAO_TON_TITLE = "BAO CAO TON"
    PAGE_BAO_CAO_TON_DESC = "Xem bao cao ton kho vat tu, phu tung."
    
    PAGE_QUAN_LY_DANH_MUC_TITLE = "QUAN LY DANH MUC"
    PAGE_QUAN_LY_DANH_MUC_DESC = "Quan ly danh muc hieu xe, vat tu, tien cong."
    
    PAGE_THAY_DOI_QUY_DINH_TITLE = "THAY DOI QUY DINH"
    PAGE_THAY_DOI_QUY_DINH_DESC = "Cau hinh cac quy dinh cua he thong."
    
    PAGE_QUAN_LY_USER_TITLE = "QUAN LY NGUOI DUNG"
    PAGE_QUAN_LY_USER_DESC = "Quan ly tai khoan nguoi dung trong he thong."
