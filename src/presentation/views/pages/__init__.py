# src/presentation/views/pages/__init__.py
"""
Pages module.
Contains all page widgets for the application.
"""

from presentation.views.pages.tiep_nhan_xe_page import TiepNhanXePage
from presentation.views.pages.phieu_sua_chua_page import PhieuSuaChuaPage
from presentation.views.pages.tra_cuu_xe_page import TraCuuXePage
from presentation.views.pages.phieu_thu_page import PhieuThuPage
from presentation.views.pages.bao_cao_doanh_so_page import BaoCaoDoanhSoPage
from presentation.views.pages.bao_cao_ton_page import BaoCaoTonPage
# from presentation.views.pages.quan_ly_danh_muc_page import QuanLyDanhMucPage
from presentation.views.pages.thay_doi_quy_dinh_page import ThayDoiQuyDinhPage
# from presentation.views.pages.quan_ly_user_page import QuanLyUserPage
from presentation.views.pages.nhap_vat_tu_page import NhapVatTuPage

__all__ = [
    "TiepNhanXePage",
    "PhieuSuaChuaPage",
    "TraCuuXePage",
    "PhieuThuPage",
    "BaoCaoDoanhSoPage",
    "BaoCaoTonPage",
    # "QuanLyDanhMucPage",
    "ThayDoiQuyDinhPage",
    # "QuanLyUserPage",
    "NhapVatTuPage",
]
