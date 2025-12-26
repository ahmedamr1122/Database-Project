# Online Bookstore Management System

## Overview
This is a comprehensive online bookstore management system built with Flask (backend) and React (frontend). The system serves both administrators and customers, providing a complete e-commerce solution for book sales with automated inventory management.

## Features

### Customer Features
- **User Registration & Authentication**: Secure signup and login with JWT tokens
- **Book Browsing & Search**: Search books by title, author, category, or publisher
- **Shopping Cart**: Add/remove items, update quantities, view cart summary
- **Secure Checkout**: Credit card validation and order placement
- **Order History**: View past orders and order details
- **Profile Management**: Update personal information and password

### Admin Features
- **Book Management**: Add new books with authors, publishers, and categories
- **Book Modification**: Update book details, stock levels, and pricing
- **Inventory Control**: Automatic low-stock alerts and publisher order management
- **Order Processing**: Confirm publisher orders to restock inventory
- **Sales Reports**: Generate monthly/daily sales, top customers, top books, and replenishment reports

### System Features
- **Automated Inventory**: Triggers prevent negative stock and auto-generate publisher orders
- **Data Integrity**: Comprehensive constraints and validation
- **Role-Based Access**: Separate admin and customer interfaces
- **Responsive Design**: Bootstrap-based UI for all devices

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: MySQL (with SQLite fallback for development)
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Custom validators for ISBN, email, credit cards
- **ORM**: Raw SQL queries with connection pooling

### Frontend
- **Framework**: React 18
- **Routing**: React Router
- **State Management**: React Context API
- **Styling**: Bootstrap 5
- **HTTP Client**: Fetch API

## Database Schema

### Core Tables
- **Users**: Customer and admin accounts
- **Books**: Book catalog with pricing and inventory
- **Authors**: Author information (many-to-many with books)
- **Publishers**: Publisher details
- **Shopping_Cart**: Customer cart items
- **Customer_Orders**: Order headers
- **Order_Items**: Order line items
- **Publisher_Orders**: Automated restocking orders

### Key Relationships
- Books ↔ Authors (Many-to-Many)
- Books → Publishers (Many-to-One)
- Users → Shopping_Cart (One-to-Many)
- Users → Customer_Orders (One-to-Many)
- Customer_Orders → Order_Items (One-to-Many)

## Business Logic & Triggers

### Automated Processes
1. **Stock Prevention**: Triggers prevent stock from going negative
2. **Auto-Reordering**: Low stock triggers automatic publisher orders
3. **Stock Updates**: Confirmed publisher orders update book inventory
4. **Order Processing**: Customer purchases deduct from stock

### Validation Rules
- ISBN format validation
- Credit card number and expiry validation
- Email format checking
- Password strength requirements
- Stock quantity constraints

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 8.0+ (or SQLite for development)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Database Setup
```bash
# Create database
mysql -u root -p < backend/database/db.sql

# Populate sample data
mysql -u root -p OnlineBookstore < backend/database/seed_data.sql
```

### Environment Configuration
Create a `.env` file in the root directory:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=OnlineBookstore
SECRET_KEY=your_secret_key_here
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Running the Application
```bash
# Backend (in one terminal)
cd backend
python app.py

# Frontend (in another terminal)
cd frontend
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Customer Operations
- `GET /api/customer/cart` - Get cart items
- `POST /api/customer/cart` - Add to cart
- `PUT /api/customer/cart/<isbn>` - Update cart item
- `DELETE /api/customer/cart/<isbn>` - Remove from cart
- `DELETE /api/customer/cart` - Clear cart
- `GET /api/customer/orders` - Get order history
- `POST /api/customer/orders` - Place order
- `GET /api/customer/orders/<id>` - Get order details
- `GET /api/customer/profile` - Get user profile
- `PUT /api/customer/profile` - Update profile

### Admin Operations
- `POST /api/admin/books` - Add new book
- `PUT /api/admin/books/<isbn>` - Update book
- `GET /api/admin/orders/pending` - Get pending publisher orders
- `POST /api/admin/orders/<id>/confirm` - Confirm publisher order
- `GET /api/admin/reports/sales-month` - Monthly sales report
- `POST /api/admin/reports/sales-day` - Daily sales report
- `GET /api/admin/reports/top-customers` - Top customers report
- `GET /api/admin/reports/top-books` - Top books report
- `GET /api/admin/reports/replenishment/<isbn>` - Replenishment count

### Shared Operations
- `GET /api/shared/books/search` - Search books
- `GET /api/shared/books/<isbn>` - Get book details

## Testing Accounts

### Admin Account
- Username: `admin`
- Password: `password123`

### Sample Customer Accounts
- Username: `john_doe`, Password: `password123`
- Username: `jane_smith`, Password: `password123`
- Username: `bob_wilson`, Password: `password123`

## Project Structure

```
online-bookstore/
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py             # Configuration
│   ├── requirements.txt      # Python dependencies
│   ├── database/
│   │   ├── db.sql           # Database schema
│   │   ├── seed_data.sql    # Sample data
│   │   └── connection.py    # DB connection
│   ├── models/              # Business logic
│   ├── routes/              # API endpoints
│   └── utils/               # Helpers & decorators
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # React context
│   │   └── App.js          # Main app component
│   ├── static/              # Static assets
│   └── templates/           # Flask templates (fallback)
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Development Notes

### Database Considerations
- Primary database is MySQL as per project requirements
- SQLite is used as fallback for development environments
- All triggers and constraints are implemented for data integrity

### Security Features
- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- Input validation and sanitization

### UI/UX Considerations
- Responsive design for mobile and desktop
- Intuitive navigation for both admin and customer roles
- Clear error messages and loading states
- Bootstrap components for consistent styling

## Future Enhancements
- Email notifications for order confirmations
- Advanced search with filters and sorting
- Wishlist functionality
- Review and rating system
- Payment gateway integration
- Multi-language support
- API documentation with Swagger

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License
This project is developed for educational purposes as part of a database systems course.
