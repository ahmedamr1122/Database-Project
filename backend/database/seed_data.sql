-- =============================================
-- TRUNCATE TABLES
-- =============================================
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE Books;
TRUNCATE TABLE Authors;
TRUNCATE TABLE Publishers;
TRUNCATE TABLE Book_Authors;
TRUNCATE TABLE Users;
TRUNCATE TABLE Shopping_Cart;
TRUNCATE TABLE Customer_Orders;

SET FOREIGN_KEY_CHECKS = 1;
-- =============================================
-- SAMPLE DATA FOR TESTING
-- =============================================
USE OnlineBookstore;

-- =============================================
-- 1. PUBLISHERS
-- =============================================

INSERT INTO Publishers (name, address, phone_number) VALUES
('Penguin Random House', '1745 Broadway, New York, NY 10019', '+1-212-782-9000'),
('HarperCollins', '195 Broadway, New York, NY 10007', '+1-212-207-7000'),
('Simon & Schuster', '1230 Avenue of the Americas, New York, NY 10020', '+1-212-698-7000'),
('Macmillan', '120 Broadway, New York, NY 10271', '+1-646-307-5151'),
('Hachette Book Group', '1290 Avenue of the Americas, New York, NY 10104', '+1-212-364-1100');

-- =============================================
-- 2. AUTHORS
-- =============================================
INSERT INTO Authors (author_name) VALUES
('J.K. Rowling'),
('George R.R. Martin'),
('Stephen King'),
('Agatha Christie'),
('Haruki Murakami'),
('Margaret Atwood'),
('Neil Gaiman'),
('Toni Morrison'),
('Yuval Noah Harari'),
('Michelle Obama');

-- =============================================
-- 3. BOOKS
-- =============================================
INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold) VALUES
('978-0-545-01022-1', 'Harry Potter and the Sorcerer\'s Stone', 1, 1997, 12.99, 'Science', 50, 10),
('978-0-553-89785-6', 'A Game of Thrones', 2, 1996, 15.99, 'History', 30, 8),
('978-0-385-08695-0', 'The Shining', 3, 1977, 11.99, 'Art', 40, 12),
('978-0-06-269366-2', 'Murder on the Orient Express', 2, 1934, 9.99, 'History', 25, 7),
('978-0-307-74255-7', 'Kafka on the Shore', 4, 2002, 14.99, 'Art', 20, 5),
('978-0-385-53783-1', 'The Handmaid\'s Tale', 3, 1985, 13.99, 'Religion', 35, 9),
('978-0-06-210732-9', 'American Gods', 2, 2001, 16.99, 'Religion', 28, 6),
('978-0-679-73237-2', 'Beloved', 1, 1987, 12.49, 'History', 22, 8),
('978-0-06-231609-7', 'Sapiens: A Brief History of Humankind', 2, 2011, 18.99, 'History', 45, 10),
('978-1-524-76315-0', 'Becoming', 5, 2018, 17.99, 'Geography', 60, 15);

-- =============================================
-- 4. BOOK_AUTHORS (Many-to-Many)
-- =============================================
INSERT INTO Book_Authors (isbn, author_id) VALUES
('978-0-545-01022-1', 1), -- Harry Potter -> J.K. Rowling
('978-0-553-89785-6', 2), -- A Game of Thrones -> George R.R. Martin
('978-0-385-08695-0', 3), -- The Shining -> Stephen King
('978-0-06-269366-2', 4), -- Murder on the Orient Express -> Agatha Christie
('978-0-307-74255-7', 5), -- Kafka on the Shore -> Haruki Murakami
('978-0-385-53783-1', 6), -- The Handmaid's Tale -> Margaret Atwood
('978-0-06-210732-9', 7), -- American Gods -> Neil Gaiman
('978-0-679-73237-2', 8), -- Beloved -> Toni Morrison
('978-0-06-231609-7', 9), -- Sapiens -> Yuval Noah Harari
('978-1-524-76315-0', 10); -- Becoming -> Michelle Obama

-- =============================================
-- 5. USERS (Admins & Customers)
-- =============================================
INSERT INTO Users (username, password, first_name, last_name, email, phone_number, shipping_address, role) VALUES
-- Admin user
('admin', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'System', 'Administrator', 'admin@bookstore.com', '+1-555-0100', '123 Admin St, Admin City, AC 12345', 'admin'),

-- Customer users
('john_doe', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'John', 'Doe', 'john.doe@email.com', '+1-555-0101', '456 Customer Ave, Customer City, CC 67890', 'customer'),
('jane_smith', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'Jane', 'Smith', 'jane.smith@email.com', '+1-555-0102', '789 Reader Blvd, Reader Town, RT 54321', 'customer'),
('bob_wilson', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'Bob', 'Wilson', 'bob.wilson@email.com', '+1-555-0103', '321 Book Lover Ln, Book City, BC 98765', 'customer'),
('alice_brown', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'Alice', 'Brown', 'alice.brown@email.com', '+1-555-0104', '654 Library Rd, Library Town, LT 13579', 'customer'),
('charlie_davis', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'Charlie', 'Davis', 'charlie.davis@email.com', '+1-555-0105', '987 Page Turner St, Page City, PC 24680', 'customer');

-- Password for all users is 'password123' (hashed)

-- =============================================
-- 6. SHOPPING CART (Sample cart items)
-- =============================================
INSERT INTO Shopping_Cart (user_id, isbn, quantity) VALUES
(2, '978-0-545-01022-1', 2), -- John Doe: 2 Harry Potter books
(2, '978-0-553-89785-6', 1), -- John Doe: 1 Game of Thrones
(3, '978-0-385-08695-0', 1), -- Jane Smith: 1 The Shining
(4, '978-0-06-269366-2', 3), -- Bob Wilson: 3 Murder on the Orient Express
(5, '978-0-307-74255-7', 1); -- Alice Brown: 1 Kafka on the Shore
-- (5, '978-0-385-53783-1', 1); -- Alice Brown: 1 The Handmaid's Tale

-- =============================================
-- 7. CUSTOMER ORDERS (Sample orders)
-- =============================================
INSERT INTO Customer_Orders (user_id, order_date, total_price, credit_card_no, expiry_date, status) VALUES
(2, '2025-12-01 10:30:00', 44.97, '4111111111111111', '2026-12-26', 'Pending'), -- John Doe order
(3, '2025-12-02 14:20:00', 11.99, '5555555555554444', '2027-08-27', 'Pending'), -- Jane Smith order
(4, '2025-12-03 16:45:00', 29.97, '378282246310005', '2028-05-28', 'Pending'),  -- Bob Wilson order
(5, '2025-12-04 09:15:00', 14.99, '6011111111111117', '2029-11-29', 'Pending'), -- Alice Brown order
(2, '2025-12-05 11:00:00', 15.99, '4111111111111111', '2026-12-26', 'Pending'); -- John Doe second order

-- =============================================
-- 8. ORDER ITEMS (Details for orders)
-- =============================================
INSERT INTO Order_Items (order_id, isbn, quantity, unit_price) VALUES
(1, '978-0-545-01022-1', 2, 12.99), -- John Doe's first order
(1, '978-0-553-89785-6', 1, 15.99),
(2, '978-0-385-08695-0', 1, 11.99), -- Jane Smith's order
(3, '978-0-06-269366-2', 3, 9.99),  -- Bob Wilson's order
(4, '978-0-307-74255-7', 1, 14.99), -- Alice Brown's order
(5, '978-0-553-89785-6', 1, 15.99); -- John Doe's second order

-- =============================================
-- 9. PUBLISHER ORDERS (Auto-generated or manual)
-- =============================================
INSERT INTO Publisher_Orders (isbn, publisher_id, quantity, order_date, status) VALUES
('978-0-545-01022-1', 1, 50, '2024-12-01', 'Pending'), -- Low stock trigger
('978-0-553-89785-6', 2, 50, '2024-12-02', 'Confirmed'), -- Confirmed order
('978-0-385-08695-0', 3, 50, '2024-12-03', 'Pending'); -- Pending order

-- =============================================
-- 10. EDGE CASE TEST DATA
-- =============================================

-- Book with very low stock (should appear on admin dashboard low stock list)
INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold) VALUES
('978-0-LOWSTOCK-1', 'Almost Out of Stock', 1, 2020, 25.99, 'Science', 3, 10);
INSERT INTO Authors (author_name) VALUES ('Test Author Low');
INSERT INTO Book_Authors (isbn, author_id) VALUES ('978-0-LOWSTOCK-1', 11);

-- Book at exact threshold (edge case for auto-order trigger)
INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold) VALUES
('978-0-ATTHRESH-1', 'Right at Threshold', 2, 2021, 19.99, 'History', 10, 10);
INSERT INTO Authors (author_name) VALUES ('Threshold Tester');
INSERT INTO Book_Authors (isbn, author_id) VALUES ('978-0-ATTHRESH-1', 12);

-- Book with ZERO stock (should NOT be addable to cart, tests stock validation)
INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold) VALUES
('978-0-NOSTOCK-01', 'Out of Stock Book', 3, 2019, 29.99, 'Art', 0, 5);
INSERT INTO Authors (author_name) VALUES ('Sold Out Author');
INSERT INTO Book_Authors (isbn, author_id) VALUES ('978-0-NOSTOCK-01', 13);

-- Book with MULTIPLE authors (tests author handling)
INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold) VALUES
('978-0-COAUTHOR-1', 'Collaborative Work', 4, 2022, 34.99, 'Science', 50, 10);
INSERT INTO Authors (author_name) VALUES ('First Coauthor'), ('Second Coauthor'), ('Third Coauthor');
INSERT INTO Book_Authors (isbn, author_id) VALUES 
('978-0-COAUTHOR-1', 14),
('978-0-COAUTHOR-1', 15),
('978-0-COAUTHOR-1', 16);

-- HIGH VOLUME customer for "Top Customers" report testing
INSERT INTO Users (username, password, first_name, last_name, email, phone_number, shipping_address, role) VALUES
('vip_customer', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'VIP', 'Customer', 'vip@email.com', '+1-555-9999', 'VIP Street 1, VIP City', 'customer');

-- Many orders from VIP customer (for reports - last 3 months)
INSERT INTO Customer_Orders (user_id, order_date, total_price, credit_card_no, expiry_date, status) VALUES
(7, NOW() - INTERVAL 1 DAY, 150.00, '4111111111111111', '2028-12-01', 'Pending'),
(7, NOW() - INTERVAL 5 DAY, 200.00, '4111111111111111', '2028-12-01', 'Pending'),
(7, NOW() - INTERVAL 10 DAY, 175.00, '4111111111111111', '2028-12-01', 'Pending'),
(7, NOW() - INTERVAL 30 DAY, 300.00, '4111111111111111', '2028-12-01', 'Pending'),
(7, NOW() - INTERVAL 60 DAY, 250.00, '4111111111111111', '2028-12-01', 'Pending');

-- Order Items for VIP customer order (testing top selling books)
INSERT INTO Order_Items (order_id, isbn, quantity, unit_price) VALUES
(6, '978-0-545-01022-1', 5, 12.99),  -- Harry Potter sells a lot
(7, '978-0-545-01022-1', 8, 12.99),  -- Harry Potter
(8, '978-0-545-01022-1', 3, 12.99),  
(8, '978-0-553-89785-6', 5, 15.99),  -- Game of Thrones sells too
(9, '978-0-553-89785-6', 10, 15.99), 
(10, '978-0-553-89785-6', 7, 15.99);

-- OLD order (outside 3-month window - should NOT appear in Top Customer report)
INSERT INTO Customer_Orders (user_id, order_date, total_price, credit_card_no, expiry_date, status) VALUES
(6, NOW() - INTERVAL 120 DAY, 500.00, '4111111111111111', '2028-12-01', 'Pending'); -- Charlie's old order

-- Customer with EXPIRED card for testing (expiry in the past)
INSERT INTO Users (username, password, first_name, last_name, email, phone_number, shipping_address, role) VALUES
('expired_card_user', '$2b$12$L7uViO83dThWjwvY3o4A0ubXAJpqyH4CJBqP4nnL3rdHrPbskZ.ku', 'Expired', 'Card', 'expired@email.com', '+1-555-0000', 'Expired St', 'customer');

-- Add item to expired_card_user's cart for checkout testing
INSERT INTO Shopping_Cart (user_id, isbn, quantity) VALUES
(8, '978-0-545-01022-1', 1);

-- Very expensive book (for high total testing)
INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold) VALUES
('978-0-EXPENSIVE1', 'Rare Collector Edition', 5, 2015, 999.99, 'Art', 5, 2);
INSERT INTO Book_Authors (isbn, author_id) VALUES ('978-0-EXPENSIVE1', 1);

-- Very cheap book (for low total testing)
INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold) VALUES
('978-0-CHEAPBOOK1', 'Budget Read', 1, 2023, 1.99, 'Geography', 100, 20);
INSERT INTO Book_Authors (isbn, author_id) VALUES ('978-0-CHEAPBOOK1', 10);

-- =============================================
-- VERIFICATION QUERIES (Optional - for testing)
-- =============================================

-- Check total books
SELECT COUNT(*) as total_books FROM Books;

-- Check total users
SELECT COUNT(*) as total_users FROM Users;

-- Check cart contents
SELECT u.username, b.title, sc.quantity
FROM Shopping_Cart sc
JOIN Users u ON sc.user_id = u.user_id
JOIN Books b ON sc.isbn = b.isbn;

-- Check orders
SELECT u.username, co.order_date, co.total_price
FROM Customer_Orders co
JOIN Users u ON co.user_id = u.user_id
ORDER BY co.order_date DESC;

-- Check low stock books (should trigger publisher orders)
SELECT isbn, title, stock, threshold FROM Books WHERE stock <= threshold;

-- Check books with multiple authors
SELECT b.isbn, b.title, GROUP_CONCAT(a.author_name SEPARATOR ', ') as authors
FROM Books b
JOIN Book_Authors ba ON b.isbn = ba.isbn
JOIN Authors a ON ba.author_id = a.author_id
GROUP BY b.isbn
HAVING COUNT(a.author_id) > 1;
