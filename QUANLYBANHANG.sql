CREATE DATABASE QUANLYBANHANG
GO

USE QUANLYBANHANG
GO

CREATE TABLE Users(
	Username VARCHAR(50) PRIMARY KEY,
	Pass VARCHAR(50) NOT NULL,
	Roles INT NOT NULL CHECK (Roles IN (0,1))
);
GO

CREATE TABLE Products(
	Ma_SP INT PRIMARY KEY,
	Ten_SP NVARCHAR(100) Not Null,
	Gia_Ban INT,
	So_Luong_Ton INT NOT NULL CHECK (So_Luong_Ton >= 0)
);

CREATE TABLE Customers(
	Ma_KH INT PRIMARY KEY IDENTITY(1,1),
	Ten_KH NVARCHAR(100) not null,
	SDT VARCHAR(10),
	Dia_Chi NVARCHAR(50),
	Username VARCHAR(50)
);

CREATE TABLE Orders(
	Ma_DH INT PRIMARY KEY IDENTITY(1,1),
	Ma_KH INT NOT NULL
	
);

ALTER TABLE Orders
ADD Trang_Thai NVARCHAR(50) DEFAULT N'CHƯA THANH TOÁN'

CREATE TABLE OrderDetails(
	Ma_DH INT,
	Ma_SP INT,
	So_Luong INT not null,
	Gia_Ban_Hien_Tai DECIMAL (18,0) not null,
	Ngay_Dat DATE DEFAULT GETDATE(),
	Tong_Tien DECIMAL(18,0),
	PRIMARY KEY (Ma_DH, Ma_SP)
);

ALTER TABLE Orders
ADD CONSTRAINT FK_MAKH_ORDERS
FOREIGN KEY (Ma_KH) REFERENCES Customers(Ma_KH);
GO

ALTER TABLE OrderDetails
ADD CONSTRAINT FK_MADH_ORDERDETIALS
FOREIGN KEY (Ma_DH) REFERENCES Orders(Ma_DH);
GO

ALTER TABLE OrderDetails
ADD CONSTRAINT FK_MASP_PRODUCTS
FOREIGN KEY (Ma_SP) REFERENCES Products(Ma_SP);
GO

ALTER TABLE Customers
ADD CONSTRAINT FK_Username_Customers
FOREIGN KEY (Username) REFERENCES Users(Username);
GO

INSERT INTO DBO.Users(Username, Pass, Roles)
VALUES ('admin', '88888888', 0);

SELECT * FROM Users
SELECT * FROM dbo.Customers
SELECT * FROM dbo.Orders
SELECT * FROM dbo.OrderDetails
SELECT * FROM DBO.Products

INSERT INTO dbo.Products(Ma_SP, Ten_SP, Gia_Ban, So_Luong_Ton) 
VALUES	(1, N'Laptop Dell XPS 13', 29990000, 15),
		(2, N'iPhone 15 Pro Max', 34990000, 8),
		(3, N'Tai nghe Sony WH-1000XM5', 7990000, 22),
		(4, N'Bàn phím cơ Logitech G Pro', 2490000, 50),
		(5, N'Chuột không dây Razer Viper', 1890000, 35),
		(6, N'Màn hình Samsung 27 inch 4K', 12990000, 12),
		(7, N'Máy in HP LaserJet Pro', 5890000, 7),
		(8, N'Ổ cứng SSD 1TB Samsung 980', 2190000, 40),
		(9, N'Loa Bluetooth JBL Flip 6', 3290000, 25),
		(10, N'Webcam Logitech C920', 1590000, 18);

