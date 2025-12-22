# src/services/system_settings_service.py
"""
Business logic cho Thay đổi quy định hệ thống (QĐ6).
Xử lý CRUD cho CAR_BRAND, PARAMETER, SUPPLIES, WAGE.
"""

from typing import List, Dict, Optional, Tuple
import logging

from app.database import db_manager

logger = logging.getLogger(__name__)


class SystemSettingsService:
    """
    Service quản lý quy định hệ thống:
    - QĐ6.1: Số xe tối đa/ngày + danh sách hiệu xe
    - QĐ6.2: Danh mục vật tư/phụ tùng + danh mục tiền công
    """
    
    def __init__(self):
        """Khởi tạo service."""
        pass
    
    # ==================== PARAMETER (MaxCarReception) ====================
    
    def get_max_cars_per_day(self) -> int:
        """
        Lấy số xe sửa chữa tối đa trong ngày.
        
        Returns:
            Số xe tối đa (default: 30)
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT value FROM PARAMETER WHERE name = 'MaxCarReception'"
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                
                return result[0] if result else 30
                
        except Exception as e:
            logger.error(f"Error getting max cars per day: {e}")
            raise
    
    def set_max_cars_per_day(self, value: int):
        """
        Cập nhật số xe sửa chữa tối đa trong ngày.
        
        Args:
            value: Số xe tối đa (phải > 0)
            
        Raises:
            ValueError: Nếu value <= 0
        """
        if value <= 0:
            raise ValueError("Số xe tối đa phải > 0")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    INSERT INTO PARAMETER (name, value) 
                    VALUES ('MaxCarReception', %s)
                    ON DUPLICATE KEY UPDATE value = %s
                """
                cursor.execute(query, (value, value))
                cursor.close()
                conn.commit()
                logger.info(f"Updated MaxCarReception to {value}")
                
        except Exception as e:
            logger.error(f"Error setting max cars per day: {e}")
            raise
    
    # ==================== CAR_BRAND ====================
    
    def get_all_brands(self) -> List[Dict[str, any]]:
        """
        Lấy danh sách tất cả hiệu xe.
        
        Returns:
            List[{'id': int, 'name': str}]
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT BrandId, BrandName FROM CAR_BRAND ORDER BY BrandName"
                cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()
                
                return [{'id': row[0], 'name': row[1]} for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting brands: {e}")
            raise
    
    def add_brand(self, name: str) -> int:
        """
        Thêm hiệu xe mới.
        
        Args:
            name: Tên hiệu xe (không được trùng)
            
        Returns:
            BrandId của hiệu xe vừa thêm
            
        Raises:
            ValueError: Nếu tên rỗng hoặc đã tồn tại
        """
        name = name.strip()
        if not name:
            raise ValueError("Tên hiệu xe không được rỗng")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO CAR_BRAND (BrandName) VALUES (%s)"
                cursor.execute(query, (name,))
                brand_id = cursor.lastrowid
                cursor.close()
                conn.commit()
                logger.info(f"Added brand: {name} (ID: {brand_id})")
                return brand_id
                
        except Exception as e:
            if "Duplicate entry" in str(e):
                raise ValueError(f"Hiệu xe '{name}' đã tồn tại")
            logger.error(f"Error adding brand: {e}")
            raise
    
    def update_brand(self, brand_id: int, new_name: str):
        """
        Cập nhật tên hiệu xe.
        
        Args:
            brand_id: ID hiệu xe
            new_name: Tên mới
            
        Raises:
            ValueError: Nếu tên rỗng hoặc đã tồn tại
        """
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("Tên hiệu xe không được rỗng")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "UPDATE CAR_BRAND SET BrandName = %s WHERE BrandId = %s"
                cursor.execute(query, (new_name, brand_id))
                cursor.close()
                conn.commit()
                logger.info(f"Updated brand ID {brand_id} to: {new_name}")
                
        except Exception as e:
            if "Duplicate entry" in str(e):
                raise ValueError(f"Hiệu xe '{new_name}' đã tồn tại")
            logger.error(f"Error updating brand: {e}")
            raise
    
    def delete_brand(self, brand_id: int):
        """
        Xóa hiệu xe.
        
        Args:
            brand_id: ID hiệu xe
            
        Raises:
            ValueError: Nếu hiệu xe đang được sử dụng trong CAR
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Kiểm tra có xe nào đang dùng hiệu này không
                check_query = "SELECT COUNT(*) FROM CAR WHERE BrandId = %s"
                cursor.execute(check_query, (brand_id,))
                count = cursor.fetchone()[0]
                
                if count > 0:
                    cursor.close()
                    raise ValueError(f"Không thể xóa hiệu xe đang được sử dụng bởi {count} xe")
                
                # Xóa hiệu xe
                delete_query = "DELETE FROM CAR_BRAND WHERE BrandId = %s"
                cursor.execute(delete_query, (brand_id,))
                cursor.close()
                conn.commit()
                logger.info(f"Deleted brand ID: {brand_id}")
                
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error deleting brand: {e}")
            raise
    
    # ==================== SUPPLIES ====================
    
    def get_all_supplies(self) -> List[Dict[str, any]]:
        """
        Lấy danh sách tất cả vật tư/phụ tùng.
        
        Returns:
            List[{'id': int, 'name': str, 'price': float}]
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT SuppliesId, SuppliesName, SuppliesPrice FROM SUPPLIES ORDER BY SuppliesName"
                cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()
                
                return [{'id': row[0], 'name': row[1], 'price': float(row[2])} for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting supplies: {e}")
            raise
    
    def add_supply(self, name: str, price: float) -> int:
        """
        Thêm vật tư mới.
        
        Args:
            name: Tên vật tư (không được trùng)
            price: Đơn giá (phải > 0)
            
        Returns:
            SuppliesId của vật tư vừa thêm
            
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        name = name.strip()
        if not name:
            raise ValueError("Tên vật tư không được rỗng")
        if price <= 0:
            raise ValueError("Đơn giá phải > 0")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO SUPPLIES (SuppliesName, SuppliesPrice) VALUES (%s, %s)"
                cursor.execute(query, (name, price))
                supply_id = cursor.lastrowid
                cursor.close()
                conn.commit()
                logger.info(f"Added supply: {name} @ {price} (ID: {supply_id})")
                return supply_id
                
        except Exception as e:
            logger.error(f"Error adding supply: {e}")
            raise
    
    def update_supply(self, supply_id: int, name: str, price: float):
        """
        Cập nhật thông tin vật tư.
        
        Args:
            supply_id: ID vật tư
            name: Tên mới
            price: Đơn giá mới
            
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        name = name.strip()
        if not name:
            raise ValueError("Tên vật tư không được rỗng")
        if price <= 0:
            raise ValueError("Đơn giá phải > 0")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "UPDATE SUPPLIES SET SuppliesName = %s, SuppliesPrice = %s WHERE SuppliesId = %s"
                cursor.execute(query, (name, price, supply_id))
                cursor.close()
                conn.commit()
                logger.info(f"Updated supply ID {supply_id}: {name} @ {price}")
                
        except Exception as e:
            logger.error(f"Error updating supply: {e}")
            raise
    
    def delete_supply(self, supply_id: int):
        """
        Xóa vật tư.
        
        Args:
            supply_id: ID vật tư
            
        Raises:
            ValueError: Nếu vật tư đang được sử dụng
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Kiểm tra REPAIR_DETAILS
                check_query = "SELECT COUNT(*) FROM REPAIR_DETAILS WHERE SuppliesId = %s"
                cursor.execute(check_query, (supply_id,))
                repair_count = cursor.fetchone()[0]
                
                # Kiểm tra STOCK_REPORT_DETAILS
                cursor.execute(
                    "SELECT COUNT(*) FROM STOCK_REPORT_DETAILS WHERE SuppliesId = %s",
                    (supply_id,)
                )
                stock_count = cursor.fetchone()[0]
                
                total_count = repair_count + stock_count
                if total_count > 0:
                    cursor.close()
                    raise ValueError(f"Không thể xóa vật tư đang được sử dụng ({repair_count} phiếu sửa chữa, {stock_count} báo cáo tồn)")
                
                # Xóa vật tư
                delete_query = "DELETE FROM SUPPLIES WHERE SuppliesId = %s"
                cursor.execute(delete_query, (supply_id,))
                cursor.close()
                conn.commit()
                logger.info(f"Deleted supply ID: {supply_id}")
                
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error deleting supply: {e}")
            raise
    
    # ==================== WAGE ====================
    
    def get_all_wages(self) -> List[Dict[str, any]]:
        """
        Lấy danh sách tất cả tiền công.
        
        Returns:
            List[{'id': int, 'name': str, 'value': float}]
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT WageId, WageName, WageValue FROM WAGE ORDER BY WageName"
                cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()
                
                return [{'id': row[0], 'name': row[1], 'value': float(row[2])} for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting wages: {e}")
            raise
    
    def add_wage(self, name: str, value: float) -> int:
        """
        Thêm tiền công mới.
        
        Args:
            name: Tên tiền công (không được trùng)
            value: Giá trị (phải > 0)
            
        Returns:
            WageId của tiền công vừa thêm
            
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        name = name.strip()
        if not name:
            raise ValueError("Tên tiền công không được rỗng")
        if value <= 0:
            raise ValueError("Giá tiền công phải > 0")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO WAGE (WageName, WageValue) VALUES (%s, %s)"
                cursor.execute(query, (name, value))
                wage_id = cursor.lastrowid
                cursor.close()
                conn.commit()
                logger.info(f"Added wage: {name} @ {value} (ID: {wage_id})")
                return wage_id
                
        except Exception as e:
            if "Duplicate entry" in str(e):
                raise ValueError(f"Tiền công '{name}' đã tồn tại")
            logger.error(f"Error adding wage: {e}")
            raise
    
    def update_wage(self, wage_id: int, name: str, value: float):
        """
        Cập nhật thông tin tiền công.
        
        Args:
            wage_id: ID tiền công
            name: Tên mới
            value: Giá trị mới
            
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        name = name.strip()
        if not name:
            raise ValueError("Tên tiền công không được rỗng")
        if value <= 0:
            raise ValueError("Giá tiền công phải > 0")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = "UPDATE WAGE SET WageName = %s, WageValue = %s WHERE WageId = %s"
                cursor.execute(query, (name, value, wage_id))
                cursor.close()
                conn.commit()
                logger.info(f"Updated wage ID {wage_id}: {name} @ {value}")
                
        except Exception as e:
            if "Duplicate entry" in str(e):
                raise ValueError(f"Tiền công '{name}' đã tồn tại")
            logger.error(f"Error updating wage: {e}")
            raise
    
    def delete_wage(self, wage_id: int):
        """
        Xóa tiền công.
        
        Args:
            wage_id: ID tiền công
            
        Raises:
            ValueError: Nếu tiền công đang được sử dụng
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Kiểm tra có phiếu sửa chữa nào đang dùng tiền công này không
                check_query = "SELECT COUNT(*) FROM REPAIR_DETAILS WHERE WageId = %s"
                cursor.execute(check_query, (wage_id,))
                count = cursor.fetchone()[0]
                
                if count > 0:
                    cursor.close()
                    raise ValueError(f"Không thể xóa tiền công đang được sử dụng trong {count} phiếu sửa chữa")
                
                # Xóa tiền công
                delete_query = "DELETE FROM WAGE WHERE WageId = %s"
                cursor.execute(delete_query, (wage_id,))
                cursor.close()
                conn.commit()
                logger.info(f"Deleted wage ID: {wage_id}")
                
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error deleting wage: {e}")
            raise
    
    # ==================== Batch Operations ====================
    
    def save_all_settings(self, 
                         max_cars: int,
                         brands: List[str],
                         supplies: List[Tuple[str, float]],
                         wages: List[Tuple[str, float]]):
        """
        Lưu tất cả cài đặt một lần (transaction).
        
        Args:
            max_cars: Số xe tối đa/ngày
            brands: List tên hiệu xe
            supplies: List (tên vật tư, đơn giá)
            wages: List (tên tiền công, giá trị)
            
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # 1. Update max cars
                cursor.execute(
                    "INSERT INTO PARAMETER (name, value) VALUES ('MaxCarReception', %s) "
                    "ON DUPLICATE KEY UPDATE value = %s",
                    (max_cars, max_cars)
                )
                
                # 2. Sync brands (delete old, insert new)
                # Note: Chỉ xóa brands không được dùng
                cursor.execute("SELECT BrandId FROM CAR_BRAND")
                existing_ids = [row[0] for row in cursor.fetchall()]
                
                for brand_id in existing_ids:
                    cursor.execute("SELECT COUNT(*) FROM CAR WHERE BrandId = %s", (brand_id,))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("DELETE FROM CAR_BRAND WHERE BrandId = %s", (brand_id,))
                
                # Insert new brands
                for brand_name in brands:
                    cursor.execute(
                        "INSERT IGNORE INTO CAR_BRAND (BrandName) VALUES (%s)",
                        (brand_name,)
                    )
                
                # 3. Sync supplies (update existing, insert new, delete unused)
                # Lấy danh sách supplies hiện có với tên và ID
                cursor.execute("SELECT SuppliesId, SuppliesName, SuppliesPrice FROM SUPPLIES")
                existing_supplies = {row[1]: {'id': row[0], 'price': row[2]} for row in cursor.fetchall()}
                
                # Tạo set tên supplies từ UI
                ui_supply_names = {name for name, _ in supplies}
                
                # Update hoặc Insert supplies từ UI
                for name, price in supplies:
                    if name in existing_supplies:
                        # Tồn tại → UPDATE giá nếu khác
                        if float(existing_supplies[name]['price']) != float(price):
                            cursor.execute(
                                "UPDATE SUPPLIES SET SuppliesPrice = %s WHERE SuppliesId = %s",
                                (price, existing_supplies[name]['id'])
                            )
                    else:
                        # Chưa tồn tại → INSERT mới
                        cursor.execute(
                            "INSERT INTO SUPPLIES (SuppliesName, SuppliesPrice) VALUES (%s, %s)",
                            (name, price)
                        )
                
                # Xóa supplies không còn trong UI và không được sử dụng
                for supply_name, supply_info in existing_supplies.items():
                    if supply_name not in ui_supply_names:
                        supply_id = supply_info['id']
                        
                        # Kiểm tra có đang được dùng không
                        cursor.execute(
                            "SELECT COUNT(*) FROM REPAIR_DETAILS WHERE SuppliesId = %s", 
                            (supply_id,)
                        )
                        repair_count = cursor.fetchone()[0]
                        
                        cursor.execute(
                            "SELECT COUNT(*) FROM STOCK_REPORT_DETAILS WHERE SuppliesId = %s", 
                            (supply_id,)
                        )
                        stock_count = cursor.fetchone()[0]
                        
                        # Chỉ xóa nếu không được dùng
                        if repair_count == 0 and stock_count == 0:
                            cursor.execute("DELETE FROM SUPPLIES WHERE SuppliesId = %s", (supply_id,))
                
                # 4. Sync wages (update existing, insert new, delete unused)
                # Lấy danh sách wages hiện có
                cursor.execute("SELECT WageId, WageName, WageValue FROM WAGE")
                existing_wages = {row[1]: {'id': row[0], 'value': row[2]} for row in cursor.fetchall()}
                
                # Tạo set tên wages từ UI
                ui_wage_names = {name for name, _ in wages}
                
                # Update hoặc Insert wages từ UI
                for name, value in wages:
                    if name in existing_wages:
                        # Tồn tại → UPDATE giá nếu khác
                        if float(existing_wages[name]['value']) != float(value):
                            cursor.execute(
                                "UPDATE WAGE SET WageValue = %s WHERE WageId = %s",
                                (value, existing_wages[name]['id'])
                            )
                    else:
                        # Chưa tồn tại → INSERT mới
                        cursor.execute(
                            "INSERT INTO WAGE (WageName, WageValue) VALUES (%s, %s)",
                            (name, value)
                        )
                
                # Xóa wages không còn trong UI và không được sử dụng
                for wage_name, wage_info in existing_wages.items():
                    if wage_name not in ui_wage_names:
                        wage_id = wage_info['id']
                        
                        # Kiểm tra có đang được dùng không
                        cursor.execute("SELECT COUNT(*) FROM REPAIR_DETAILS WHERE WageId = %s", (wage_id,))
                        if cursor.fetchone()[0] == 0:
                            cursor.execute("DELETE FROM WAGE WHERE WageId = %s", (wage_id,))
                
                cursor.close()
                conn.commit()
                logger.info("Successfully saved all settings")
                
        except Exception as e:
            logger.error(f"Error saving all settings: {e}")
            raise


# Singleton instance
_system_settings_service = None

def get_system_settings_service() -> SystemSettingsService:
    """
    Lấy singleton instance của SystemSettingsService.
    
    Returns:
        SystemSettingsService instance
    """
    global _system_settings_service
    if _system_settings_service is None:
        _system_settings_service = SystemSettingsService()
    return _system_settings_service
