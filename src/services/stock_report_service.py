# src/services/stock_report_service.py
"""
Business logic cho Báo cáo Tồn kho (BM5.2).
Xử lý luồng dữ liệu D1→D3→D4→D6 theo DFD.
"""

from typing import Optional, Dict, List, Any
from datetime import datetime
import logging

from app.database import db_manager

logger = logging.getLogger(__name__)


class StockReportService:
    """
    Service xử lý báo cáo tồn kho tháng.
    
    Luồng DFD:
    - D1: Nhận input (tháng, năm) từ Người dùng
    - D3: Lấy dữ liệu từ Bộ nhớ phụ (SUPPLIES, STOCK_REPORT_DETAILS tháng trước, REPAIR_DETAILS)
    - D4: Xử lý và lưu vào STOCK_REPORT + STOCK_REPORT_DETAILS
    - D6: Trả kết quả về Người dùng (màn hình)
    """
    
    def __init__(self):
        """Khởi tạo service."""
        pass
    
    def get_or_create_monthly_report(self, month: int, year: int) -> Dict[str, Any]:
        """
        Lấy hoặc tạo báo cáo tồn kho tháng.
        Xử lý D1 → D6.
        
        Args:
            month: Tháng báo cáo (1-12) - từ D1
            year: Năm báo cáo - từ D1
            
        Returns:
            Dict chứa:
                - report_id: ID báo cáo
                - month: Tháng
                - year: Năm
                - items: List các dòng báo cáo [supply_name, begin_qty, issue_qty, end_qty]
                
        Raises:
            ValueError: Nếu tháng/năm không hợp lệ
            Exception: Lỗi database
        """
        # Validate D1
        if not (1 <= month <= 12):
            raise ValueError(f"Tháng không hợp lệ: {month}")
        if year < 1900 or year > 2100:
            raise ValueError(f"Năm không hợp lệ: {year}")
        
        logger.info(f"Processing stock report for {month}/{year}")
        
        # Kiểm tra báo cáo đã tồn tại (D3)
        existing_id = self._get_existing_report_id(month, year)
        
        if existing_id:
            logger.info(f"Report exists with ID: {existing_id}")
            report_id = existing_id
        else:
            # Tạo báo cáo mới: D3 → D4
            logger.info("Generating new stock report...")
            report_id = self._generate_report(month, year)
            logger.info(f"Report created with ID: {report_id}")
        
        # Lấy dữ liệu chi tiết để trả về D6
        report_data = self._fetch_report_data(report_id, month, year)
        
        return report_data
    
    def _get_existing_report_id(self, month: int, year: int) -> Optional[int]:
        """
        Kiểm tra báo cáo đã tồn tại chưa (D3).
        
        Returns:
            ID báo cáo nếu tồn tại, None nếu chưa có
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT StockReportId 
                    FROM STOCK_REPORT
                    WHERE ReportMonth = %s AND ReportYear = %s
                    LIMIT 1
                """
                cursor.execute(query, (month, year))
                result = cursor.fetchone()
                cursor.close()
                
                return result[0] if result else None
                
        except Exception as e:
            logger.error(f"Error checking existing report: {e}")
            raise
    
    def _generate_report(self, month: int, year: int) -> int:
        """
        Tạo báo cáo mới bằng stored procedure.
        Xử lý D3 → D4 (lưu vào database).
        
        Returns:
            ID báo cáo được tạo
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Gọi stored procedure với OUT parameter
                # D3 → D4: Procedure xử lý toàn bộ logic tính toán và lưu trữ
                cursor.execute("CALL sp_CreateStockReport(%s, %s, @report_id)", (month, year))
                
                # Lấy OUT parameter
                cursor.execute("SELECT @report_id")
                result = cursor.fetchone()
                
                if not result or result[0] is None:
                    raise Exception("Failed to create stock report")
                
                report_id = result[0]
                cursor.close()
                conn.commit()
                
                return report_id
                
        except Exception as e:
            logger.error(f"Error generating stock report: {e}")
            raise
    
    def _fetch_report_data(self, report_id: int, month: int, year: int) -> Dict[str, Any]:
        """
        Lấy dữ liệu báo cáo chi tiết để hiển thị (D6).
        
        Returns:
            Dict chứa thông tin báo cáo đầy đủ
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Lấy chi tiết báo cáo với tên vật tư
                query = """
                    SELECT 
                        s.SuppliesName,
                        srd.BeginQty,
                        srd.IssueQty,
                        srd.EndQty
                    FROM STOCK_REPORT_DETAILS srd
                    JOIN SUPPLIES s ON srd.SuppliesId = s.SuppliesId
                    WHERE srd.StockReportId = %s
                    ORDER BY s.SuppliesName
                """
                cursor.execute(query, (report_id,))
                rows = cursor.fetchall()
                cursor.close()
                
                # Format dữ liệu cho D6 (màn hình)
                items = []
                for row in rows:
                    items.append({
                        'supply_name': row[0],
                        'begin_qty': row[1],
                        'issue_qty': row[2],
                        'end_qty': row[3]
                    })
                
                return {
                    'report_id': report_id,
                    'month': month,
                    'year': year,
                    'items': items
                }
                
        except Exception as e:
            logger.error(f"Error fetching report data: {e}")
            raise


# Singleton instance
_stock_report_service = None

def get_stock_report_service() -> StockReportService:
    """
    Lấy singleton instance của StockReportService.
    
    Returns:
        StockReportService instance
    """
    global _stock_report_service
    if _stock_report_service is None:
        _stock_report_service = StockReportService()
    return _stock_report_service
