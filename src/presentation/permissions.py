# src/presentation/permissions.py
"""
Role-based permissions module.
Defines which pages each role can access.
"""

from typing import List


class Roles:
    """Available roles in the system."""
    ADMIN = "ADMIN"
    STAFF = "STAFF"


class PagePermissions:
    """Page identifiers for permission checking."""
    TIEP_NHAN_XE = "tiep_nhan_xe"
    PHIEU_SUA_CHUA = "phieu_sua_chua"
    TRA_CUU_XE = "tra_cuu_xe"
    PHIEU_THU = "phieu_thu"
    BAO_CAO_DOANH_SO = "bao_cao_doanh_so"
    BAO_CAO_TON = "bao_cao_ton"
    QUAN_LY_DANH_MUC = "quan_ly_danh_muc"
    THAY_DOI_QUY_DINH = "thay_doi_quy_dinh"
    QUAN_LY_USER = "quan_ly_user"
    NHAP_VAT_TU = "nhap_vat_tu"


# Define permissions for each role
ROLE_PERMISSIONS = {
    Roles.ADMIN: [
        PagePermissions.TIEP_NHAN_XE,
        PagePermissions.PHIEU_SUA_CHUA,
        PagePermissions.TRA_CUU_XE,
        PagePermissions.PHIEU_THU,
        PagePermissions.BAO_CAO_DOANH_SO,
        PagePermissions.BAO_CAO_TON,
        PagePermissions.QUAN_LY_DANH_MUC,
        PagePermissions.THAY_DOI_QUY_DINH,
        PagePermissions.QUAN_LY_USER,
        PagePermissions.NHAP_VAT_TU,
    ],
    Roles.STAFF: [
        PagePermissions.TIEP_NHAN_XE,
        PagePermissions.PHIEU_SUA_CHUA,
        PagePermissions.TRA_CUU_XE,
        PagePermissions.PHIEU_THU,
    ],
}


def can_access(role: str, page_id: str) -> bool:
    """
    Check if a role has permission to access a specific page.
    
    Args:
        role: The user's role (ADMIN or STAFF)
        page_id: The page identifier to check access for
        
    Returns:
        True if the role can access the page, False otherwise
    """
    if role not in ROLE_PERMISSIONS:
        return False
    return page_id in ROLE_PERMISSIONS[role]


def get_accessible_pages(role: str) -> List[str]:
    """
    Get list of page IDs that a role can access.
    
    Args:
        role: The user's role (ADMIN or STAFF)
        
    Returns:
        List of page identifiers the role can access
    """
    return ROLE_PERMISSIONS.get(role, [])
