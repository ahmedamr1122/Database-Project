# Online Bookstore Project Setup and Testing Guide

## Project Structure

```
project-root/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── book.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── publisher.py
│   │   └── user.py
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── customer.py
│   │   └── shared.py
│   └── utils/
│       ├── auth_decorators.py
│       └── validators.py
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   ├── Navbar.js
│   │   │   ├── Register.js
│   │   │   ├── admin/
│   │   │   │   ├── AddBook.js
│   │   │   │   └── Dashboard.js
│   │   │   └── customer/
│   │   │       ├── Cart.js
│   │   │       ├── Dashboard.js
│   │   │       ├── Orders.js
│   │   │       ├── Profile.js
│   │   │       └── SearchBooks.js
│   │   └── context/
│   │       └── AuthContext.js
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── images/
│   │   └── js/
│   │       ├── admin.js
│   │       ├── customer.js
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── admin/
│       │   ├── add_book.html
│       │   ├── dashboard.html
│       │   ├── modify_book.html
│       │   ├── orders.html
│       │   └── reports.html
│       └── customer/
│           ├── cart.html
│           ├── checkout.html
│           ├── dashouboard.html
│           ├── orders.html
│           ├── profile.html
│           └── search.html
├── db.sql
├── file-structure.md
├── preview.py
└── TODO.md
```

## How to Run the Project

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-here
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your-mysql-password
   DB_NAME=OnlineBookstore
   DEBUG=True
   CORS_ORIGINS=http://localhost:3000
   ```

5. **Set up database:**
   - Ensure MySQL is running
   - Create database: `CREATE DATABASE OnlineBookstore;`
   - Run the SQL script:
     ```bash
     mysql -u root -p OnlineBookstore < ../db.sql
     ```

6. **Run the backend:**
   ```bash
   python app.py
   ```
   The backend will be available at http://localhost:5000

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the frontend:**
   ```bash
   npm start
   ```
   The frontend will be available at http://localhost:3000

## Testing the Project

### Backend API Testing

#### Using Postman

1. **Import API Collection:**
   - Create a new collection called "Online Bookstore API"
   - Set base URL to `http://localhost:5000/api`

2. **Authentication Endpoints:**

   **Register User:**
   - Method: POST
   - URL: `/auth/register`
   - Body (JSON):
     ```json
     {
       "username": "testuser",
       "password": "password123",
       "first_name": "Test",
       "last_name": "User",
       "email": "test@example.com",
       "phone_number": "1234567890",
       "shipping_address": "123 Test St"
     }
     ```

   **Login:**
   - Method: POST
   - URL: `/auth/login`
   - Body (JSON):
     ```json
     {
       "username": "testuser",
       "password": "password123"
     }
     ```
   - Save the returned token for authenticated requests

3. **Book Management (Admin):**

   **Add Book:**
   - Method: POST
   - URL: `/admin/books`
   - Headers: `Authorization: Bearer <token>`
   - Body (JSON):
     ```json
     {
       "isbn": "9781234567890",
       "title": "Test Book",
       "publisher_name": "Test Publisher",
       "selling_price": 29.99,
       "category": "Fiction",
       "stock": 100,
       "threshold": 10,
       "authors": ["Test Author"]
     }
     ```

4. **Shared Endpoints:**

   **Search Books:**
   - Method: GET
   - URL: `/shared/books/search?title=test`

5. **Customer Endpoints:**

   **Get Cart:**
   - Method: GET
   - URL: `/customer/cart`
   - Headers: `Authorization: Bearer <token>`

   **Add to Cart:**
   - Method: POST
   - URL: `/customer/cart`
   - Headers: `Authorization: Bearer <token>`
   - Body (JSON):
     ```json
     {
       "isbn": "9781234567890",
       "quantity": 1
     }
     ```

### Frontend Testing

1. **User Registration:**
   - Navigate to http://localhost:3000
   - Click "Register"
   - Fill in registration form
   - Verify account creation

2. **User Login:**
   - Use registered credentials to login
   - Verify dashboard access based on role

3. **Book Search (Customer):**
   - Login as customer
   - Navigate to Search Books
   - Search for books by title, author, or category
   - Verify search results

4. **Cart Management:**
   - Add books to cart
   - Update quantities
   - Remove items
   - Verify cart total calculation

5. **Order Placement:**
   - Proceed to checkout
   - Place order
   - Verify order creation and stock reduction

6. **Admin Functions:**
   - Login as admin
   - Add new books
   - View pending orders
   - Generate reports

### Integration Testing

1. **Complete User Flow:**
   - Register -> Login -> Search -> Add to Cart -> Checkout -> View Orders

2. **Admin Workflow:**
   - Login as Admin -> Add Books -> View Orders -> Confirm Orders -> Generate Reports

3. **Cross-browser Testing:**
   - Test on Chrome, Firefox, Safari
   - Verify responsive design on mobile devices

### Performance Testing

1. **Load Testing:**
   - Use tools like Apache JMeter or Locust
   - Test concurrent users accessing the application

2. **Database Performance:**
   - Monitor query execution times
   - Check for N+1 query problems

### Security Testing

1. **Authentication:**
   - Test invalid login attempts
   - Verify JWT token expiration
   - Test unauthorized access attempts

2. **Input Validation:**
   - Test SQL injection attempts
   - Verify input sanitization
   - Test XSS prevention

## Troubleshooting

### Common Issues

1. **Module Not Found Errors:**
   - Ensure all dependencies are installed
   - Check virtual environment activation

2. **Database Connection Errors:**
   - Verify MySQL is running
   - Check database credentials in .env
   - Ensure database and tables are created

3. **CORS Errors:**
   - Check CORS_ORIGINS in .env file
   - Ensure backend allows frontend origin

4. **Port Conflicts:**
   - Change ports if 3000 or 5000 are in use
   - Update CORS settings accordingly

### Logs and Debugging

- Backend logs are printed to console
- Frontend errors appear in browser console
- Check MySQL error logs for database issues

## Deployment

### Production Setup

1. **Environment Variables:**
   - Set DEBUG=False
   - Use strong SECRET_KEY and JWT_SECRET_KEY
   - Configure production database

2. **Web Server:**
   - Use Gunicorn for Flask
   - Configure Nginx as reverse proxy

3. **Database:**
   - Use production MySQL instance
   - Set up backups and monitoring

4. **Frontend Build:**
   - Run `npm run build`
   - Serve static files with web server

This guide provides comprehensive instructions for setting up, running, and testing the Online Bookstore project. Follow the steps in order for successful deployment and testing.
