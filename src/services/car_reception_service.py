# src/services/car_reception_service.py
"""
Service layer for car reception operations.
Handles business logic for receiving cars into the garage.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from mysql.connector import Error

from app.database import db_manager

logger = logging.getLogger(__name__)


class CarReceptionService:
    """Service class for handling car reception operations."""
    
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
    def get_brand_id_by_name(brand_name: str) -> Optional[int]:
        """
        Lấy BrandId từ tên hiệu xe.
        
        Args:
            brand_name: Tên hiệu xe
            
        Returns:
            BrandId nếu tìm thấy, None nếu không tìm thấy
        """
        try:
            query = "SELECT BrandId FROM CAR_BRAND WHERE BrandName = %s"
            result = db_manager.execute_query(query, params=(brand_name,), fetch_one=True)
            return result['BrandId'] if result else None
        except Error as e:
            logger.error(f"Failed to get brand ID for {brand_name}: {e}")
            return None
    
    @staticmethod
    def get_car_by_license_plate(license_plate: str) -> Optional[Dict[str, Any]]:
        """
        Tìm thông tin xe theo biển số.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            Car information dictionary or None if not found
        """
        try:
            query = """
                SELECT c.LicensePlate, c.BrandId, b.BrandName, c.OwnerName, 
                       c.PhoneNumber, c.Address, c.Email
                FROM CAR c
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                WHERE c.LicensePlate = %s
            """
            result = db_manager.execute_query(query, params=(license_plate,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get car info for {license_plate}: {e}")
            return None
    
    @staticmethod
    def get_max_car_reception_limit() -> int:
        """
        Lấy giới hạn số lượng xe tiếp nhận trong ngày từ bảng PARAMETER.
        
        Returns:
            Số lượng xe tối đa (mặc định 30)
        """
        try:
            query = "SELECT value FROM PARAMETER WHERE name = 'MaxCarReception'"
            result = db_manager.execute_query(query, fetch_one=True)
            return result['value'] if result else 30
        except Error as e:
            logger.error(f"Failed to get max car reception limit: {e}")
            return 30
    
    @staticmethod
    def get_daily_reception_count(reception_date: str) -> int:
        """
        Đếm số xe đã tiếp nhận trong ngày.
        
        Args:
            reception_date: Ngày tiếp nhận (format: YYYY-MM-DD)
            
        Returns:
            Số lượng xe đã tiếp nhận
        """
        try:
            query = "SELECT COUNT(*) as count FROM CAR_RECEPTION WHERE ReceptionDate = %s"
            result = db_manager.execute_query(query, params=(reception_date,), fetch_one=True)
            return result['count'] if result else 0
        except Error as e:
            logger.error(f"Failed to get daily reception count: {e}")
            return 0
    
    @staticmethod
    def create_or_update_car(
        license_plate: str,
        brand_id: int,
        owner_name: str,
        phone_number: str,
        address: str,
        email: Optional[str] = None
    ) -> bool:
        """
        Tạo mới hoặc cập nhật thông tin xe.
        Nếu xe đã tồn tại, cập nhật thông tin chủ xe.
        
        Args:
            license_plate: Biển số xe
            brand_id: ID hiệu xe
            owner_name: Tên chủ xe
            phone_number: Số điện thoại
            address: Địa chỉ
            email: Email (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Kiểm tra xe đã tồn tại chưa
            existing_car = CarReceptionService.get_car_by_license_plate(license_plate)
            
            if existing_car:
                # Cập nhật thông tin xe
                update_query = """
                    UPDATE CAR 
                    SET BrandId = %s, OwnerName = %s, PhoneNumber = %s, 
                        Address = %s, Email = %s
                    WHERE LicensePlate = %s
                """
                db_manager.execute_update(
                    update_query,
                    params=(brand_id, owner_name, phone_number, address, email, license_plate)
                )
                logger.info(f"Updated car information for {license_plate}")
            else:
                # Thêm xe mới
                insert_query = """
                    INSERT INTO CAR (LicensePlate, BrandId, OwnerName, PhoneNumber, Address, Email)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                db_manager.execute_insert(
                    insert_query,
                    params=(license_plate, brand_id, owner_name, phone_number, address, email)
                )
                logger.info(f"Created new car record for {license_plate}")
            
            return True
        except Error as e:
            logger.error(f"Failed to create/update car {license_plate}: {e}")
            return False
    
    @staticmethod
    def create_car_reception(
        license_plate: str,
        reception_date: str,
        initial_debt: float = 0.0
    ) -> Optional[int]:
        """
        Tạo phiếu tiếp nhận xe mới.
        
        Args:
            license_plate: Biển số xe
            reception_date: Ngày tiếp nhận (format: YYYY-MM-DD)
            initial_debt: Số nợ ban đầu (mặc định 0)
            
        Returns:
            ReceptionId if successful, None otherwise
        """
        try:
            # Kiểm tra giới hạn số xe trong ngày (trigger sẽ kiểm tra nhưng ta check trước)
            max_limit = CarReceptionService.get_max_car_reception_limit()
            current_count = CarReceptionService.get_daily_reception_count(reception_date)
            
            if current_count >= max_limit:
                logger.warning(f"Daily reception limit reached: {current_count}/{max_limit}")
                raise ValueError(f"Đã đạt giới hạn tiếp nhận xe trong ngày ({max_limit} xe)")
            
            # Tạo phiếu tiếp nhận
            insert_query = """
                INSERT INTO CAR_RECEPTION (LicensePlate, ReceptionDate, Debt)
                VALUES (%s, %s, %s)
            """
            reception_id = db_manager.execute_insert(
                insert_query,
                params=(license_plate, reception_date, initial_debt)
            )
            
            logger.info(f"Created car reception {reception_id} for {license_plate} on {reception_date}")
            return reception_id
        except Error as e:
            logger.error(f"Failed to create car reception: {e}")
            # Check if it's the trigger error
            if "45000" in str(e):  # SQLSTATE for custom error
                raise ValueError("Số lượng xe tiếp nhận trong ngày đã vượt quá quy định")
            raise
        except ValueError:
            raise
    
    @staticmethod
    def receive_car(
        license_plate: str,
        brand_name: str,
        owner_name: str,
        phone_number: str,
        address: str,
        reception_date: str,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Xử lý toàn bộ quy trình tiếp nhận xe.
        Bao gồm: tạo/cập nhật thông tin xe và tạo phiếu tiếp nhận.
        
        Args:
            license_plate: Biển số xe
            brand_name: Tên hiệu xe
            owner_name: Tên chủ xe
            phone_number: Số điện thoại
            address: Địa chỉ
            reception_date: Ngày tiếp nhận (format: YYYY-MM-DD)
            email: Email (optional)
            
        Returns:
            Dictionary with success status, reception_id, and message
        """
        try:
            # Sử dụng transaction để đảm bảo tính toàn vẹn dữ liệu
            with db_manager.transaction() as cursor:
                # 1. Lấy BrandId từ tên hiệu xe
                brand_id = CarReceptionService.get_brand_id_by_name(brand_name)
                if not brand_id:
                    return {
                        'success': False,
                        'message': f"Không tìm thấy hiệu xe: {brand_name}"
                    }
                
                # 2. Tạo hoặc cập nhật thông tin xe
                cursor.execute("""
                    SELECT LicensePlate FROM CAR WHERE LicensePlate = %s
                """, (license_plate,))
                existing_car = cursor.fetchone()
                
                if existing_car:
                    # Cập nhật thông tin xe
                    cursor.execute("""
                        UPDATE CAR 
                        SET BrandId = %s, OwnerName = %s, PhoneNumber = %s, 
                            Address = %s, Email = %s
                        WHERE LicensePlate = %s
                    """, (brand_id, owner_name, phone_number, address, email, license_plate))
                else:
                    # Thêm xe mới
                    cursor.execute("""
                        INSERT INTO CAR (LicensePlate, BrandId, OwnerName, PhoneNumber, Address, Email)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (license_plate, brand_id, owner_name, phone_number, address, email))
                
                # 3. Kiểm tra giới hạn tiếp nhận trong ngày
                cursor.execute("SELECT value FROM PARAMETER WHERE name = 'MaxCarReception'")
                max_result = cursor.fetchone()
                max_limit = max_result['value'] if max_result else 30
                
                cursor.execute(
                    "SELECT COUNT(*) as count FROM CAR_RECEPTION WHERE ReceptionDate = %s",
                    (reception_date,)
                )
                count_result = cursor.fetchone()
                current_count = count_result['count'] if count_result else 0
                
                if current_count >= max_limit:
                    return {
                        'success': False,
                        'message': f"Đã đạt giới hạn tiếp nhận xe trong ngày ({max_limit} xe)"
                    }
                
                # 4. Tạo phiếu tiếp nhận
                cursor.execute("""
                    INSERT INTO CAR_RECEPTION (LicensePlate, ReceptionDate, Debt)
                    VALUES (%s, %s, 0)
                """, (license_plate, reception_date))
                
                reception_id = cursor.lastrowid
                
                logger.info(
                    f"Successfully received car {license_plate} with reception ID {reception_id}"
                )
                
                return {
                    'success': True,
                    'reception_id': reception_id,
                    'message': 'Tiếp nhận xe thành công',
                    'data': {
                        'license_plate': license_plate,
                        'owner_name': owner_name,
                        'brand_name': brand_name,
                        'reception_date': reception_date
                    }
                }
                
        except Error as e:
            logger.error(f"Failed to receive car {license_plate}: {e}")
            # Check if it's a trigger error
            error_message = str(e)
            if "45000" in error_message or "vượt quá quy định" in error_message:
                return {
                    'success': False,
                    'message': "Số lượng xe tiếp nhận trong ngày đã vượt quá quy định (MaxCarReception)"
                }
            return {
                'success': False,
                'message': f"Lỗi khi tiếp nhận xe: {error_message}"
            }
        except Exception as e:
            logger.error(f"Unexpected error when receiving car {license_plate}: {e}")
            return {
                'success': False,
                'message': f"Lỗi không xác định: {str(e)}"
            }
    
    @staticmethod
    def get_reception_by_id(reception_id: int) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin phiếu tiếp nhận theo ID.
        
        Args:
            reception_id: ID phiếu tiếp nhận
            
        Returns:
            Reception information dictionary or None
        """
        try:
            query = """
                SELECT cr.ReceptionId, cr.LicensePlate, cr.ReceptionDate, cr.Debt,
                       c.OwnerName, c.PhoneNumber, c.Address, c.Email,
                       b.BrandName
                FROM CAR_RECEPTION cr
                JOIN CAR c ON cr.LicensePlate = c.LicensePlate
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                WHERE cr.ReceptionId = %s
            """
            result = db_manager.execute_query(query, params=(reception_id,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get reception info for ID {reception_id}: {e}")
            return None
