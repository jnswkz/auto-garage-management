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
INSERT INTO `car` VALUES ('30F-111.22',4,'Pháº¡m Minh DÅ©ng','0905111222','HoÃ n Kiáº¿m, HÃ  Ná»™i','dung.pham@email.com'),('51A',5,'AAAA','9237287355','aaa',NULL),('51H-987.65',2,'Tráº§n Thá»‹ BÃ­ch','0912345678','45 Nguyá»…n TrÃ£i, Q5, TP.HCM','bich.tran@email.com'),('59A-123.45',1,'Nguyá»…n VÄƒn An','0909123456','123 LÃª Lá»£i, Q1, TP.HCM','an.nguyen@email.com'),('59K-234.56',1,'VÃµ Thá»‹ Em','0933444555','Thá»§ Äá»©c, TP.HCM','em.vo@email.com'),('60C-555.88',3,'LÃª HoÃ ng CÆ°á»ng','0988777666','BiÃªn HÃ²a, Äá»“ng Nai','cuong.le@email.com'),('62A-616.36',5,'VÃµ ThÃ nh Äáº¡t','0369472671','Äá»‹a ngá»¥c',NULL);
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
INSERT INTO `supplies` VALUES (1,'GÆ°Æ¡ng chiáº¿u háº­u Toyota',1500000.00,20),(2,'Bá»‘ tháº¯ng Ä‘Ä©a',450000.00,50),(3,'Nhá»›t Castrol 4L',550000.00,100),(4,'Lá»c giÃ³ Ä‘iá»u hÃ²a',250000.00,30),(5,'Bugi Denso',120000.00,60),(6,'Gáº¡t mÆ°a Bosch',300000.00,40);
/*!40000 ALTER TABLE `supplies` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `wage` WRITE;
/*!40000 ALTER TABLE `wage` DISABLE KEYS */;
INSERT INTO `wage` VALUES (1,'Thay nhá»›t mÃ¡y',50000.00),(2,'Rá»­a xe bá»t tuyáº¿t',70000.00),(3,'Vá»‡ sinh khoang mÃ¡y',300000.00),(4,'Thay mÃ¡ phanh',150000.00),(5,'Kiá»ƒm tra tá»•ng quÃ¡t',100000.00),(6,'SÆ¡n dáº·m vÃ¡',500000.00);
/*!40000 ALTER TABLE `wage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'garagemanagement'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-22 17:48:48

