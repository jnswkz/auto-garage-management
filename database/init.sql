-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: garagemanagement
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `car`
--
CREATE DATABASE IF NOT EXISTS `garagemanagement` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `garagemanagement`;

-- Drop tables in correct dependency order
DROP TABLE IF EXISTS `repair_details`;
DROP TABLE IF EXISTS `repair`;
DROP TABLE IF EXISTS `receipt`;
DROP TABLE IF EXISTS `car_reception`;
DROP TABLE IF EXISTS `car`;
DROP TABLE IF EXISTS `car_brand`;
DROP TABLE IF EXISTS `parameter`;
DROP TABLE IF EXISTS `revenue_report_details`;
DROP TABLE IF EXISTS `revenue_report`;
DROP TABLE IF EXISTS `stock_report_details`;
DROP TABLE IF EXISTS `stock_report`;
DROP TABLE IF EXISTS `supplies`;
DROP TABLE IF EXISTS `wage`;

-- Create tables in correct dependency order
CREATE TABLE `car_brand` (
  `BrandId` int NOT NULL AUTO_INCREMENT COMMENT 'Brand ID (Auto-increment)',
  `BrandName` varchar(255) NOT NULL COMMENT 'Brand Name',
  PRIMARY KEY (`BrandId`),
  UNIQUE KEY `BrandName` (`BrandName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `car` (
  `LicensePlate` varchar(255) NOT NULL COMMENT 'License Plate (Primary Key)',
  `BrandId` int NOT NULL COMMENT 'Brand ID (Foreign Key)',
  `OwnerName` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'Car Owner Name',
  `PhoneNumber` varchar(20) DEFAULT NULL COMMENT 'Phone Number',
  `Address` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'Address',
  `Email` varchar(255) DEFAULT NULL COMMENT 'Owner Email',
  PRIMARY KEY (`LicensePlate`),
  KEY `BrandId` (`BrandId`),
  CONSTRAINT `car_ibfk_1` FOREIGN KEY (`BrandId`) REFERENCES `car_brand` (`BrandId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `car_reception` (
  `ReceptionId` int NOT NULL AUTO_INCREMENT COMMENT 'Reception ID (Auto-increment)',
  `LicensePlate` varchar(255) NOT NULL COMMENT 'License Plate (Foreign Key)',
  `ReceptionDate` date NOT NULL COMMENT 'Date of reception',
  `Debt` decimal(15,2) DEFAULT '0.00' COMMENT 'Total debt at the time of reception',
  PRIMARY KEY (`ReceptionId`),
  KEY `LicensePlate` (`LicensePlate`),
  CONSTRAINT `car_reception_ibfk_1` FOREIGN KEY (`LicensePlate`) REFERENCES `car` (`LicensePlate`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `parameter` (
  `name` varchar(50) NOT NULL,
  `value` int DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `receipt` (
  `ReceiptId` int NOT NULL AUTO_INCREMENT COMMENT 'Receipt ID (Auto-increment)',
  `ReceptionId` int NOT NULL COMMENT 'Reception ID (Foreign Key)',
  `ReceiptDate` date NOT NULL COMMENT 'Payment Date',
  `MoneyAmount` decimal(15,2) NOT NULL COMMENT 'Amount Received',
  PRIMARY KEY (`ReceiptId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `repair` (
  `RepairId` int NOT NULL AUTO_INCREMENT COMMENT 'Repair Ticket ID (Auto-increment)',
  `ReceptionId` int NOT NULL COMMENT 'Reception ID (Foreign Key)',
  `RepairDate` date NOT NULL COMMENT 'Repair Date',
  `RepairMoney` decimal(15,2) DEFAULT '0.00' COMMENT 'Total Repair Cost',
  PRIMARY KEY (`RepairId`),
  KEY `ReceptionId` (`ReceptionId`),
  CONSTRAINT `repair_ibfk_1` FOREIGN KEY (`ReceptionId`) REFERENCES `car_reception` (`ReceptionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `supplies` (
  `SuppliesId` int NOT NULL AUTO_INCREMENT COMMENT 'Supply ID (Auto-increment)',
  `SuppliesName` varchar(255) NOT NULL COMMENT 'Supply Name',
  `SuppliesPrice` decimal(15,2) NOT NULL DEFAULT '0.00' COMMENT 'Unit Price',
  `InventoryNumber` int DEFAULT '0' COMMENT 'Inventory Quantity',
  PRIMARY KEY (`SuppliesId`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `wage` (
  `WageId` int NOT NULL AUTO_INCREMENT COMMENT 'Wage ID (Auto-increment)',
  `WageName` varchar(255) NOT NULL COMMENT 'Wage/Service Name',
  `WageValue` decimal(15,2) NOT NULL DEFAULT '0.00' COMMENT 'Wage Value / Service Fee',
  PRIMARY KEY (`WageId`),
  UNIQUE KEY `WageName` (`WageName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `repair_details` (
  `RepairDetailId` int NOT NULL AUTO_INCREMENT COMMENT 'Detail ID (Auto-increment)',
  `RepairId` int NOT NULL COMMENT 'Repair Ticket ID (Foreign Key)',
  `Content` varchar(255) DEFAULT NULL COMMENT 'Repair Content / Description',
  `SuppliesId` int NOT NULL COMMENT 'Supply ID (Foreign Key)',
  `SuppliesAmount` int NOT NULL DEFAULT '1' COMMENT 'Quantity of supplies used',
  `WageId` int DEFAULT NULL COMMENT 'Wage ID (Foreign Key)',
  PRIMARY KEY (`RepairDetailId`),
  KEY `RepairId` (`RepairId`),
  KEY `SuppliesId` (`SuppliesId`),
  KEY `WageId` (`WageId`),
  CONSTRAINT `repair_details_ibfk_1` FOREIGN KEY (`RepairId`) REFERENCES `repair` (`RepairId`),
  CONSTRAINT `repair_details_ibfk_2` FOREIGN KEY (`SuppliesId`) REFERENCES `supplies` (`SuppliesId`),
  CONSTRAINT `repair_details_ibfk_3` FOREIGN KEY (`WageId`) REFERENCES `wage` (`WageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `revenue_report` (
  `ReportId` int NOT NULL AUTO_INCREMENT COMMENT 'Report ID',
  `ReportMonth` int NOT NULL COMMENT 'Report Month',
  `ReportYear` int NOT NULL COMMENT 'Report Year',
  `TotalRevenue` decimal(15,2) DEFAULT '0.00' COMMENT 'Total Revenue',
  PRIMARY KEY (`ReportId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `revenue_report_details` (
  `ReportDetailId` int NOT NULL AUTO_INCREMENT,
  `ReportId` int NOT NULL COMMENT 'Report ID (Foreign Key)',
  `BrandId` int NOT NULL COMMENT 'Brand ID (Foreign Key)',
  `Count` int DEFAULT '0' COMMENT 'Number of repairs',
  `TotalMoney` decimal(15,2) DEFAULT '0.00' COMMENT 'Total Amount',
  `Rate` float DEFAULT '0' COMMENT 'Ratio / Percentage',
  PRIMARY KEY (`ReportDetailId`),
  KEY `ReportId` (`ReportId`),
  KEY `BrandId` (`BrandId`),
  CONSTRAINT `revenue_report_details_ibfk_1` FOREIGN KEY (`ReportId`) REFERENCES `revenue_report` (`ReportId`),
  CONSTRAINT `revenue_report_details_ibfk_2` FOREIGN KEY (`BrandId`) REFERENCES `car_brand` (`BrandId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stock_report` (
  `StockReportId` int NOT NULL AUTO_INCREMENT COMMENT 'Stock Report ID',
  `ReportMonth` int NOT NULL COMMENT 'Report Month',
  `ReportYear` int NOT NULL COMMENT 'Report Year',
  PRIMARY KEY (`StockReportId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stock_report_details` (
  `StockDetailId` int NOT NULL AUTO_INCREMENT,
  `StockReportId` int NOT NULL COMMENT 'Stock Report ID (Foreign Key)',
  `SuppliesId` int NOT NULL COMMENT 'Supply ID (Foreign Key)',
  `BeginQty` int DEFAULT '0' COMMENT 'Beginning Inventory',
  `IssueQty` int DEFAULT '0' COMMENT 'Incurred Quantity (Import/Export)',
  `EndQty` int DEFAULT '0' COMMENT 'Ending Inventory',
  PRIMARY KEY (`StockDetailId`),
  KEY `StockReportId` (`StockReportId`),
  KEY `SuppliesId` (`SuppliesId`),
  CONSTRAINT `stock_report_details_ibfk_1` FOREIGN KEY (`StockReportId`) REFERENCES `stock_report` (`StockReportId`),
  CONSTRAINT `stock_report_details_ibfk_2` FOREIGN KEY (`SuppliesId`) REFERENCES `supplies` (`SuppliesId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE SUPPLIES_IMPORT (
    ImportId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Import Transaction ID (Auto-increment)',
    SuppliesId INTEGER NOT NULL COMMENT 'Supply ID (Foreign Key)',
    ImportAmount INTEGER NOT NULL COMMENT 'Quantity Imported',
    ImportDate DATE NOT NULL COMMENT 'Import Date',
    FOREIGN KEY (SuppliesId) REFERENCES SUPPLIES(SuppliesId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DELIMITER //
DROP TRIGGER IF EXISTS trg_CheckMaxCarReception //
CREATE TRIGGER trg_CheckMaxCarReception
BEFORE INSERT ON CAR_RECEPTION
FOR EACH ROW
BEGIN
    DECLARE max_cars INT;
    DECLARE current_cars INT;

    -- 1. Lấy giá trị từ bảng PARAMETER của bạn (cột name, value)
    SELECT value INTO max_cars
    FROM PARAMETER 
    WHERE name = 'MaxCarReception';

    -- 2. Đếm số xe đã tiếp nhận trong ngày
    SELECT COUNT(*) INTO current_cars
    FROM CAR_RECEPTION
    WHERE ReceptionDate = NEW.ReceptionDate;

    -- 3. Kiểm tra: Nếu số xe hiện tại >= giới hạn thì báo lỗi
    IF current_cars >= max_cars THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Lỗi: Số lượng xe tiếp nhận trong ngày đã vượt quá quy định (MaxCarReception).';
    END IF;
END //
DELIMITER ;
DELIMITER //

DROP TRIGGER IF EXISTS trg_CheckPaymentLimit //

CREATE TRIGGER trg_CheckPaymentLimit
BEFORE INSERT ON RECEIPT
FOR EACH ROW
BEGIN
    DECLARE current_debt DECIMAL(15, 2);
    DECLARE is_over_pay INT;
    -- 1. Lấy quy định IsOverPay từ bảng PARAMETER
    SELECT value INTO is_over_pay
    FROM PARAMETER 
    WHERE name = 'IsOverPay';
    -- 2. Lấy số nợ hiện tại của xe
    SELECT Debt INTO current_debt
    FROM CAR_RECEPTION
    WHERE ReceptionId = NEW.ReceptionId;
    -- 3. Kiểm tra logic
    -- Nếu không cho phép thu quá (is_over_pay = 0) VÀ Tiền thu (MoneyAmount) > Nợ (Debt)
    IF (is_over_pay = 0) AND (NEW.MoneyAmount > current_debt) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Lỗi: Số tiền thu vượt quá số tiền khách đang nợ.';
    END IF;
END //
DELIMITER ;
DELIMITER //
DROP TRIGGER IF EXISTS trg_UpdateDebtAfterReceipt //
CREATE TRIGGER trg_UpdateDebtAfterReceipt
AFTER INSERT ON RECEIPT
FOR EACH ROW
BEGIN
    -- Trừ số tiền nợ trong bảng tiếp nhận tương ứng với số tiền vừa thu
    UPDATE CAR_RECEPTION
    SET Debt = Debt - NEW.MoneyAmount
    WHERE ReceptionId = NEW.ReceptionId;
END //
DELIMITER ;

--
-- Insert data after all table and trigger definitions
--

LOCK TABLES `car_brand` WRITE;
/*!40000 ALTER TABLE `car_brand` DISABLE KEYS */;
INSERT INTO `car_brand` VALUES (5,'Ford'),(2,'Honda'),(3,'Hyundai'),(4,'Kia'),(6,'Mazda'),(1,'Toyota');
/*!40000 ALTER TABLE `car_brand` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES ('30F-111.22',4,'Phạm Minh Dũng','0905111222','Hoàn Kiếm, Hà Nội','dung.pham@email.com'),('51A',5,'AAAA','9237287355','aaa',NULL),('51H-987.65',2,'Trần Thị Bích','0912345678','45 Nguyễn Trãi, Q5, TP.HCM','bich.tran@email.com'),('59A-123.45',1,'Nguyễn Văn An','0909123456','123 Lê Lợi, Q1, TP.HCM','an.nguyen@email.com'),('59K-234.56',1,'Võ Thị Em','0933444555','Thủ Đức, TP.HCM','em.vo@email.com'),('60C-555.88',3,'Lê Hoàng Cường','0988777666','Biên Hòa, Đồng Nai','cuong.le@email.com'),('62A-616.36',5,'Võ Thành Đạt','0369472671','Địa ngọc',NULL);
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `car_reception` WRITE;
/*!40000 ALTER TABLE `car_reception` DISABLE KEYS */;
INSERT INTO `car_reception` VALUES (1,'59A-123.45','2025-12-22',0.00),(2,'51H-987.65','2025-12-22',500000.00),(3,'60C-555.88','2025-12-22',0.00),(4,'59K-234.56','2025-12-21',1200000.00),(5,'62A-616.36','2025-12-22',0.00),(6,'51A','2025-12-22',0.00);
/*!40000 ALTER TABLE `car_reception` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `parameter` WRITE;
/*!40000 ALTER TABLE `parameter` DISABLE KEYS */;
INSERT INTO `parameter` VALUES ('IsOverPay',0),('MaxCarReception',30);
/*!40000 ALTER TABLE `parameter` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `supplies` WRITE;
/*!40000 ALTER TABLE `supplies` DISABLE KEYS */;
INSERT INTO `supplies` VALUES (1,'Gương chiếu hậu Toyota',1500000.00,20),(2,'Bộ thắng đĩa',450000.00,50),(3,'Nhớt Castrol 4L',550000.00,100),(4,'Lọc gió điều hòa',250000.00,30),(5,'Bugi Denso',120000.00,60),(6,'Gạt mưa Bosch',300000.00,40);
/*!40000 ALTER TABLE `supplies` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `wage` WRITE;
/*!40000 ALTER TABLE `wage` DISABLE KEYS */;
INSERT INTO `wage` VALUES (1,'Thay nhớt máy',50000.00),(2,'Rửa xe bọt tuyết',70000.00),(3,'Vệ sinh khoang máy',300000.00),(4,'Thay má phanh',150000.00),(5,'Kiểm tra tổng quát',100000.00),(6,'Sơn dặm vá',500000.00);
/*!40000 ALTER TABLE `wage` ENABLE KEYS */;
UNLOCK TABLES;

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