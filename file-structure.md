# Online Bookstore - Complete Project Structure

```
online-bookstore/
│
├── backend/
│   ├── app.py                      # Main Flask application entry point
│   ├── config.py                   # Database and app configuration
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.sql                  # Schema + triggers (your existing file)
│   │   ├── seed_data.sql           # Sample data for testing
│   │   └── connection.py           # Database connection handler
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User model (auth, registration)
│   │   ├── book.py                 # Book CRUD operations
│   │   ├── cart.py                 # Shopping cart operations
│   │   ├── order.py                # Customer orders management
│   │   └── publisher.py            # Publisher orders & operations
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Login, Register, Logout
│   │   ├── admin.py                # Admin-only operations
│   │   ├── customer.py             # Customer operations
│   │   └── shared.py               # Search books (both roles)
│   │
│   └── utils/
│       ├── __init__.py
│       ├── auth_decorators.py      # @login_required, @admin_required
│       └── validators.py           # Input validation functions
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Main stylesheet
│   │   ├── js/
│   │   │   ├── main.js             # Common functions
│   │   │   ├── admin.js            # Admin-specific JS
│   │   │   └── customer.js         # Customer-specific JS
│   │   └── images/
│   │       └── logo.png
│   │
│   └── templates/
│       ├── base.html               # Base template (header/footer)
│       ├── index.html              # Landing page
│       ├── login.html              # Login page
│       ├── register.html           # Registration page
│       │
│       ├── admin/
│       │   ├── dashboard.html      # Admin home
│       │   ├── add_book.html       # Add new book
│       │   ├── modify_book.html    # Edit/update books
│       │   ├── orders.html         # Confirm publisher orders
│       │   └── reports.html        # Generate reports
│       │
│       └── customer/
│           ├── dashboard.html      # Customer home
│           ├── search.html         # Search books
│           ├── cart.html           # View/manage cart
│           ├── checkout.html       # Checkout process
│           ├── orders.html         # View past orders
│           └── profile.html        # Edit personal info
│
├── .env                            # Environment variables (DB password, secret key)
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation

```

## File Descriptions

### Backend Core Files

**`backend/app.py`** - Main Flask application
- Initializes Flask app
- Registers all blueprints (routes)
- Configures session management
- Starts the server

**`backend/config.py`** - Configuration settings
- Database credentials (from .env)
- Flask secret key
- Session configuration

**`backend/requirements.txt`** - Python dependencies
```
Flask==3.0.0
mysql-connector-python==8.2.0
python-dotenv==1.0.0
bcrypt==4.1.1
```

### Database Files

**`database/connection.py`** - Database connection manager
- Establishes MySQL connection
- Connection pooling
- Query execution helper functions

**`database/db.sql`** - Your existing schema
- All tables, triggers, and constraints

**`database/seed_data.sql`** - Sample data
- Publishers, books, users (admin + customers)
- Sample orders for testing reports

### Models (Business Logic Layer)

**`models/user.py`**
- `register_user()` - Create new customer account
- `login()` - Authenticate user
- `update_profile()` - Edit personal info
- `get_user_by_id()` - Fetch user details

**`models/book.py`**
- `add_book()` - Admin adds new book
- `update_book()` - Admin modifies book
- `search_books()` - Search by ISBN, title, author, category, publisher
- `get_book_details()` - Get specific book info

**`models/cart.py`**
- `add_to_cart()` - Add book to user's cart
- `get_cart_items()` - Retrieve cart contents
- `remove_from_cart()` - Remove item
- `clear_cart()` - Empty cart (on logout/checkout)

**`models/order.py`**
- `create_order()` - Process checkout
- `get_user_orders()` - Fetch customer's past orders
- `get_order_details()` - Get specific order info

**`models/publisher.py`**
- `get_pending_orders()` - Get orders awaiting confirmation
- `confirm_order()` - Mark order as confirmed (triggers stock update)
- `get_replenishment_count()` - Count orders for specific book
- `generate_reports()` - All admin reports

### Routes (API Endpoints)

**`routes/auth.py`**
- `POST /login` - User login
- `POST /register` - New customer registration
- `POST /logout` - Logout (clears cart)

**`routes/admin.py`**
- `POST /admin/books` - Add new book
- `PUT /admin/books/<isbn>` - Update book
- `GET /admin/orders/pending` - View pending publisher orders
- `POST /admin/orders/<id>/confirm` - Confirm order
- `GET /admin/reports/sales-month` - Monthly sales
- `GET /admin/reports/sales-day` - Daily sales
- `GET /admin/reports/top-customers` - Top 5 customers
- `GET /admin/reports/top-books` - Top 10 books
- `GET /admin/reports/replenishment/<isbn>` - Replenishment count

**`routes/customer.py`**
- `POST /cart/add` - Add to cart
- `GET /cart` - View cart
- `DELETE /cart/<isbn>` - Remove from cart
- `POST /checkout` - Complete purchase
- `GET /orders` - View past orders
- `PUT /profile` - Update personal info

**`routes/shared.py`**
- `GET /books/search` - Search books (any user)
- `GET /books/<isbn>` - Get book details

### Utils (Helper Functions)

**`utils/auth_decorators.py`**
```python
@login_required      # Ensures user is logged in
@admin_required      # Ensures user is admin
```

**`utils/validators.py`**
- `validate_isbn()` - Check ISBN format
- `validate_email()` - Check email format
- `validate_credit_card()` - Check credit card number
- `validate_expiry_date()` - Check if card is not expired

### Frontend

**`templates/base.html`** - Base template
- Common header with navigation
- Footer
- Include CSS/JS files

**Admin Pages:**
- Dashboard: Quick stats, navigation menu
- Add Book: Form with all book fields + threshold
- Modify Book: Search book, then edit form
- Orders: Table of pending orders with "Confirm" buttons
- Reports: Forms to select date/parameters, display results

**Customer Pages:**
- Dashboard: Welcome message, featured books
- Search: Search form + results table
- Cart: List items, quantities, prices, total
- Checkout: Credit card form
- Orders: Past orders history
- Profile: Edit form (username, email, password, etc.)

## Environment Variables (.env)

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=OnlineBookstore
SECRET_KEY=your_secret_key_here
```

## .gitignore

```
.env
__pycache__/
*.pyc
*.pyo
.DS_Store
venv/
*.log
```

## Team Member Roles Suggestion

**Member 1: Database & Authentication**
- Setup database (db.sql, seed_data.sql)
- Connection handler
- User model + auth routes
- Login/Register pages

**Member 2: Admin Features**
- Book model (add/update)
- Admin routes
- Publisher model
- Admin pages (add/modify books, orders, reports)

**Member 3: Customer Features**
- Cart model
- Order model
- Customer routes
- Customer pages (cart, checkout, orders, profile)

**Member 4: Search & Frontend Integration**
- Search functionality (shared routes)
- CSS styling
- JavaScript functionality
- Testing & bug fixes

## Next Steps

1. Create the directory structure
2. Set up virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file with database credentials
5. Run `db.sql` to create schema
6. Run `seed_data.sql` to populate test data
7. Start development on assigned modules
8. Integrate and test together

Would you like me to generate starter code for any specific file?