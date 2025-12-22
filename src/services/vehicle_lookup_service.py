# src/services/vehicle_lookup_service.py
"""
Service layer for vehicle lookup operations.
Handles business logic for searching and retrieving vehicle information with debt.
"""

from typing import Optional, Dict, Any, List
import logging
from mysql.connector import Error

from app.database import db_manager

logger = logging.getLogger(__name__)


class VehicleLookupService:
    """Service class for handling vehicle lookup operations."""
    
    @staticmethod
    def get_all_vehicles_with_debt() -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả xe với tổng tiền nợ hiện tại.
        
        Returns:
            List of vehicle dictionaries with LicensePlate, BrandName, OwnerName, TotalDebt
        """
        try:
            query = """
                SELECT 
                    c.LicensePlate,
                    b.BrandName,
                    c.OwnerName,
                    c.PhoneNumber,
                    c.Address,
                    COALESCE(SUM(cr.Debt), 0) as TotalDebt
                FROM CAR c
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                LEFT JOIN CAR_RECEPTION cr ON c.LicensePlate = cr.LicensePlate
                GROUP BY c.LicensePlate, b.BrandName, c.OwnerName, c.PhoneNumber, c.Address
                ORDER BY c.LicensePlate
            """
            vehicles = db_manager.execute_query(query, fetch_all=True)
            return vehicles or []
        except Error as e:
            logger.error(f"Failed to fetch vehicles with debt: {e}")
            return []
    
    @staticmethod
    def search_vehicles(
        license_plate: Optional[str] = None,
        owner_name: Optional[str] = None,
        brand_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Tìm kiếm xe theo các tiêu chí.
        
        Args:
            license_plate: Biển số xe (tìm kiếm gần đúng)
            owner_name: Tên chủ xe (tìm kiếm gần đúng)
            brand_name: Tên hiệu xe (chính xác)
            
        Returns:
            List of vehicle dictionaries matching the criteria
        """
        try:
            # Base query
            query = """
                SELECT 
                    c.LicensePlate,
                    b.BrandName,
                    c.OwnerName,
                    c.PhoneNumber,
                    c.Address,
                    COALESCE(SUM(cr.Debt), 0) as TotalDebt
                FROM CAR c
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                LEFT JOIN CAR_RECEPTION cr ON c.LicensePlate = cr.LicensePlate
                WHERE 1=1
            """
            
            params = []
            
            # Add conditions based on provided filters
            if license_plate:
                query += " AND c.LicensePlate LIKE %s"
                params.append(f"%{license_plate}%")
            
            if owner_name:
                query += " AND c.OwnerName LIKE %s"
                params.append(f"%{owner_name}%")
            
            if brand_name:
                query += " AND b.BrandName = %s"
                params.append(brand_name)
            
            query += """
                GROUP BY c.LicensePlate, b.BrandName, c.OwnerName, c.PhoneNumber, c.Address
                ORDER BY c.LicensePlate
            """
            
            vehicles = db_manager.execute_query(query, params=tuple(params), fetch_all=True)
            return vehicles or []
        except Error as e:
            logger.error(f"Failed to search vehicles: {e}")
            return []
    
    @staticmethod
    def get_vehicle_detail_by_license_plate(license_plate: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin chi tiết của xe theo biển số.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            Vehicle detail dictionary or None
        """
        try:
            query = """
                SELECT 
                    c.LicensePlate,
                    b.BrandName,
                    c.OwnerName,
                    c.PhoneNumber,
                    c.Address,
                    c.Email,
                    COALESCE(SUM(cr.Debt), 0) as TotalDebt
                FROM CAR c
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                LEFT JOIN CAR_RECEPTION cr ON c.LicensePlate = cr.LicensePlate
                WHERE c.LicensePlate = %s
                GROUP BY c.LicensePlate, b.BrandName, c.OwnerName, 
                         c.PhoneNumber, c.Address, c.Email
            """
            result = db_manager.execute_query(query, params=(license_plate,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get vehicle detail for {license_plate}: {e}")
            return None
    
    @staticmethod
    def get_vehicle_reception_history(license_plate: str) -> List[Dict[str, Any]]:
        """
        Lấy lịch sử tiếp nhận của xe.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            List of reception history dictionaries
        """
        try:
            query = """
                SELECT 
                    cr.ReceptionId,
                    cr.ReceptionDate,
                    cr.Debt,
                    COUNT(r.RepairId) as RepairCount,
                    COALESCE(SUM(r.RepairMoney), 0) as TotalRepairMoney
                FROM CAR_RECEPTION cr
                LEFT JOIN REPAIR r ON cr.ReceptionId = r.ReceptionId
                WHERE cr.LicensePlate = %s
                GROUP BY cr.ReceptionId, cr.ReceptionDate, cr.Debt
                ORDER BY cr.ReceptionDate DESC, cr.ReceptionId DESC
            """
            history = db_manager.execute_query(query, params=(license_plate,), fetch_all=True)
            return history or []
        except Error as e:
            logger.error(f"Failed to get reception history for {license_plate}: {e}")
            return []
    
    @staticmethod
    def get_vehicle_repair_history(license_plate: str) -> List[Dict[str, Any]]:
        """
        Lấy lịch sử sửa chữa của xe.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            List of repair history dictionaries
        """
        try:
            query = """
                SELECT 
                    r.RepairId,
                    r.RepairDate,
                    r.RepairMoney,
                    cr.ReceptionDate,
                    cr.ReceptionId
                FROM REPAIR r
                JOIN CAR_RECEPTION cr ON r.ReceptionId = cr.ReceptionId
                WHERE cr.LicensePlate = %s
                ORDER BY r.RepairDate DESC, r.RepairId DESC
            """
            repairs = db_manager.execute_query(query, params=(license_plate,), fetch_all=True)
            return repairs or []
        except Error as e:
            logger.error(f"Failed to get repair history for {license_plate}: {e}")
            return []
    
    @staticmethod
    def get_all_brands() -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả các hiệu xe từ database.
        
        Returns:
            List of brand dictionaries with BrandId and BrandName
        """
        try:
            query = "SELECT BrandId, BrandName FROM CAR_BRAND ORDER BY BrandName"
            brands = db_manager.execute_query(query, fetch_all=True)
            return brands or []
        except Error as e:
            logger.error(f"Failed to fetch car brands: {e}")
            return []
    
    @staticmethod
    def get_vehicles_by_brand(brand_name: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách xe theo hiệu xe.
        
        Args:
            brand_name: Tên hiệu xe
            
        Returns:
            List of vehicle dictionaries
        """
        try:
            query = """
                SELECT 
                    c.LicensePlate,
                    b.BrandName,
                    c.OwnerName,
                    c.PhoneNumber,
                    COALESCE(SUM(cr.Debt), 0) as TotalDebt
                FROM CAR c
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                LEFT JOIN CAR_RECEPTION cr ON c.LicensePlate = cr.LicensePlate
                WHERE b.BrandName = %s
                GROUP BY c.LicensePlate, b.BrandName, c.OwnerName, c.PhoneNumber
                ORDER BY c.LicensePlate
            """
            vehicles = db_manager.execute_query(query, params=(brand_name,), fetch_all=True)
            return vehicles or []
        except Error as e:
            logger.error(f"Failed to get vehicles for brand {brand_name}: {e}")
            return []
    
    @staticmethod
    def get_vehicles_with_debt_only() -> List[Dict[str, Any]]:
        """
        Lấy danh sách các xe đang có nợ.
        
        Returns:
            List of vehicle dictionaries with debt > 0
        """
        try:
            query = """
                SELECT 
                    c.LicensePlate,
                    b.BrandName,
                    c.OwnerName,
                    c.PhoneNumber,
                    SUM(cr.Debt) as TotalDebt
                FROM CAR c
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                JOIN CAR_RECEPTION cr ON c.LicensePlate = cr.LicensePlate
                WHERE cr.Debt > 0
                GROUP BY c.LicensePlate, b.BrandName, c.OwnerName, c.PhoneNumber
                HAVING SUM(cr.Debt) > 0
                ORDER BY TotalDebt DESC
            """
            vehicles = db_manager.execute_query(query, fetch_all=True)
            return vehicles or []
        except Error as e:
            logger.error(f"Failed to get vehicles with debt: {e}")
            return []
