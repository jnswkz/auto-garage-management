-- =====================================================
-- Stored Procedure: Báo cáo tồn kho tháng (BM5.2)
-- Xử lý D3 → D4 theo DFD
-- =====================================================

USE GarageManagement;

DELIMITER //

-- Xóa procedure cũ nếu tồn tại
DROP PROCEDURE IF EXISTS sp_CreateStockReport //

-- Tạo stored procedure
CREATE PROCEDURE sp_CreateStockReport(
    IN p_month INT,              -- D1: Tháng báo cáo (1-12)
    IN p_year INT,               -- D1: Năm báo cáo
    OUT p_report_id INT          -- ID báo cáo được tạo (OUT parameter)
)
BEGIN
    DECLARE v_existing_report_id INT DEFAULT NULL;
    DECLARE v_prev_month INT;
    DECLARE v_prev_year INT;
    
    -- ===============================================
    -- Tính tháng trước để lấy Tồn Đầu (từ D3)
    -- ===============================================
    IF p_month = 1 THEN
        SET v_prev_month = 12;
        SET v_prev_year = p_year - 1;
    ELSE
        SET v_prev_month = p_month - 1;
        SET v_prev_year = p_year;
    END IF;
    
    -- ===============================================
    -- 1. Kiểm tra báo cáo đã tồn tại → Xóa để tạo lại
    -- ===============================================
    SELECT StockReportId INTO v_existing_report_id
    FROM STOCK_REPORT
    WHERE ReportMonth = p_month AND ReportYear = p_year
    LIMIT 1;
    
    IF v_existing_report_id IS NOT NULL THEN
        DELETE FROM STOCK_REPORT_DETAILS WHERE StockReportId = v_existing_report_id;
        DELETE FROM STOCK_REPORT WHERE StockReportId = v_existing_report_id;
    END IF;
    
    -- ===============================================
    -- 2. Tạo record chính D4: STOCK_REPORT
    -- ===============================================
    INSERT INTO STOCK_REPORT (ReportMonth, ReportYear)
    VALUES (p_month, p_year);
    
    SET p_report_id = LAST_INSERT_ID();
    
    -- ===============================================
    -- 3. Tạo chi tiết D4: STOCK_REPORT_DETAILS
    -- Xử lý D3:
    --   - Danh mục Vật Tư (SUPPLIES)
    --   - Tồn Đầu: EndQty tháng trước từ STOCK_REPORT_DETAILS
    --   - Phát Sinh: SUM(SuppliesAmount) từ REPAIR_DETAILS
    --   - Tồn Cuối = Tồn Đầu - Phát Sinh
    -- ===============================================
    INSERT INTO STOCK_REPORT_DETAILS (StockReportId, SuppliesId, BeginQty, IssueQty, EndQty)
    SELECT 
        p_report_id AS StockReportId,
        s.SuppliesId,
        -- BeginQty (Tồn Đầu): Lấy từ Tồn Cuối tháng trước hoặc tính ngược từ inventory hiện tại
        COALESCE(
            (SELECT srd.EndQty 
             FROM STOCK_REPORT_DETAILS srd
             JOIN STOCK_REPORT sr ON srd.StockReportId = sr.StockReportId
             WHERE sr.ReportMonth = v_prev_month 
               AND sr.ReportYear = v_prev_year
               AND srd.SuppliesId = s.SuppliesId
             LIMIT 1),
            -- Nếu không có tháng trước: Tồn hiện tại + Phát sinh = Tồn Đầu
            s.InventoryNumber + COALESCE(issue.total_issued, 0)
        ) AS BeginQty,
        -- IssueQty (Phát Sinh): Tổng xuất kho trong tháng từ REPAIR_DETAILS
        COALESCE(issue.total_issued, 0) AS IssueQty,
        -- EndQty (Tồn Cuối): Tồn Đầu - Phát Sinh (không có nhập trong hệ thống)
        COALESCE(
            (SELECT srd.EndQty 
             FROM STOCK_REPORT_DETAILS srd
             JOIN STOCK_REPORT sr ON srd.StockReportId = sr.StockReportId
             WHERE sr.ReportMonth = v_prev_month 
               AND sr.ReportYear = v_prev_year
               AND srd.SuppliesId = s.SuppliesId
             LIMIT 1),
            s.InventoryNumber + COALESCE(issue.total_issued, 0)
        ) - COALESCE(issue.total_issued, 0) AS EndQty
    FROM SUPPLIES s
    LEFT JOIN (
        -- D3: Tính Phát Sinh từ Chi tiết Phiếu Sửa Chữa trong tháng
        SELECT 
            rd.SuppliesId,
            SUM(rd.SuppliesAmount) AS total_issued
        FROM REPAIR_DETAILS rd
        JOIN REPAIR r ON rd.RepairId = r.RepairId
        WHERE MONTH(r.RepairDate) = p_month 
          AND YEAR(r.RepairDate) = p_year
        GROUP BY rd.SuppliesId
    ) issue ON s.SuppliesId = issue.SuppliesId;
    
END //

DELIMITER ;

-- =====================================================
-- Cách sử dụng (Test D1 → D4):
-- =====================================================
-- Tạo báo cáo tồn kho tháng 12/2025:
--   CALL sp_CreateStockReport(12, 2025, @report_id);
--   SELECT @report_id AS 'Created Report ID';
--
-- Xem kết quả D4:
--   SELECT * FROM STOCK_REPORT WHERE StockReportId = @report_id;
--   SELECT srd.*, s.SuppliesName 
--   FROM STOCK_REPORT_DETAILS srd
--   JOIN SUPPLIES s ON srd.SuppliesId = s.SuppliesId
--   WHERE srd.StockReportId = @report_id
--   ORDER BY s.SuppliesName;
-- =====================================================
