-- =====================================================
-- Stored Procedure: Tổng hợp báo cáo doanh thu tháng
-- Lưu vào REVENUE_REPORT và REVENUE_REPORT_DETAILS
-- =====================================================

USE GarageManagement;

DELIMITER //

-- Xóa procedure cũ nếu tồn tại
DROP PROCEDURE IF EXISTS sp_CreateRevenueReport //

-- Tạo stored procedure
CREATE PROCEDURE sp_CreateRevenueReport(
    IN p_month INT,           -- Tháng báo cáo (1-12)
    IN p_year INT,            -- Năm báo cáo
    OUT p_report_id INT       -- ID báo cáo được tạo (OUT parameter)
)
BEGIN
    DECLARE v_total_revenue DECIMAL(15, 2) DEFAULT 0;
    DECLARE v_existing_report_id INT DEFAULT NULL;
    
    -- 1. Kiểm tra xem báo cáo tháng này đã tồn tại chưa
    SELECT ReportId INTO v_existing_report_id
    FROM REVENUE_REPORT
    WHERE ReportMonth = p_month AND ReportYear = p_year
    LIMIT 1;
    
    -- 2. Nếu đã tồn tại -> Xóa báo cáo cũ để tạo lại
    IF v_existing_report_id IS NOT NULL THEN
        -- Xóa details trước (do FK constraint)
        DELETE FROM REVENUE_REPORT_DETAILS WHERE ReportId = v_existing_report_id;
        -- Xóa báo cáo chính
        DELETE FROM REVENUE_REPORT WHERE ReportId = v_existing_report_id;
    END IF;
    
    -- 3. Tính tổng doanh thu tháng từ bảng REPAIR
    SELECT COALESCE(SUM(r.RepairMoney), 0) INTO v_total_revenue
    FROM REPAIR r
    WHERE MONTH(r.RepairDate) = p_month 
      AND YEAR(r.RepairDate) = p_year;
    
    -- 4. Tạo record chính trong REVENUE_REPORT
    INSERT INTO REVENUE_REPORT (ReportMonth, ReportYear, TotalRevenue)
    VALUES (p_month, p_year, v_total_revenue);
    
    -- Lấy ID báo cáo vừa tạo
    SET p_report_id = LAST_INSERT_ID();
    
    -- 5. Tạo chi tiết theo từng hãng xe trong REVENUE_REPORT_DETAILS
    -- Join: REPAIR -> CAR_RECEPTION -> CAR -> CAR_BRAND
    -- Chỉ insert các hãng xe có dữ liệu sửa chữa trong tháng
    INSERT INTO REVENUE_REPORT_DETAILS (ReportId, BrandId, Count, TotalMoney, Rate)
    SELECT 
        p_report_id AS ReportId,
        cb.BrandId,
        COUNT(r.RepairId) AS Count,
        COALESCE(SUM(r.RepairMoney), 0) AS TotalMoney,
        CASE 
            WHEN v_total_revenue > 0 THEN 
                ROUND((COALESCE(SUM(r.RepairMoney), 0) / v_total_revenue) * 100, 2)
            ELSE 0 
        END AS Rate
    FROM REPAIR r
    INNER JOIN CAR_RECEPTION cr ON r.ReceptionId = cr.ReceptionId
    INNER JOIN CAR c ON cr.LicensePlate = c.LicensePlate
    INNER JOIN CAR_BRAND cb ON c.BrandId = cb.BrandId
    WHERE MONTH(r.RepairDate) = p_month 
      AND YEAR(r.RepairDate) = p_year
    GROUP BY cb.BrandId, cb.BrandName
    HAVING COUNT(r.RepairId) > 0
    ORDER BY TotalMoney DESC;
    
END //

DELIMITER ;

-- =====================================================
-- Cách sử dụng:
-- =====================================================
-- Tạo báo cáo tháng 12/2025:
--   CALL sp_CreateRevenueReport(12, 2025, @report_id);
--   SELECT @report_id AS 'Created Report ID';
--
-- Xem kết quả:
--   SELECT * FROM REVENUE_REPORT WHERE ReportId = @report_id;
--   SELECT rd.*, cb.BrandName 
--   FROM REVENUE_REPORT_DETAILS rd
--   JOIN CAR_BRAND cb ON rd.BrandId = cb.BrandId
--   WHERE rd.ReportId = @report_id
--   ORDER BY rd.TotalMoney DESC;
-- =====================================================
