# src/services/receipt_service.py
"""
Service layer for receipt (payment collection) operations.
Handles business logic for creating payment receipts and managing debt.
"""

from typing import Optional, Dict, Any, List
import logging
from mysql.connector import Error

from app.database import db_manager

logger = logging.getLogger(__name__)


class ReceiptService:
    """Service class for handling payment receipt operations."""
    
    @staticmethod
    def get_vehicle_debt_info(license_plate: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin xe và tổng nợ theo biển số.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            Dictionary with vehicle info and total debt, or None if not found
        """
        try:
            query = """
                SELECT 
                    c.LicensePlate,
                    c.OwnerName,
                    c.PhoneNumber,
                    c.Address,
                    c.Email,
                    b.BrandName,
                    COALESCE(SUM(cr.Debt), 0) as TotalDebt
                FROM CAR c
                JOIN CAR_BRAND b ON c.BrandId = b.BrandId
                LEFT JOIN CAR_RECEPTION cr ON c.LicensePlate = cr.LicensePlate
                WHERE c.LicensePlate = %s
                GROUP BY c.LicensePlate, c.OwnerName, c.PhoneNumber, 
                         c.Address, c.Email, b.BrandName
            """
            result = db_manager.execute_query(query, params=(license_plate,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get vehicle debt info for {license_plate}: {e}")
            return None
    
    @staticmethod
    def get_latest_reception_with_debt(license_plate: str) -> Optional[Dict[str, Any]]:
        """
        Lấy phiếu tiếp nhận mới nhất có nợ của xe.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            Reception information with debt > 0, or None
        """
        try:
            query = """
                SELECT ReceptionId, LicensePlate, ReceptionDate, Debt
                FROM CAR_RECEPTION
                WHERE LicensePlate = %s AND Debt > 0
                ORDER BY ReceptionDate DESC, ReceptionId DESC
                LIMIT 1
            """
            result = db_manager.execute_query(query, params=(license_plate,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get latest reception with debt for {license_plate}: {e}")
            return None
    
    @staticmethod
    def get_all_receptions_with_debt(license_plate: str) -> List[Dict[str, Any]]:
        """
        Lấy tất cả phiếu tiếp nhận có nợ của xe.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            List of reception dictionaries with debt > 0
        """
        try:
            query = """
                SELECT ReceptionId, LicensePlate, ReceptionDate, Debt
                FROM CAR_RECEPTION
                WHERE LicensePlate = %s AND Debt > 0
                ORDER BY ReceptionDate DESC, ReceptionId DESC
            """
            receptions = db_manager.execute_query(query, params=(license_plate,), fetch_all=True)
            return receptions or []
        except Error as e:
            logger.error(f"Failed to get receptions with debt for {license_plate}: {e}")
            return []
    
    @staticmethod
    def check_payment_allowed(payment_amount: float, total_debt: float) -> Dict[str, Any]:
        """
        Kiểm tra xem có cho phép thu tiền quá nợ không (theo quy định IsOverPay).
        
        Args:
            payment_amount: Số tiền thu
            total_debt: Tổng nợ hiện tại
            
        Returns:
            Dictionary with allowed status and message
        """
        try:
            # Lấy quy định IsOverPay từ bảng PARAMETER
            query = "SELECT value FROM PARAMETER WHERE name = 'IsOverPay'"
            result = db_manager.execute_query(query, fetch_one=True)
            is_over_pay = result['value'] if result else 0
            
            if is_over_pay == 0 and payment_amount > total_debt:
                return {
                    'allowed': False,
                    'message': f"Số tiền thu ({payment_amount:,.0f}) vượt quá số tiền nợ ({total_debt:,.0f}). "
                              "Quy định không cho phép thu quá nợ."
                }
            
            return {
                'allowed': True,
                'message': 'Được phép thu tiền'
            }
        except Error as e:
            logger.error(f"Failed to check payment allowed: {e}")
            # Default to not allowing overpayment
            return {
                'allowed': payment_amount <= total_debt,
                'message': 'Lỗi khi kiểm tra quy định' if payment_amount > total_debt else 'OK'
            }
    
    @staticmethod
    def create_receipt(
        reception_id: int,
        receipt_date: str,
        money_amount: float
    ) -> Dict[str, Any]:
        """
        Tạo phiếu thu tiền mới.
        
        Args:
            reception_id: ID phiếu tiếp nhận (để thu nợ)
            receipt_date: Ngày thu tiền (format: YYYY-MM-DD)
            money_amount: Số tiền thu
            
        Returns:
            Dictionary with success status, receipt_id, and message
        """
        try:
            with db_manager.transaction() as cursor:
                # 1. Kiểm tra phiếu tiếp nhận có tồn tại và có nợ không
                cursor.execute("""
                    SELECT ReceptionId, LicensePlate, Debt
                    FROM CAR_RECEPTION
                    WHERE ReceptionId = %s
                """, (reception_id,))
                
                reception = cursor.fetchone()
                if not reception:
                    return {
                        'success': False,
                        'message': f"Không tìm thấy phiếu tiếp nhận ID {reception_id}"
                    }
                
                current_debt = float(reception['Debt'])
                if current_debt <= 0:
                    return {
                        'success': False,
                        'message': "Phiếu tiếp nhận này không còn nợ"
                    }
                
                # 2. Kiểm tra quy định IsOverPay
                cursor.execute("SELECT value FROM PARAMETER WHERE name = 'IsOverPay'")
                param_result = cursor.fetchone()
                is_over_pay = param_result['value'] if param_result else 0
                
                if is_over_pay == 0 and money_amount > current_debt:
                    return {
                        'success': False,
                        'message': f"Số tiền thu ({money_amount:,.0f}) vượt quá số tiền nợ ({current_debt:,.0f}). "
                                  "Quy định không cho phép thu quá nợ."
                    }
                
                # 3. Tạo phiếu thu (trigger sẽ tự động cập nhật Debt trong CAR_RECEPTION)
                cursor.execute("""
                    INSERT INTO RECEIPT (ReceptionId, ReceiptDate, MoneyAmount)
                    VALUES (%s, %s, %s)
                """, (reception_id, receipt_date, money_amount))
                
                receipt_id = cursor.lastrowid
                
                # 4. Lấy số nợ còn lại sau khi thu (trigger đã cập nhật)
                cursor.execute("""
                    SELECT Debt FROM CAR_RECEPTION WHERE ReceptionId = %s
                """, (reception_id,))
                updated_reception = cursor.fetchone()
                remaining_debt = float(updated_reception['Debt']) if updated_reception else 0
                
                logger.info(
                    f"Successfully created receipt {receipt_id} "
                    f"for reception {reception_id}, amount: {money_amount}"
                )
                
                return {
                    'success': True,
                    'receipt_id': receipt_id,
                    'message': 'Tạo phiếu thu thành công',
                    'remaining_debt': remaining_debt,
                    'license_plate': reception['LicensePlate']
                }
                
        except Error as e:
            logger.error(f"Failed to create receipt: {e}")
            # Check if it's the trigger error about overpayment
            error_message = str(e)
            if "45000" in error_message or "vượt quá số tiền" in error_message:
                return {
                    'success': False,
                    'message': "Số tiền thu vượt quá số tiền nợ (bị trigger từ chối)"
                }
            return {
                'success': False,
                'message': f"Lỗi khi tạo phiếu thu: {error_message}"
            }
        except Exception as e:
            logger.error(f"Unexpected error when creating receipt: {e}")
            return {
                'success': False,
                'message': f"Lỗi không xác định: {str(e)}"
            }
    
    @staticmethod
    def get_receipt_by_id(receipt_id: int) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin phiếu thu theo ID.
        
        Args:
            receipt_id: ID phiếu thu
            
        Returns:
            Receipt information dictionary or None
        """
        try:
            query = """
                SELECT 
                    r.ReceiptId, r.ReceptionId, r.ReceiptDate, r.MoneyAmount,
                    cr.LicensePlate, cr.ReceptionDate,
                    c.OwnerName, c.PhoneNumber
                FROM RECEIPT r
                JOIN CAR_RECEPTION cr ON r.ReceptionId = cr.ReceptionId
                JOIN CAR c ON cr.LicensePlate = c.LicensePlate
                WHERE r.ReceiptId = %s
            """
            result = db_manager.execute_query(query, params=(receipt_id,), fetch_one=True)
            return result
        except Error as e:
            logger.error(f"Failed to get receipt info for ID {receipt_id}: {e}")
            return None
    
    @staticmethod
    def get_receipts_by_license_plate(license_plate: str) -> List[Dict[str, Any]]:
        """
        Lấy lịch sử phiếu thu của xe theo biển số.
        
        Args:
            license_plate: Biển số xe
            
        Returns:
            List of receipt dictionaries
        """
        try:
            query = """
                SELECT 
                    r.ReceiptId, r.ReceiptDate, r.MoneyAmount,
                    r.ReceptionId, cr.ReceptionDate
                FROM RECEIPT r
                JOIN CAR_RECEPTION cr ON r.ReceptionId = cr.ReceptionId
                WHERE cr.LicensePlate = %s
                ORDER BY r.ReceiptDate DESC, r.ReceiptId DESC
            """
            receipts = db_manager.execute_query(query, params=(license_plate,), fetch_all=True)
            return receipts or []
        except Error as e:
            logger.error(f"Failed to get receipt history for {license_plate}: {e}")
            return []
    
    @staticmethod
    def get_all_receipts_by_date_range(
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách phiếu thu trong khoảng thời gian.
        
        Args:
            start_date: Ngày bắt đầu (format: YYYY-MM-DD)
            end_date: Ngày kết thúc (format: YYYY-MM-DD)
            
        Returns:
            List of receipt dictionaries
        """
        try:
            query = """
                SELECT 
                    r.ReceiptId, r.ReceiptDate, r.MoneyAmount,
                    cr.LicensePlate, c.OwnerName
                FROM RECEIPT r
                JOIN CAR_RECEPTION cr ON r.ReceptionId = cr.ReceptionId
                JOIN CAR c ON cr.LicensePlate = c.LicensePlate
                WHERE r.ReceiptDate BETWEEN %s AND %s
                ORDER BY r.ReceiptDate DESC, r.ReceiptId DESC
            """
            receipts = db_manager.execute_query(
                query,
                params=(start_date, end_date),
                fetch_all=True
            )
            return receipts or []
        except Error as e:
            logger.error(f"Failed to get receipts by date range: {e}")
            return []
