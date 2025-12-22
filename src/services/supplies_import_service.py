# src/services/supplies_import_service.py
"""
Business logic cho Nhập vật tư/phụ tùng.
Xử lý CRUD cho SUPPLIES_IMPORT và cập nhật tồn kho.
"""

from typing import List, Dict, Tuple
from datetime import date
import logging

from app.database import db_manager

logger = logging.getLogger(__name__)


class SuppliesImportService:
    """
    Service quản lý nhập vật tư:
    - Load danh sách vật tư từ SUPPLIES
    - Tạo phiếu nhập (insert SUPPLIES_IMPORT + update InventoryNumber)
    """
    
    def __init__(self):
        """Khởi tạo service."""
        pass
    
    # ==================== SUPPLIES ====================
    
    def get_all_supplies_for_import(self) -> List[Dict[str, any]]:
        """
        Lấy danh sách tất cả vật tư để hiển thị trong form nhập.
        
        Returns:
            List[{'id': int, 'name': str, 'price': float, 'stock': int}]
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT SuppliesId, SuppliesName, SuppliesPrice, InventoryNumber 
                    FROM SUPPLIES 
                    ORDER BY SuppliesName
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()
                
                return [{
                    'id': row[0],
                    'name': row[1],
                    'price': float(row[2]),
                    'stock': row[3]
                } for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting supplies for import: {e}")
            raise
    
    # ==================== IMPORT ====================
    
    def create_import_ticket(self, import_date: date, items: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Tạo phiếu nhập vật tư.
        
        Args:
            import_date: Ngày nhập
            items: List[{'supply_id': int, 'import_qty': int}]
            
        Returns:
            Dict {
                'total_items': int,
                'total_money': float,
                'imported_ids': List[int]  # List ImportId đã tạo
            }
            
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        if not items:
            raise ValueError("Danh sách nhập không được rỗng")
        
        # Validate items
        for item in items:
            if 'supply_id' not in item or 'import_qty' not in item:
                raise ValueError("Thiếu thông tin supply_id hoặc import_qty")
            if item['import_qty'] <= 0:
                raise ValueError(f"Số lượng nhập phải > 0 (SuppliesId={item['supply_id']})")
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                imported_ids = []
                total_money = 0.0
                
                for item in items:
                    supply_id = item['supply_id']
                    import_qty = item['import_qty']
                    
                    # 1. Lấy giá vật tư
                    cursor.execute(
                        "SELECT SuppliesPrice FROM SUPPLIES WHERE SuppliesId = %s",
                        (supply_id,)
                    )
                    result = cursor.fetchone()
                    if not result:
                        raise ValueError(f"Không tìm thấy vật tư ID {supply_id}")
                    
                    supply_price = float(result[0])
                    line_money = supply_price * import_qty
                    total_money += line_money
                    
                    # 2. Insert vào SUPPLIES_IMPORT
                    insert_query = """
                        INSERT INTO SUPPLIES_IMPORT (SuppliesId, ImportAmount, ImportDate)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_query, (supply_id, import_qty, import_date))
                    import_id = cursor.lastrowid
                    imported_ids.append(import_id)
                    
                    # 3. Cập nhật tồn kho trong SUPPLIES
                    update_query = """
                        UPDATE SUPPLIES 
                        SET InventoryNumber = InventoryNumber + %s
                        WHERE SuppliesId = %s
                    """
                    cursor.execute(update_query, (import_qty, supply_id))
                    
                    logger.info(f"Imported {import_qty} of SuppliesId={supply_id}, ImportId={import_id}")
                
                cursor.close()
                conn.commit()
                
                logger.info(f"Created import ticket: {len(items)} items, total: {total_money}")
                
                return {
                    'total_items': len(items),
                    'total_money': total_money,
                    'imported_ids': imported_ids
                }
                
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error creating import ticket: {e}")
            raise
    
    # ==================== History ====================
    
    def get_import_history(self, limit: int = 100) -> List[Dict[str, any]]:
        """
        Lấy lịch sử nhập vật tư.
        
        Args:
            limit: Số lượng bản ghi tối đa
            
        Returns:
            List[{
                'import_id': int,
                'supply_name': str,
                'import_qty': int,
                'import_date': date
            }]
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT 
                        si.ImportId,
                        s.SuppliesName,
                        si.ImportAmount,
                        si.ImportDate
                    FROM SUPPLIES_IMPORT si
                    JOIN SUPPLIES s ON si.SuppliesId = s.SuppliesId
                    ORDER BY si.ImportDate DESC, si.ImportId DESC
                    LIMIT %s
                """
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                cursor.close()
                
                return [{
                    'import_id': row[0],
                    'supply_name': row[1],
                    'import_qty': row[2],
                    'import_date': row[3]
                } for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting import history: {e}")
            raise


# Singleton instance
_supplies_import_service = None

def get_supplies_import_service() -> SuppliesImportService:
    """
    Lấy singleton instance của SuppliesImportService.
    
    Returns:
        SuppliesImportService instance
    """
    global _supplies_import_service
    if _supplies_import_service is None:
        _supplies_import_service = SuppliesImportService()
    return _supplies_import_service
