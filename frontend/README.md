# Online Bookstore - Frontend Documentation

## 📁 Frontend Structure Overview

```
frontend/
├── static/
│   ├── css/
│   │   └── style.css              # Main stylesheet
│   ├── js/
│   │   ├── main.js                # Common functions for all pages
│   │   ├── admin.js               # Admin-specific functions
│   │   └── customer.js            # Customer-specific functions
│   └── images/
│       └── logo.png               # (Add your logo here)
│
└── templates/
    ├── base.html                  # Base template (navigation, footer)
    ├── index.html                 # Landing page
    ├── login.html                 # Login page
    ├── register.html              # Registration page
    │
    ├── admin/
    │   ├── dashboard.html         # Admin dashboard
    │   ├── add_book.html          # Add new book
    │   ├── modify_book.html       # Search & modify books
    │   ├── orders.html            # Manage publisher orders
    │   └── reports.html           # Generate reports
    │
    └── customer/
        ├── dashboard.html         # Customer home
        ├── search.html            # Search books
        ├── cart.html              # Shopping cart
        ├── checkout.html          # Checkout process
        ├── orders.html            # View past orders
        └── profile.html           # Edit profile
```

---

## 📄 Template Files Description

### **Common Templates**

#### `base.html`
- **Purpose**: Base template that all other pages extend
- **Features**:
  - Navigation bar (changes based on user role)
  - Flash message display
  - Footer
  - Loads Bootstrap 5, Font Awesome, and custom CSS/JS
  - Cart count badge (for customers)

#### `index.html`
- **Purpose**: Landing page
- **Features**:
  - Hero section with welcome message
  - Quick action buttons (Login/Register or Dashboard)
  - Feature cards (Wide Selection, Fast Delivery, Secure Payment)
  - Category badges

#### `login.html`
- **Purpose**: User login
- **Form Fields**:
  - Username
  - Password
- **Actions**: Submit to `/login` endpoint

#### `register.html`
- **Purpose**: New customer registration
- **Form Fields**:
  - First Name, Last Name
  - Username
  - Email
  - Phone Number
  - Shipping Address
  - Password, Confirm Password
- **Client-side Validation**: Password matching
- **Actions**: Submit to `/register` endpoint

### **Admin Templates**

#### `admin/dashboard.html`
- **Purpose**: Admin home page
- **Features**:
  - Statistics cards (Total Books, Customers, Pending Orders, Monthly Sales)
  - Quick action buttons
  - Low stock alerts table
- **Required Backend Data**:
  ```python
  stats = {
      'total_books': int,
      'total_customers': int,
      'pending_orders': int,
      'monthly_sales': float
  }
  low_stock_books = [{'isbn', 'title', 'stock'}, ...]
  ```

#### `admin/add_book.html`
- **Purpose**: Add new books to inventory
- **Form Fields**:
  - ISBN (required, unique)
  - Title
  - Authors (comma-separated)
  - Publisher (dropdown)
  - Publication Year
  - Selling Price
  - Category (dropdown: Science, Art, Religion, History, Geography)
  - Initial Stock
  - Stock Threshold
- **Features**:
  - Add publisher modal
  - Form validation
  - ISBN format check
- **Actions**: Submit to `/admin/add-book`

#### `admin/modify_book.html`
- **Purpose**: Search and update existing books
- **Features**:
  - Search form (by ISBN or Title)
  - Search results table
  - Edit form (pre-filled with book data)
  - Stock level indicators
  - Cannot change ISBN (primary key)
- **Actions**: 
  - Search: GET `/admin/modify-book`
  - Update: POST `/admin/modify-book`

#### `admin/orders.html`
- **Purpose**: View and confirm publisher orders
- **Features**:
  - Pending orders table with "Confirm" buttons
  - Recently confirmed orders table
  - Order statistics cards
- **Actions**: 
  - Confirm: POST `/admin/orders/{id}/confirm`
- **Required Backend Data**:
  ```python
  pending_orders = [{'po_id', 'isbn', 'book_title', 'publisher_name', 'quantity', 'order_date'}, ...]
  confirmed_orders = [same structure]
  stats = {'total_orders', 'pending_count', 'confirmed_count'}
  ```

#### `admin/reports.html`
- **Purpose**: Generate various business reports
- **Report Types**:
  1. **Previous Month Sales**: Total revenue from last month
  2. **Specific Day Sales**: Revenue for selected date
  3. **Top 5 Customers**: Last 3 months, by total spent
  4. **Top 10 Books**: Last 3 months, by copies sold
  5. **Replenishment Count**: Times a book was reordered
- **Actions**:
  - POST `/admin/reports/sales-month`
  - POST `/admin/reports/sales-day`
  - POST `/admin/reports/top-customers`
  - POST `/admin/reports/top-books`
  - POST `/admin/reports/replenishment`

### **Customer Templates**

#### `customer/dashboard.html`
- **Purpose**: Customer home page
- **Features**:
  - Welcome message
  - Quick action cards (Search, Cart, Orders, Profile)
  - Browse by category links
  - Recent orders table (if any)
- **Required Backend Data**:
  ```python
  cart_count = int
  recent_orders = [{'order_id', 'order_date', 'total_price'}, ...]
  ```

#### `customer/search.html`
- **Purpose**: Search for books
- **Search Filters**:
  - ISBN
  - Title
  - Author
  - Category (dropdown)
  - Publisher
- **Features**:
  - Search results displayed as cards
  - Shows book details, price, stock status
  - "Add to Cart" button with quantity selector
  - Disabled button for out-of-stock items
- **Actions**: 
  - Search: GET `/customer/search`
  - Add to Cart: POST `/customer/cart/add`

#### `customer/cart.html`
- **Purpose**: View and manage shopping cart
- **Features**:
  - Cart items table
  - Quantity update (auto-submit on change)
  - Remove item button
  - Order summary (subtotal, shipping, total)
  - Clear cart button
  - Proceed to checkout button
- **Actions**:
  - Update: POST `/customer/cart/update`
  - Remove: POST `/customer/cart/remove`
  - Clear: POST `/customer/cart/clear`

#### `customer/checkout.html`
- **Purpose**: Complete purchase
- **Features**:
  - Order review (items, quantities, prices)
  - Shipping address display
  - Payment form:
    - Credit Card Number (16 digits)
    - Expiry Month/Year (dropdowns)
    - CVV (3 digits)
    - Cardholder Name
  - Terms & conditions checkbox
  - Client-side validation
- **Validation**:
  - Card number format (16 digits, no spaces)
  - Expiry date (not in past)
  - CVV format (3 digits)
- **Actions**: POST `/customer/checkout`

#### `customer/orders.html`
- **Purpose**: View past orders
- **Features**:
  - Order cards with full details
  - Order items table
  - Payment info (last 4 digits)
  - Shipping address
  - Order summary
- **Required Backend Data**:
  ```python
  orders = [{
      'order_id': int,
      'order_date': datetime,
      'total_price': float,
      'credit_card_no': str,
      'expiry_date': date,
      'total_items': int,
      'items': [{'isbn', 'title', 'authors', 'quantity', 'unit_price'}, ...]
  }, ...]
  ```

#### `customer/profile.html`
- **Purpose**: Edit personal information
- **Form Fields**:
  - First Name, Last Name
  - Username
  - Email
  - Phone Number
  - Shipping Address
  - Change Password section (optional):
    - Current Password
    - New Password
    - Confirm New Password
- **Features**:
  - Account info sidebar
  - Account statistics
  - Password change validation
- **Actions**: POST `/customer/profile`

## 🎨 CSS Styling (style.css)

### **Key Features**:
- Bootstrap 5 as base framework
- Custom color scheme using CSS variables
- Responsive design
- Hover effects on cards and buttons
- Smooth transitions and animations
- Print-friendly styles

### **Main Components**:
1. **Hero Section**: Gradient background for landing page
2. **Cards**: Shadow effects with hover animations
3. **Navigation**: Fixed top navbar with role-based links
4. **Tables**: Hover effects for better UX
5. **Buttons**: Consistent styling with hover effects
6. **Badges**: Color-coded status indicators

## 📜 JavaScript Files

### **main.js** (Common Functions)

**Key Functions**:
- `initializeApp()` - Initialize on page load
- `updateCartCount()` - Fetch and update cart badge
- `showAlert(message, type)` - Display Bootstrap alerts
- `validateForm(formId)` - Basic form validation
- `showLoading(element)` / `hideLoading(element)` - Loading spinners
- `formatCurrency(amount)` - Format prices
- `fetchAPI(url, options)` - API call wrapper

### **admin.js** (Admin Functions)

**Key Functions**:
- `validateAddBookForm(e)` - Validate add book form
- `validateModifyBookForm(e)` - Validate modify book form
- `isValidISBN(isbn)` - Check ISBN format
- `addPublisher()` - Add new publisher via modal
- `confirmOrder(orderId)` - Confirm publisher order
- `generateReport(type, params)` - Generate reports
- `checkStockLevel(stock, threshold)` - Check stock status
- `exportReportToCSV(data, filename)` - Export reports

### **customer.js** (Customer Functions)

**Key Functions**:
- `handleAddToCart(e)` - Add book to cart
- `validateQuantity(e)` - Check quantity limits
- `updateCartCount()` - Update cart badge
- `removeFromCart(isbn)` - Remove item from cart
- `clearCart()` - Empty entire cart
- `validateCheckoutForm(e)` - Validate checkout form
- `formatCreditCardInput(e)` - Format card number
- `formatCVVInput(e)` - Format CVV
- `validateProfileForm(e)` - Validate profile update

## 🔗 Flask Backend Integration

### **Required Flask Routes**:

```python
# Authentication
POST /login
POST /register
GET  /logout

# Admin Routes
GET  /admin/dashboard
GET  /admin/add-book
POST /admin/add-book
GET  /admin/modify-book
POST /admin/modify-book
GET  /admin/orders
POST /admin/orders/<id>/confirm
GET  /admin/reports
POST /admin/reports/sales-month
POST /admin/reports/sales-day
POST /admin/reports/top-customers
POST /admin/reports/top-books
POST /admin/reports/replenishment
POST /admin/publishers/add

# Customer Routes
GET  /customer/dashboard
GET  /customer/search
POST /customer/cart/add
GET  /customer/cart
POST /customer/cart/update
POST /customer/cart/remove
POST /customer/cart/clear
GET  /customer/cart/count
GET  /customer/checkout
POST /customer/checkout
GET  /customer/orders
GET  /customer/profile
POST /customer/profile
```

### **Session Variables Required**:
```python
session['user_id']
session['username']
session['role']  # 'admin' or 'customer'
session['first_name']
session['last_name']
session['shipping_address']
```

## 🛠️ Setup Instructions

1. **Place Files**:
   - Put all HTML files in `templates/` folder
   - Put CSS file in `static/css/`
   - Put JS files in `static/js/`

2. **Flask Configuration**:
   ```python
   from flask import Flask, render_template
   
   app = Flask(__name__)
   app.secret_key = 'your-secret-key'
   
   @app.route('/')
   def index():
       return render_template('index.html')
   ```

3. **Dependencies**:
   - Bootstrap 5 (CDN)
   - Font Awesome 6 (CDN)
   - No additional npm packages needed


## ✅ Features Checklist

### Admin Features:
- ✅ Add new books with validation
- ✅ Modify existing books
- ✅ View and confirm publisher orders
- ✅ Generate 5 types of reports
- ✅ Low stock alerts
- ✅ Dashboard with statistics

### Customer Features:
- ✅ Register and login
- ✅ Search books (multiple criteria)
- ✅ Add to cart with quantity
- ✅ View and manage cart
- ✅ Checkout with credit card validation
- ✅ View past orders
- ✅ Edit profile and password

### Security:
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ Client-side validation
- ✅ CSRF protection (Flask-WTF recommended)
- ✅ Password confirmation

## 📱 Responsive Design

All pages are mobile-friendly using Bootstrap 5's responsive grid system:
- Mobile (< 768px): Single column layout
- Tablet (768px - 992px): 2-column layout
- Desktop (> 992px): Full layout


## 🎯 Next Steps

1. Connect templates to Flask backend
2. Implement all route handlers
3. Add database queries
4. Test all features
5. Add error handling
6. Implement CSRF protection
7. Add loading states
8. Test on different browsers

---

## 📝 Notes

- All forms use POST method for security
- Flash messages are automatically displayed
- Cart count updates dynamically
- Triggers in database handle auto-ordering
- Credit card validation is basic (for demo purposes)
- Real production app would need stronger security

---

## 🤝 Team Collaboration

**Suggested Division**:
- **Member 1**: Authentication pages (login, register, base.html)
- **Member 2**: Admin pages (dashboard, add/modify books, orders)
- **Member 3**: Customer pages (search, cart, checkout)
- **Member 4**: Reports page, CSS/JS, testing

Each member should work on their assigned templates and corresponding Flask routes.

---



Here is the optimized documentation, refined for clarity and technical precision within the specified character limit.

---

# Online Bookstore - Frontend Documentation

## 📁 Frontend Structure Overview

```text
frontend/
├── static/
│   ├── css/
│   │   └── style.css            # Main stylesheet (Bootstrap overrides)
│   ├── js/
│   │   ├── main.js              # Common utilities
│   │   ├── admin.js             # Admin logic (reports, stock)
│   │   └── customer.js          # Customer logic (cart, checkout)
│   └── images/
│       └── logo.png
│
└── templates/
    ├── base.html                # Master layout
    ├── index.html               # Landing page
    ├── login.html               # Auth: Login
    ├── register.html            # Auth: Registration
    │
    ├── admin/
    │   ├── dashboard.html       # Admin home & stats
    │   ├── add_book.html        # Inventory entry
    │   ├── modify_book.html     # Inventory update
    │   ├── orders.html          # Publisher order management
    │   └── reports.html         # Analytics interface
    │
    └── customer/
        ├── dashboard.html       # User home
        ├── search.html          # Book catalog & filters
        ├── cart.html            # Shopping cart
        ├── checkout.html        # Payment processing
        ├── orders.html          # History view
        └── profile.html         # Account settings

```

