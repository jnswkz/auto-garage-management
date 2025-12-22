# src/services/revenue_report_service.py
"""
Service for revenue report operations.
Handles generating and retrieving monthly revenue reports.
"""

import logging
from typing import Optional

from app.database import db_manager

logger = logging.getLogger(__name__)


class RevenueReportService:
    """Service for revenue report business logic."""

    def __init__(self):
        """Initialize the service."""
        pass

    def get_or_create_monthly_report(self, month: int, year: int) -> dict:
        """
        Get monthly revenue report. If not exists, generate it first.
        
        Args:
            month: Report month (1-12)
            year: Report year (e.g., 2025)
            
        Returns:
            dict with keys:
                - 'report_id': int
                - 'month': int
                - 'year': int
                - 'total_revenue': float
                - 'details': list of dict with keys:
                    - 'brand_name': str
                    - 'count': int (number of repairs)
                    - 'total_money': float
                    - 'rate': float (percentage)
        """
        try:
            # 1. Check if report already exists
            report_id = self._get_existing_report_id(month, year)
            
            if report_id is None:
                # 2. Generate new report using stored procedure
                logger.info(f"Generating new revenue report for {month}/{year}")
                report_id = self._generate_report(month, year)
            else:
                logger.info(f"Found existing revenue report (ID={report_id}) for {month}/{year}")
            
            # 3. Fetch report details
            return self._fetch_report_data(report_id)
            
        except Exception as e:
            logger.error(f"Error in get_or_create_monthly_report: {e}")
            raise

    def _get_existing_report_id(self, month: int, year: int) -> Optional[int]:
        """Check if report exists and return its ID."""
        try:
            with db_manager.get_cursor() as cursor:
                query = """
                    SELECT ReportId 
                    FROM REVENUE_REPORT 
                    WHERE ReportMonth = %s AND ReportYear = %s
                """
                cursor.execute(query, (month, year))
                result = cursor.fetchone()
                
                return result['ReportId'] if result else None
        except Exception as e:
            logger.error(f"Error checking existing report: {e}")
            raise

    def _generate_report(self, month: int, year: int) -> int:
        """
        Generate new revenue report using stored procedure.
        Calls sp_CreateRevenueReport which inserts into REVENUE_REPORT and REVENUE_REPORT_DETAILS.
        
        Returns:
            report_id: ID of newly created report
        """
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Call stored procedure using SQL statement
                cursor.execute("CALL sp_CreateRevenueReport(%s, %s, @report_id)", (month, year))
                
                # Fetch the OUT parameter
                cursor.execute("SELECT @report_id")
                result = cursor.fetchone()
                report_id = result[0] if result and result[0] is not None else None
                
                if report_id is None:
                    raise ValueError("Failed to get report ID from stored procedure")
                
                conn.commit()
                cursor.close()
                
                logger.info(f"Created revenue report (ID={report_id}) for {month}/{year}")
                
                return report_id
                
        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)
            raise

    def _fetch_report_data(self, report_id: int) -> dict:
        """Fetch complete report data including details."""
        try:
            with db_manager.get_cursor() as cursor:
                # Get main report info
                report_query = """
                    SELECT ReportId, ReportMonth, ReportYear, TotalRevenue
                    FROM REVENUE_REPORT
                    WHERE ReportId = %s
                """
                cursor.execute(report_query, (report_id,))
                report = cursor.fetchone()
                
                if not report:
                    raise ValueError(f"Report ID {report_id} not found")
                
                # Get details with brand names
                details_query = """
                    SELECT 
                        cb.BrandName,
                        rd.Count,
                        rd.TotalMoney,
                        rd.Rate
                    FROM REVENUE_REPORT_DETAILS rd
                    JOIN CAR_BRAND cb ON rd.BrandId = cb.BrandId
                    WHERE rd.ReportId = %s
                    ORDER BY rd.TotalMoney DESC
                """
                cursor.execute(details_query, (report_id,))
                details = cursor.fetchall()
                
                return {
                    'report_id': report['ReportId'],
                    'month': report['ReportMonth'],
                    'year': report['ReportYear'],
                    'total_revenue': float(report['TotalRevenue']),
                    'details': [
                        {
                            'brand_name': row['BrandName'],
                            'count': row['Count'],
                            'total_money': float(row['TotalMoney']),
                            'rate': float(row['Rate'])
                        }
                        for row in details
                    ]
                }
        except Exception as e:
            logger.error(f"Error fetching report data: {e}")
            raise

    def delete_report(self, month: int, year: int) -> bool:
        """
        Delete existing report for re-generation.
        Useful when data has been updated and report needs refresh.
        """
        try:
            with db_manager.transaction() as cursor:
                # Get report ID first
                cursor.execute(
                    "SELECT ReportId FROM REVENUE_REPORT WHERE ReportMonth = %s AND ReportYear = %s",
                    (month, year)
                )
                result = cursor.fetchone()
                
                if not result:
                    logger.info(f"No report found for {month}/{year} to delete")
                    return False
                
                report_id = result['ReportId']
                
                # Delete details first (foreign key constraint)
                cursor.execute("DELETE FROM REVENUE_REPORT_DETAILS WHERE ReportId = %s", (report_id,))
                
                # Delete main report
                cursor.execute("DELETE FROM REVENUE_REPORT WHERE ReportId = %s", (report_id,))
                
                logger.info(f"Deleted report (ID={report_id}) for {month}/{year}")
                
                return True
                
        except Exception as e:
            logger.error(f"Error deleting report: {e}")
            raise
