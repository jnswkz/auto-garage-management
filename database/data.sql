USE GarageManagement;

-- 1. Thêm dữ liệu Hiệu xe (CAR_BRAND)
INSERT INTO CAR_BRAND (BrandName) VALUES 
('Toyota'),
('Honda'),
('Hyundai'),
('Kia'),
('Ford'),
('Mazda');

-- 2. Thêm dữ liệu Vật tư (SUPPLIES)
INSERT INTO SUPPLIES (SuppliesName, SuppliesPrice, InventoryNumber) VALUES 
('Gương chiếu hậu Toyota', 1500000, 20),
('Bố thắng đĩa', 450000, 50),
('Nhớt Castrol 4L', 550000, 100),
('Lọc gió điều hòa', 250000, 30),
('Bugi Denso', 120000, 60),
('Gạt mưa Bosch', 300000, 40);

-- 3. Thêm dữ liệu Tiền công (WAGE)
INSERT INTO WAGE (WageName, WageValue) VALUES 
('Thay nhớt máy', 50000),
('Rửa xe bọt tuyết', 70000),
('Vệ sinh khoang máy', 300000),
('Thay má phanh', 150000),
('Kiểm tra tổng quát', 100000),
('Sơn dặm vá', 500000);

-- 4. Thêm dữ liệu Hồ sơ xe (CAR)
INSERT INTO CAR (LicensePlate, BrandId, OwnerName, PhoneNumber, Address, Email) VALUES 
('59A-123.45', 1, 'Nguyễn Văn An', '0909123456', '123 Lê Lợi, Q1, TP.HCM', 'an.nguyen@email.com'),
('51H-987.65', 2, 'Trần Thị Bích', '0912345678', '45 Nguyễn Trãi, Q5, TP.HCM', 'bich.tran@email.com'),
('60C-555.88', 3, 'Lê Hoàng Cường', '0988777666', 'Biên Hòa, Đồng Nai', 'cuong.le@email.com'),
('30F-111.22', 4, 'Phạm Minh Dũng', '0905111222', 'Hoàn Kiếm, Hà Nội', 'dung.pham@email.com'),
('59K-234.56', 1, 'Võ Thị Em', '0933444555', 'Thủ Đức, TP.HCM', 'em.vo@email.com');

-- 5. Thêm dữ liệu Tiếp nhận xe (CAR_RECEPTION)
INSERT INTO CAR_RECEPTION (LicensePlate, ReceptionDate, Debt) VALUES 
('59A-123.45', CURDATE(), 0),        -- Xe không nợ, mới vào hôm nay
('51H-987.65', CURDATE(), 500000),   -- Xe này đang nợ cũ 500k
('60C-555.88', CURDATE(), 0),        -- Xe không nợ
('59K-234.56', CURDATE() - INTERVAL 1 DAY, 1200000); -- Xe vào ngày hôm qua, nợ 1.2tr