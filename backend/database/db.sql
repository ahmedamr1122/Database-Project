-- =============================================
-- DATABASE INITIALIZATION
-- =============================================
-- DROP DATABASE IF EXISTS OnlineBookstore;
-- CREATE DATABASE OnlineBookstore;
-- USE OnlineBookstore;

-- =============================================
-- 1. TABLE CREATION
-- =============================================

-- Publishers Table 
CREATE TABLE Publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    address TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);  

-- Authors Table 
-- Separate table to handle "one or more authors" requirement
CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL
);

-- Books Table 
CREATE TABLE Books (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    publisher_id INT NOT NULL,
    pub_year INT,
    selling_price DECIMAL(10, 2) NOT NULL,
    category ENUM('Science', 'Art', 'Religion', 'History', 'Geography') NOT NULL,
    stock INT DEFAULT 0,
    threshold INT DEFAULT 10, -- Minimum quantity before auto-order 
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Book_Authors Bridge Table (Many-to-Many) 
CREATE TABLE Book_Authors (
    isbn VARCHAR(20),
    author_id INT,
    PRIMARY KEY (isbn, author_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);

-- Users Table (Admins & Customers) 
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    shipping_address TEXT, -- Required for Customers 
    role ENUM('admin', 'customer') DEFAULT 'customer'
);

-- Shopping Cart Table 
CREATE TABLE Shopping_Cart (
    user_id INT,
    isbn VARCHAR(20),
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    PRIMARY KEY (user_id, isbn),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (isbn) REFERENCES Books(isbn) ON DELETE CASCADE
);

-- Customer Orders Header 
CREATE TABLE Customer_Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2),
    credit_card_no VARCHAR(16) NOT NULL, -- Added per requirement 
    expiry_date DATE NOT NULL,           -- Added per requirement 
    status ENUM('Pending', 'Confirmed') DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Order Items Detail Table
CREATE TABLE Order_Items (
    order_id INT,
    isbn VARCHAR(20),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL, -- Snapshot price at time of sale
    PRIMARY KEY (order_id, isbn),
    FOREIGN KEY (order_id) REFERENCES Customer_Orders(order_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

-- Publisher Orders 
CREATE TABLE Publisher_Orders (
    po_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20),
    publisher_id INT, -- Added to link order to specific publisher
    quantity INT NOT NULL DEFAULT 50, -- Constant quantity 
    order_date DATE DEFAULT (CURRENT_DATE),
    status ENUM('Pending', 'Confirmed') DEFAULT 'Pending',
    FOREIGN KEY (isbn) REFERENCES Books(isbn),
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
);

-- =============================================
-- 2. TRIGGERS (BUSINESS LOGIC)
-- =============================================
DELIMITER //

-- 1. Prevent Negative Stock [cite: 35]
CREATE TRIGGER Prevent_Negative_Stock
BEFORE UPDATE ON Books
FOR EACH ROW
BEGIN
    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Stock cannot be negative.';
    END IF;
END; //

-- 2. Auto-order from Publisher 
-- Triggered when stock drops below threshold
CREATE TRIGGER Auto_Order_Trigger
AFTER UPDATE ON Books
FOR EACH ROW
BEGIN
    -- Only trigger if stock WAS above/equal threshold AND IS NOW below
    IF NEW.stock < NEW.threshold AND OLD.stock >= NEW.threshold THEN
        INSERT INTO Publisher_Orders (isbn, publisher_id, quantity, status)
        VALUES (NEW.isbn, NEW.publisher_id, 50, 'Pending');
    END IF;
END; //

-- 3. Update Stock on Publisher Confirmation 
CREATE TRIGGER Update_Stock_On_Confirmation
AFTER UPDATE ON Publisher_Orders
FOR EACH ROW
BEGIN
    IF OLD.status = 'Pending' AND NEW.status = 'Confirmed' THEN
        UPDATE Books SET stock = stock + NEW.quantity WHERE isbn = NEW.isbn;
    END IF;
END; //

-- 4. Deduct Stock on Customer Purchase 
CREATE TRIGGER Deduct_Stock_On_Purchase
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    UPDATE Books SET stock = stock - NEW.quantity WHERE isbn = NEW.isbn;
END; //

DELIMITER ;


-- 3. ADMIN REPORTS (QUERIES) 


-- A) Total sales for previous month 
SELECT SUM(total_price) AS Last_Month_Sales
FROM Customer_Orders 
WHERE order_date >= DATE_FORMAT(CURRENT_DATE - INTERVAL 1 MONTH, '%Y-%m-01') 
  AND order_date < DATE_FORMAT(CURRENT_DATE, '%Y-%m-01');

-- B) Total sales for a specific day (Example: 2025-12-23) 
SELECT SUM(total_price) AS Daily_Sales
FROM Customer_Orders
WHERE DATE(order_date) = '2025-12-23';

-- C) Top 5 Customers (Last 3 Months) 
SELECT u.username, SUM(co.total_price) AS Total_Spent 
FROM Customer_Orders co
JOIN Users u ON co.user_id = u.user_id
WHERE co.order_date >= CURRENT_DATE - INTERVAL 3 MONTH 
GROUP BY u.username 
ORDER BY Total_Spent DESC 
LIMIT 5;

-- D) Top 10 Selling Books (Last 3 Months) 
SELECT b.isbn, b.title, SUM(oi.quantity) AS Copies_Sold 
FROM Order_Items oi
JOIN Books b ON oi.isbn = b.isbn
JOIN Customer_Orders co ON oi.order_id = co.order_id
WHERE co.order_date >= CURRENT_DATE - INTERVAL 3 MONTH 
GROUP BY b.isbn, b.title -- Fixed: Added title to GROUP BY
ORDER BY Copies_Sold DESC 
LIMIT 10;

-- E) Total Replenishment Orders for a specific book
SELECT isbn, COUNT(*) AS Replenishment_Count 
FROM Publisher_Orders 
WHERE isbn = '978-0-13-468599-1';