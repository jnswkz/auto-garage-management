# src/services/repair_service.py
"""
Service layer for repair operations.
Handles business logic for creating repair tickets and managing repair details.
"""

from typing import Optional, Dict, Any, List
import logging
from mysql.connector import Error

from app.database import db_manager

logger = logging.getLogger(__name__)


class RepairService:
    """Service class for handling repair ticket operations."""
    
    @staticmethod
    def get_all_supplies() -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả vật tư/phụ tùng từ database.
        
        Returns:
            List of supply dictionaries with SuppliesId, SuppliesName, SuppliesPrice, InventoryNumber
        """
        try:
            query = """
                SELECT SuppliesId, SuppliesName, SuppliesPrice, InventoryNumber 
                FROM SUPPLIES 
                ORDER BY SuppliesName
            """
            supplies = db_manager.execute_query(query, fetch_all=True)
            return supplies or []
        except Error as e:
            logger.error(f"Failed to fetch supplies: {e}")
            return []
    
    @staticmethod
    def get_all_wages() -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả loại công việc/tiền công từ database.
        
        Returns:
            List of wage dictionaries with WageId, WageName, WageValue
        """
        try:
            query = "SELECT WageId, WageName, WageValue FROM WAGE ORDER BY WageName"
            wages = db_manager.execute_query(query, fetch_all=True)
            return wages or []
        except Error as e:
            logger.error(f"Failed to fetch wages: {e}")
            return []
    
    @staticmethod
    def get_supply_by_name(supply_name: str) -> Optional[Dict[str, Any]]:
        """
        Tìm thông tin vật tư theo tên.
        
        Args:
            supply_name: Tên vật tư
            
        Returns:
            Supply information dictionary or None
        """
        try:
            query = """
                SELECT SuppliesId, SuppliesName, SuppliesPrice, InventoryNumber 
                FROM SUPPLIES 
                WHERE SuppliesName = %s
            """
            result = db_manager.execute_query(query, params=(supply_name,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get supply {supply_name}: {e}")
            return None
    
    @staticmethod
    def get_wage_by_name(wage_name: str) -> Optional[Dict[str, Any]]:
        """
        Tìm thông tin tiền công theo tên.
        
        Args:
            wage_name: Tên loại công việc
            
        Returns:
            Wage information dictionary or None
        """
        try:
            query = "SELECT WageId, WageName, WageValue FROM WAGE WHERE WageName = %s"
            result = db_manager.execute_query(query, params=(wage_name,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get wage {wage_name}: {e}")
            return None
    
    @staticmethod
    def get_latest_reception_by_license_plate(license_plate: str) -> Optional[Dict[str, Any]]:
        """
        Lấy phiếu tiếp nhận mới nhất của xe theo biển số.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            Reception information dictionary or None
        """
        try:
            query = """
                SELECT cr.ReceptionId, cr.LicensePlate, cr.ReceptionDate, cr.Debt,
                       c.OwnerName, c.PhoneNumber, b.BrandName
                FROM CAR_RECEPTION cr
                JOIN CAR c ON cr.LicensePlate = c.LicensePlate
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                WHERE cr.LicensePlate = %s
                ORDER BY cr.ReceptionDate DESC, cr.ReceptionId DESC
                LIMIT 1
            """
            result = db_manager.execute_query(query, params=(license_plate,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get latest reception for {license_plate}: {e}")
            return None
    
    @staticmethod
    def create_repair_ticket(
        reception_id: int,
        repair_date: str,
        repair_money: float,
        details: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Tạo phiếu sửa chữa mới với chi tiết.
        
        Args:
            reception_id: ID phiếu tiếp nhận
            repair_date: Ngày sửa chữa (format: YYYY-MM-DD)
            repair_money: Tổng tiền sửa chữa
            details: List of repair detail dictionaries containing:
                - content: Nội dung sửa chữa
                - supply_name: Tên vật tư
                - supply_amount: Số lượng vật tư
                - wage_name: Tên tiền công (optional)
        
        Returns:
            Dictionary with success status, repair_id, and message
        """
        try:
            with db_manager.transaction() as cursor:
                # 1. Tạo phiếu sửa chữa
                cursor.execute("""
                    INSERT INTO REPAIR (ReceptionId, RepairDate, RepairMoney)
                    VALUES (%s, %s, %s)
                """, (reception_id, repair_date, repair_money))
                
                repair_id = cursor.lastrowid
                
                # 2. Thêm chi tiết sửa chữa
                for detail in details:
                    # Lấy SuppliesId từ tên vật tư
                    cursor.execute(
                        "SELECT SuppliesId FROM SUPPLIES WHERE SuppliesName = %s",
                        (detail['supply_name'],)
                    )
                    supply_result = cursor.fetchone()
                    
                    if not supply_result:
                        return {
                            'success': False,
                            'message': f"Không tìm thấy vật tư: {detail['supply_name']}"
                        }
                    
                    supply_id = supply_result['SuppliesId']
                    
                    # Lấy WageId từ tên tiền công (nếu có)
                    wage_id = None
                    if detail.get('wage_name') and detail['wage_name'] != "-- Chọn tiền công --":
                        cursor.execute(
                            "SELECT WageId FROM WAGE WHERE WageName = %s",
                            (detail['wage_name'],)
                        )
                        wage_result = cursor.fetchone()
                        if wage_result:
                            wage_id = wage_result['WageId']
                    
                    # Thêm chi tiết sửa chữa
                    cursor.execute("""
                        INSERT INTO REPAIR_DETAILS 
                        (RepairId, Content, SuppliesId, SuppliesAmount, WageId)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        repair_id,
                        detail['content'],
                        supply_id,
                        detail['supply_amount'],
                        wage_id
                    ))
                    
                    # Cập nhật số lượng tồn kho
                    cursor.execute("""
                        UPDATE SUPPLIES 
                        SET InventoryNumber = InventoryNumber - %s
                        WHERE SuppliesId = %s
                    """, (detail['supply_amount'], supply_id))
                
                # 3. Cập nhật số nợ trong phiếu tiếp nhận
                cursor.execute("""
                    UPDATE CAR_RECEPTION 
                    SET Debt = Debt + %s
                    WHERE ReceptionId = %s
                """, (repair_money, reception_id))
                
                logger.info(
                    f"Successfully created repair ticket {repair_id} "
                    f"for reception {reception_id}"
                )
                
                return {
                    'success': True,
                    'repair_id': repair_id,
                    'message': 'Tạo phiếu sửa chữa thành công'
                }
                
        except Error as e:
            logger.error(f"Failed to create repair ticket: {e}")
            return {
                'success': False,
                'message': f"Lỗi khi tạo phiếu sửa chữa: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error when creating repair ticket: {e}")
            return {
                'success': False,
                'message': f"Lỗi không xác định: {str(e)}"
            }
    
    @staticmethod
    def get_repair_by_id(repair_id: int) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin phiếu sửa chữa theo ID.
        
        Args:
            repair_id: ID phiếu sửa chữa
            
        Returns:
            Repair information dictionary or None
        """
        try:
            query = """
                SELECT r.RepairId, r.ReceptionId, r.RepairDate, r.RepairMoney,
                       cr.LicensePlate, c.OwnerName, b.BrandName
                FROM REPAIR r
                JOIN CAR_RECEPTION cr ON r.ReceptionId = cr.ReceptionId
                JOIN CAR c ON cr.LicensePlate = c.LicensePlate
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                WHERE r.RepairId = %s
            """
            result = db_manager.execute_query(query, params=(repair_id,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get repair info for ID {repair_id}: {e}")
            return None
    
    @staticmethod
    def get_repair_details(repair_id: int) -> List[Dict[str, Any]]:
        """
        Lấy chi tiết sửa chữa theo ID phiếu sửa chữa.
        
        Args:
            repair_id: ID phiếu sửa chữa
            
        Returns:
            List of repair detail dictionaries
        """
        try:
            query = """
                SELECT rd.RepairDetailId, rd.Content,
                       s.SuppliesName, rd.SuppliesAmount, s.SuppliesPrice,
                       w.WageName, w.WageValue
                FROM REPAIR_DETAILS rd
                JOIN SUPPLIES s ON rd.SuppliesId = s.SuppliesId
                LEFT JOIN WAGE w ON rd.WageId = w.WageId
                WHERE rd.RepairId = %s
                ORDER BY rd.RepairDetailId
            """
            details = db_manager.execute_query(query, params=(repair_id,), fetch_all=True)
            return details or []
        except Error as e:
            logger.error(f"Failed to get repair details for repair {repair_id}: {e}")
            return []
    
    @staticmethod
    def check_supply_inventory(supply_name: str, required_amount: int) -> Dict[str, Any]:
        """
        Kiểm tra tồn kho vật tư có đủ không.
        
        Args:
            supply_name: Tên vật tư
            required_amount: Số lượng cần dùng
            
        Returns:
            Dictionary with available status and current inventory
        """
        try:
            supply = RepairService.get_supply_by_name(supply_name)
            if not supply:
                return {
                    'available': False,
                    'message': f"Không tìm thấy vật tư: {supply_name}",
                    'current_inventory': 0
                }
            
            current_inventory = supply['InventoryNumber']
            if current_inventory < required_amount:
                return {
                    'available': False,
                    'message': f"Vật tư {supply_name} không đủ tồn kho. Hiện có: {current_inventory}, cần: {required_amount}",
                    'current_inventory': current_inventory
                }
            
            return {
                'available': True,
                'message': 'Đủ tồn kho',
                'current_inventory': current_inventory
            }
        except Exception as e:
            logger.error(f"Error checking inventory for {supply_name}: {e}")
            return {
                'available': False,
                'message': f"Lỗi khi kiểm tra tồn kho: {str(e)}",
                'current_inventory': 0
            }
