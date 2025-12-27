# 📚 Online Bookstore - Complete Project Documentation

## Overview

This is a full-stack web application for an Online Bookstore built as a Database Systems project. It features:

- **Backend**: Python Flask with MySQL database
- **Frontend**: HTML/CSS/JavaScript with Bootstrap 5
- **Architecture**: Server-Side Rendering (SSR)

---

## 🗄️ Database Schema (SQL)

### Tables

#### 1. Publishers

Stores book publisher information.

```sql
CREATE TABLE Publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    address TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);
```

#### 2. Authors

Stores author names (separate from books for many-to-many relationship).

```sql
CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL
);
```

#### 3. Books

Core book catalog with inventory tracking.

```sql
CREATE TABLE Books (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    publisher_id INT NOT NULL,
    pub_year INT,
    selling_price DECIMAL(10, 2) NOT NULL,
    category ENUM('Science', 'Art', 'Religion', 'History', 'Geography') NOT NULL,
    stock INT DEFAULT 0,
    threshold INT DEFAULT 10,  -- Triggers auto-order when stock falls below
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
);
```

#### 4. Book_Authors (Bridge Table)

Handles the **many-to-many** relationship between books and authors.

```sql
CREATE TABLE Book_Authors (
    isbn VARCHAR(20),
    author_id INT,
    PRIMARY KEY (isbn, author_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE
);
```

**Why?** A book can have multiple authors, and an author can write multiple books.

#### 5. Users

Both admins and customers share this table (role-based access).

```sql
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Bcrypt hashed
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    shipping_address TEXT,
    role ENUM('admin', 'customer') DEFAULT 'customer'
);
```

#### 6. Shopping_Cart

Temporary storage for items users want to buy.

```sql
CREATE TABLE Shopping_Cart (
    user_id INT,
    isbn VARCHAR(20),
    quantity INT NOT NULL DEFAULT 1,
    PRIMARY KEY (user_id, isbn),  -- Composite key = one row per user-book pair
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (isbn) REFERENCES Books(isbn) ON DELETE CASCADE
);
```

#### 7. Customer_Orders (Order Header)

Records completed purchases.

```sql
CREATE TABLE Customer_Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2),
    credit_card_no VARCHAR(16) NOT NULL,
    expiry_date DATE NOT NULL,
    status ENUM('Pending', 'Confirmed') DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
```

#### 8. Order_Items (Order Details)

Items within each order (one order → many items).

```sql
CREATE TABLE Order_Items (
    order_id INT,
    isbn VARCHAR(20),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,  -- Snapshot at time of purchase
    PRIMARY KEY (order_id, isbn),
    FOREIGN KEY (order_id) REFERENCES Customer_Orders(order_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);
```

#### 9. Publisher_Orders

Orders placed TO publishers to restock books.

```sql
CREATE TABLE Publisher_Orders (
    po_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20),
    publisher_id INT,
    quantity INT NOT NULL DEFAULT 50,
    order_date DATE DEFAULT (CURRENT_DATE),
    status ENUM('Pending', 'Confirmed') DEFAULT 'Pending',
    FOREIGN KEY (isbn) REFERENCES Books(isbn),
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
);
```

---

## ⚡ Database Triggers

### 1. Prevent Negative Stock

**When**: Before any UPDATE on Books  
**What**: Throws error if stock would go below 0

```sql
CREATE TRIGGER Prevent_Negative_Stock
BEFORE UPDATE ON Books
FOR EACH ROW
BEGIN
    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Stock cannot be negative.';
    END IF;
END;
```

### 2. Auto-Order from Publisher

**When**: After stock UPDATE that drops below threshold  
**What**: Automatically creates a Publisher_Order for 50 units

```sql
CREATE TRIGGER Auto_Order_Trigger
AFTER UPDATE ON Books
FOR EACH ROW
BEGIN
    IF NEW.stock < NEW.threshold AND OLD.stock >= NEW.threshold THEN
        INSERT INTO Publisher_Orders (isbn, publisher_id, quantity, status)
        VALUES (NEW.isbn, NEW.publisher_id, 50, 'Pending');
    END IF;
END;
```

### 3. Update Stock on Confirmation

**When**: Admin confirms a Publisher_Order  
**What**: Adds the quantity to book stock

```sql
CREATE TRIGGER Update_Stock_On_Confirmation
AFTER UPDATE ON Publisher_Orders
FOR EACH ROW
BEGIN
    IF OLD.status = 'Pending' AND NEW.status = 'Confirmed' THEN
        UPDATE Books SET stock = stock + NEW.quantity WHERE isbn = NEW.isbn;
    END IF;
END;
```

### 4. Deduct Stock on Purchase

**When**: New Order_Item inserted (customer checkout)  
**What**: Subtracts quantity from book stock

```sql
CREATE TRIGGER Deduct_Stock_On_Purchase
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    UPDATE Books SET stock = stock - NEW.quantity WHERE isbn = NEW.isbn;
END;
```

---

## 🔄 How the Checkout Flow Works

```
Customer Cart → Checkout POST → Order.create_order()
    ↓
1. Fetch cart items from Shopping_Cart
2. Calculate total price
3. INSERT into Customer_Orders (creates order_id)
4. For each cart item:
   - INSERT into Order_Items ← TRIGGERS Deduct_Stock_On_Purchase
5. DELETE from Shopping_Cart (clear cart)
6. COMMIT transaction
```

---

## 📊 Admin Reports (SQL Queries)

### Monthly Sales

```sql
SELECT SUM(total_price) FROM Customer_Orders
WHERE order_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
```

### Top 5 Customers (Last 3 Months)

```sql
SELECT u.username, SUM(co.total_price) as total_spent
FROM Users u
JOIN Customer_Orders co ON u.user_id = co.user_id
WHERE co.order_date >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
GROUP BY u.user_id
ORDER BY total_spent DESC
LIMIT 5;
```

### Top 10 Selling Books

```sql
SELECT b.isbn, b.title, SUM(oi.quantity) as copies_sold
FROM Books b
JOIN Order_Items oi ON b.isbn = oi.isbn
JOIN Customer_Orders co ON oi.order_id = co.order_id
WHERE co.order_date >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
GROUP BY b.isbn
ORDER BY copies_sold DESC
LIMIT 10;
```

---

## 🔐 Authentication & Security

- **Passwords**: Hashed using `bcrypt`
- **Sessions**: Flask session stores `user_id`, `role`, `username`
- **Route Protection**:
  - `@login_required` decorator for customer routes
  - `@admin_required` decorator for admin routes

---

## 📁 Project Structure

```
Database-Project/
├── backend/
│   ├── app.py              # Flask entry point
│   ├── config.py           # Environment config
│   ├── database/
│   │   ├── connection.py   # MySQL connection
│   │   ├── db.sql          # Schema + Triggers
│   │   └── seed_data.sql   # Test data
│   ├── models/
│   │   ├── book.py         # Book CRUD
│   │   ├── cart.py         # Shopping cart
│   │   ├── order.py        # Order processing
│   │   ├── publisher.py    # Publisher + Reports
│   │   └── user.py         # User auth + profile
│   ├── routes/
│   │   ├── admin.py        # Admin endpoints
│   │   ├── auth.py         # Login/Register
│   │   ├── customer.py     # Customer endpoints
│   │   └── shared.py       # API endpoints
│   └── utils/
│       ├── auth_decorators.py
│       └── validators.py
└── frontend/
    ├── templates/          # Jinja2 HTML
    └── static/
        ├── css/
        └── js/
```

---

## 🧪 Test Accounts

| Username     | Password    | Role                   |
| ------------ | ----------- | ---------------------- |
| admin        | password123 | Admin                  |
| john_doe     | password123 | Customer               |
| vip_customer | password123 | Customer (High Volume) |
