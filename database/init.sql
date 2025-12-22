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

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car`
--

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES ('30F-111.22',4,'Phạm Minh Dũng','0905111222','Hoàn Kiếm, Hà Nội','dung.pham@email.com'),('51A',5,'AAAA','9237287355','aaa',NULL),('51H-987.65',2,'Trần Thị Bích','0912345678','45 Nguyễn Trãi, Q5, TP.HCM','bich.tran@email.com'),('59A-123.45',1,'Nguyễn Văn An','0909123456','123 Lê Lợi, Q1, TP.HCM','an.nguyen@email.com'),('59K-234.56',1,'Võ Thị Em','0933444555','Thủ Đức, TP.HCM','em.vo@email.com'),('60C-555.88',3,'Lê Hoàng Cường','0988777666','Biên Hòa, Đồng Nai','cuong.le@email.com'),('62A-616.36',5,'Võ Thành Đạt','0369472671','Địa ngục',NULL);
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_brand`
--

DROP TABLE IF EXISTS `car_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_brand` (
  `BrandId` int NOT NULL AUTO_INCREMENT COMMENT 'Brand ID (Auto-increment)',
  `BrandName` varchar(255) NOT NULL COMMENT 'Brand Name',
  PRIMARY KEY (`BrandId`),
  UNIQUE KEY `BrandName` (`BrandName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_brand`
--

LOCK TABLES `car_brand` WRITE;
/*!40000 ALTER TABLE `car_brand` DISABLE KEYS */;
INSERT INTO `car_brand` VALUES (5,'Ford'),(2,'Honda'),(3,'Hyundai'),(4,'Kia'),(6,'Mazda'),(1,'Toyota');
/*!40000 ALTER TABLE `car_brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_reception`
--

DROP TABLE IF EXISTS `car_reception`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_reception` (
  `ReceptionId` int NOT NULL AUTO_INCREMENT COMMENT 'Reception ID (Auto-increment)',
  `LicensePlate` varchar(255) NOT NULL COMMENT 'License Plate (Foreign Key)',
  `ReceptionDate` date NOT NULL COMMENT 'Date of reception',
  `Debt` decimal(15,2) DEFAULT '0.00' COMMENT 'Total debt at the time of reception',
  PRIMARY KEY (`ReceptionId`),
  KEY `LicensePlate` (`LicensePlate`),
  CONSTRAINT `car_reception_ibfk_1` FOREIGN KEY (`LicensePlate`) REFERENCES `car` (`LicensePlate`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_reception`
--

LOCK TABLES `car_reception` WRITE;
/*!40000 ALTER TABLE `car_reception` DISABLE KEYS */;
INSERT INTO `car_reception` VALUES (1,'59A-123.45','2025-12-22',0.00),(2,'51H-987.65','2025-12-22',500000.00),(3,'60C-555.88','2025-12-22',0.00),(4,'59K-234.56','2025-12-21',1200000.00),(5,'62A-616.36','2025-12-22',0.00),(6,'51A','2025-12-22',0.00);
/*!40000 ALTER TABLE `car_reception` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_CheckMaxCarReception` BEFORE INSERT ON `car_reception` FOR EACH ROW BEGIN
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `parameter`
--

DROP TABLE IF EXISTS `parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parameter` (
  `name` varchar(50) NOT NULL,
  `value` int DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter`
--

LOCK TABLES `parameter` WRITE;
/*!40000 ALTER TABLE `parameter` DISABLE KEYS */;
INSERT INTO `parameter` VALUES ('IsOverPay',0),('MaxCarReception',30);
/*!40000 ALTER TABLE `parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt`
--

DROP TABLE IF EXISTS `receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt` (
  `ReceiptId` int NOT NULL AUTO_INCREMENT COMMENT 'Receipt ID (Auto-increment)',
  `ReceptionId` int NOT NULL COMMENT 'Reception ID (Foreign Key)',
  `ReceiptDate` date NOT NULL COMMENT 'Payment Date',
  `MoneyAmount` decimal(15,2) NOT NULL COMMENT 'Amount Received',
  PRIMARY KEY (`ReceiptId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt`
--

LOCK TABLES `receipt` WRITE;
/*!40000 ALTER TABLE `receipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `receipt` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_CheckPaymentLimit` BEFORE INSERT ON `receipt` FOR EACH ROW BEGIN
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_UpdateDebtAfterReceipt` AFTER INSERT ON `receipt` FOR EACH ROW BEGIN
    -- Trừ số tiền nợ trong bảng tiếp nhận tương ứng với số tiền vừa thu
    UPDATE CAR_RECEPTION
    SET Debt = Debt - NEW.MoneyAmount
    WHERE ReceptionId = NEW.ReceptionId;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `repair`
--

DROP TABLE IF EXISTS `repair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair` (
  `RepairId` int NOT NULL AUTO_INCREMENT COMMENT 'Repair Ticket ID (Auto-increment)',
  `ReceptionId` int NOT NULL COMMENT 'Reception ID (Foreign Key)',
  `RepairDate` date NOT NULL COMMENT 'Repair Date',
  `RepairMoney` decimal(15,2) DEFAULT '0.00' COMMENT 'Total Repair Cost',
  PRIMARY KEY (`RepairId`),
  KEY `ReceptionId` (`ReceptionId`),
  CONSTRAINT `repair_ibfk_1` FOREIGN KEY (`ReceptionId`) REFERENCES `car_reception` (`ReceptionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair`
--

LOCK TABLES `repair` WRITE;
/*!40000 ALTER TABLE `repair` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_details`
--

DROP TABLE IF EXISTS `repair_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_details`
--

LOCK TABLES `repair_details` WRITE;
/*!40000 ALTER TABLE `repair_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revenue_report`
--

DROP TABLE IF EXISTS `revenue_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `revenue_report` (
  `ReportId` int NOT NULL AUTO_INCREMENT COMMENT 'Report ID',
  `ReportMonth` int NOT NULL COMMENT 'Report Month',
  `ReportYear` int NOT NULL COMMENT 'Report Year',
  `TotalRevenue` decimal(15,2) DEFAULT '0.00' COMMENT 'Total Revenue',
  PRIMARY KEY (`ReportId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revenue_report`
--

LOCK TABLES `revenue_report` WRITE;
/*!40000 ALTER TABLE `revenue_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `revenue_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revenue_report_details`
--

DROP TABLE IF EXISTS `revenue_report_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revenue_report_details`
--

LOCK TABLES `revenue_report_details` WRITE;
/*!40000 ALTER TABLE `revenue_report_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `revenue_report_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_report`
--

DROP TABLE IF EXISTS `stock_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_report` (
  `StockReportId` int NOT NULL AUTO_INCREMENT COMMENT 'Stock Report ID',
  `ReportMonth` int NOT NULL COMMENT 'Report Month',
  `ReportYear` int NOT NULL COMMENT 'Report Year',
  PRIMARY KEY (`StockReportId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_report`
--

LOCK TABLES `stock_report` WRITE;
/*!40000 ALTER TABLE `stock_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `stock_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_report_details`
--

DROP TABLE IF EXISTS `stock_report_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_report_details`
--

LOCK TABLES `stock_report_details` WRITE;
/*!40000 ALTER TABLE `stock_report_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `stock_report_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplies`
--

DROP TABLE IF EXISTS `supplies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplies` (
  `SuppliesId` int NOT NULL AUTO_INCREMENT COMMENT 'Supply ID (Auto-increment)',
  `SuppliesName` varchar(255) NOT NULL COMMENT 'Supply Name',
  `SuppliesPrice` decimal(15,2) NOT NULL DEFAULT '0.00' COMMENT 'Unit Price',
  `InventoryNumber` int DEFAULT '0' COMMENT 'Inventory Quantity',
  PRIMARY KEY (`SuppliesId`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplies`
--

LOCK TABLES `supplies` WRITE;
/*!40000 ALTER TABLE `supplies` DISABLE KEYS */;
INSERT INTO `supplies` VALUES (1,'Gương chiếu hậu Toyota',1500000.00,20),(2,'Bố thắng đĩa',450000.00,50),(3,'Nhớt Castrol 4L',550000.00,100),(4,'Lọc gió điều hòa',250000.00,30),(5,'Bugi Denso',120000.00,60),(6,'Gạt mưa Bosch',300000.00,40);
/*!40000 ALTER TABLE `supplies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wage`
--

DROP TABLE IF EXISTS `wage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wage` (
  `WageId` int NOT NULL AUTO_INCREMENT COMMENT 'Wage ID (Auto-increment)',
  `WageName` varchar(255) NOT NULL COMMENT 'Wage/Service Name',
  `WageValue` decimal(15,2) NOT NULL DEFAULT '0.00' COMMENT 'Wage Value / Service Fee',
  PRIMARY KEY (`WageId`),
  UNIQUE KEY `WageName` (`WageName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wage`
--

LOCK TABLES `wage` WRITE;
/*!40000 ALTER TABLE `wage` DISABLE KEYS */;
INSERT INTO `wage` VALUES (1,'Thay nhớt máy',50000.00),(2,'Rửa xe bọt tuyết',70000.00),(3,'Vệ sinh khoang máy',300000.00),(4,'Thay má phanh',150000.00),(5,'Kiểm tra tổng quát',100000.00),(6,'Sơn dặm vá',500000.00);
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
