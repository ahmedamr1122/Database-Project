from flask import Flask, render_template, session, request

# Point to your specific folders
app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

app.secret_key = 'preview_key'

# --- 1. Fake Data (Mocking the Database) ---
MOCK_BOOKS = [
    {'isbn': '978-01', 'title': 'The Great Gatsby', 'authors': 'F. Scott Fitzgerald', 'selling_price': 15.99, 'stock': 5, 'category': 'History', 'publisher_name': 'Penguin'},
    {'isbn': '978-02', 'title': 'Clean Code', 'authors': 'Robert C. Martin', 'selling_price': 45.50, 'stock': 0, 'category': 'Science', 'publisher_name': 'O Reilly'},
    {'isbn': '978-03', 'title': 'Design Patterns', 'authors': 'Gang of Four', 'selling_price': 55.00, 'stock': 12, 'category': 'Science', 'publisher_name': 'Pearson'},
]

MOCK_STATS = {
    'total_books': 120,
    'total_customers': 45,
    'pending_orders': 3,
    'monthly_sales': 1250.00
}

# --- 2. Context Processor (Makes 'session' available everywhere) ---
@app.context_processor
def inject_user():
    # You can change 'role' to 'admin' to see the admin dashboard!
    return dict(session=session)

# --- 3. Routes (The Pages) ---

@app.route('/')
def index():
    # Force a fake login for preview purposes if not set
    if 'user_id' not in session:
        session['user_id'] = 1
        session['username'] = 'preview_user'
        session['role'] = 'customer' # Change to 'admin' to test admin views
        session['first_name'] = 'Ahmed'
        session['shipping_address'] = '123 Fake St, Cairo'
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# --- Customer Routes ---
@app.route('/customer/dashboard')
def customer_dash():
    return render_template('customer/dashouboard.html', # Note: Your file has a typo 'dashouboard.html'
                         cart_count=2,
                         recent_orders=[{'order_id': 101, 'order_date': '2023-10-15', 'total_price': 45.99}])

@app.route('/customer/search')
def search():
    return render_template('customer/search.html', books=MOCK_BOOKS)

@app.route('/customer/cart')
def cart():
    # Fake cart items
    cart_items = [MOCK_BOOKS[0]]
    cart_items[0]['quantity'] = 2
    return render_template('customer/cart.html', cart_items=cart_items, total=31.98)

@app.route('/customer/orders')
def orders():
    return render_template('customer/orders.html', orders=[
        {'order_id': 99, 'order_date': '2023-01-01', 'total_price': 100, 'items': [], 'credit_card_no': '1234', 'expiry_date': '12/25'}
    ])

@app.route('/customer/profile')
def profile():
    user = {'first_name': 'Ahmed', 'last_name': 'Amr', 'username': 'ahmed123', 'email': 'ahmed@test.com', 'phone_number': '01012345678', 'shipping_address': 'Alexandria'}
    stats = {'total_orders': 5, 'total_spent': 500, 'total_books': 12}
    return render_template('customer/profile.html', user=user, stats=stats)

# --- Admin Routes ---
@app.route('/admin/dashboard')
def admin_dash():
    low_stock = [MOCK_BOOKS[1]] # The out of stock book
    return render_template('admin/dashboard.html', stats=MOCK_STATS, low_stock_books=low_stock)

@app.route('/admin/orders')
def admin_orders():
    return render_template('admin/orders.html', pending_orders=[], confirmed_orders=[], stats={'total_orders': 10, 'pending_count': 0, 'confirmed_count': 10})

if __name__ == '__main__':
    print("Preview server running! Open http://localhost:5000")
    app.run(debug=True, port=5000)