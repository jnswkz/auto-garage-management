-- Create database
CREATE DATABASE IF NOT EXISTS GarageManagement;
USE GarageManagement;

-- 1. Table CAR_BRAND
-- Stores the list of car brands
CREATE TABLE CAR_BRAND (
    BrandId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Brand ID (Auto-increment)',
    BrandName VARCHAR(255) NOT NULL UNIQUE COMMENT 'Brand Name'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Table CAR
-- Stores customer car information
CREATE TABLE CAR (
    LicensePlate VARCHAR(255) PRIMARY KEY COMMENT 'License Plate (Primary Key)',
    BrandId INTEGER NOT NULL COMMENT 'Brand ID (Foreign Key)',
    OwnerName NVARCHAR(255) NOT NULL COMMENT 'Car Owner Name',
    PhoneNumber VARCHAR(20) COMMENT 'Phone Number',
    Address NVARCHAR(255) COMMENT 'Address',
    Email VARCHAR(255) COMMENT 'Owner Email',
    FOREIGN KEY (BrandId) REFERENCES CAR_BRAND(BrandId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- 3. Table CAR_RECEPTION
-- Stores information about car reception instances at the garage
CREATE TABLE CAR_RECEPTION (
    ReceptionId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Reception ID (Auto-increment)',
    LicensePlate VARCHAR(255) NOT NULL COMMENT 'License Plate (Foreign Key)',
    ReceptionDate DATE NOT NULL COMMENT 'Date of reception',
    Debt NUMERIC(15, 2) DEFAULT 0 COMMENT 'Total debt at the time of reception',
    FOREIGN KEY (LicensePlate) REFERENCES CAR(LicensePlate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Table PARAMETER
-- Stores configurable regulations (max cars, payment rules...)
CREATE TABLE PARAMETER (
	name VARCHAR(50) PRIMARY KEY,
    value INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO PARAMETER VALUES ('MaxCarReception', 30);
INSERT INTO PARAMETER VALUES ('IsOverPay', 0);
-- 5. Table SUPPLIES
-- Stores the list of supplies/parts and their unit prices
CREATE TABLE SUPPLIES (
    SuppliesId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Supply ID (Auto-increment)',
    SuppliesName VARCHAR(255) NOT NULL COMMENT 'Supply Name',
    SuppliesPrice NUMERIC(15, 2) NOT NULL DEFAULT 0 COMMENT 'Unit Price',
    InventoryNumber INTEGER DEFAULT 0 COMMENT 'Inventory Quantity'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5.1. Table SUPPLIES_IMPORT
-- Stores supply import transactions
CREATE TABLE SUPPLIES_IMPORT (
    ImportId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Import Transaction ID (Auto-increment)',
    SuppliesId INTEGER NOT NULL COMMENT 'Supply ID (Foreign Key)',
    ImportAmount INTEGER NOT NULL COMMENT 'Quantity Imported',
    ImportDate DATE NOT NULL COMMENT 'Import Date',
    FOREIGN KEY (SuppliesId) REFERENCES SUPPLIES(SuppliesId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Table WAGE
-- Stores the list of labor/service types
CREATE TABLE WAGE (
    WageId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Wage ID (Auto-increment)',
    WageName VARCHAR(255) UNIQUE NOT NULL COMMENT 'Wage/Service Name',
    WageValue NUMERIC(15, 2) NOT NULL DEFAULT 0 COMMENT 'Wage Value / Service Fee'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Table REPAIR
-- Stores repair ticket information for a reception instance
CREATE TABLE REPAIR (
    RepairId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Repair Ticket ID (Auto-increment)',
    ReceptionId INTEGER NOT NULL COMMENT 'Reception ID (Foreign Key)',
    RepairDate DATE NOT NULL COMMENT 'Repair Date',
    RepairMoney NUMERIC(15, 2) DEFAULT 0 COMMENT 'Total Repair Cost',
    FOREIGN KEY (ReceptionId) REFERENCES CAR_RECEPTION(ReceptionId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Table REPAIR_DETAILS
-- Stores details of each repair item (supplies used + work content)
CREATE TABLE REPAIR_DETAILS (
    RepairDetailId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Detail ID (Auto-increment)',
    RepairId INTEGER NOT NULL COMMENT 'Repair Ticket ID (Foreign Key)',
    Content VARCHAR(255) COMMENT 'Repair Content / Description',
    SuppliesId INTEGER NOT NULL COMMENT 'Supply ID (Foreign Key)',
    SuppliesAmount INTEGER NOT NULL DEFAULT 1 COMMENT 'Quantity of supplies used',
    WageId INTEGER COMMENT 'Wage ID (Foreign Key)',
    FOREIGN KEY (RepairId) REFERENCES REPAIR(RepairId),
    FOREIGN KEY (SuppliesId) REFERENCES SUPPLIES(SuppliesId),
    FOREIGN KEY (WageId) REFERENCES WAGE(WageId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Table RECEIPT
-- Stores payment collection information from customers
CREATE TABLE RECEIPT (
    ReceiptId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Receipt ID (Auto-increment)',
    ReceptionId INTEGER NOT NULL COMMENT 'Reception ID (Foreign Key)',
    ReceiptDate DATE NOT NULL COMMENT 'Payment Date',
    MoneyAmount NUMERIC(15, 2) NOT NULL COMMENT 'Amount Received'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Table REVENUE_REPORT
-- Stores monthly revenue report summary
CREATE TABLE REVENUE_REPORT (
    ReportId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Report ID',
    ReportMonth INTEGER NOT NULL COMMENT 'Report Month',
    ReportYear INTEGER NOT NULL COMMENT 'Report Year',
    TotalRevenue NUMERIC(15, 2) DEFAULT 0 COMMENT 'Total Revenue'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. Table REVENUE_REPORT_DETAILS
-- Stores revenue details breakdown by car brand
CREATE TABLE REVENUE_REPORT_DETAILS (
    ReportDetailId INTEGER AUTO_INCREMENT PRIMARY KEY,
    ReportId INTEGER NOT NULL COMMENT 'Report ID (Foreign Key)',
    BrandId INTEGER NOT NULL COMMENT 'Brand ID (Foreign Key)',
    Count INTEGER DEFAULT 0 COMMENT 'Number of repairs',
    TotalMoney NUMERIC(15, 2) DEFAULT 0 COMMENT 'Total Amount',
    Rate FLOAT DEFAULT 0 COMMENT 'Ratio / Percentage',
    FOREIGN KEY (ReportId) REFERENCES REVENUE_REPORT(ReportId),
    FOREIGN KEY (BrandId) REFERENCES CAR_BRAND(BrandId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. Table STOCK_REPORT
-- Stores monthly inventory/stock report summary
CREATE TABLE STOCK_REPORT (
    StockReportId INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT 'Stock Report ID',
    ReportMonth INTEGER NOT NULL COMMENT 'Report Month',
    ReportYear INTEGER NOT NULL COMMENT 'Report Year'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 13. Table STOCK_REPORT_DETAILS
-- Stores inventory details for each supply item
CREATE TABLE STOCK_REPORT_DETAILS (
    StockDetailId INTEGER AUTO_INCREMENT PRIMARY KEY,
    StockReportId INTEGER NOT NULL COMMENT 'Stock Report ID (Foreign Key)',
    SuppliesId INTEGER NOT NULL COMMENT 'Supply ID (Foreign Key)',
    BeginQty INTEGER DEFAULT 0 COMMENT 'Beginning Inventory',
    IssueQty INTEGER DEFAULT 0 COMMENT 'Incurred Quantity (Import/Export)',
    EndQty INTEGER DEFAULT 0 COMMENT 'Ending Inventory',
    FOREIGN KEY (StockReportId) REFERENCES STOCK_REPORT(StockReportId),
    FOREIGN KEY (SuppliesId) REFERENCES SUPPLIES(SuppliesId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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