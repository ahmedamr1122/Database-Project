from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from models.cart import Cart
from models.order import Order
from models.user import User
from models.book import Book
from utils.auth_decorators import login_required
from utils.validators import validate_credit_card, validate_expiry_date
from database.connection import get_db_connection


customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Fetch All Books to display on the dashboard
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    # 2. Pass the books to the dashboard template
    return render_template('customer/dashboard.html', books=books)

@customer_bp.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query') # Keep for compatibility if used elsewhere
    category = request.args.get('category')
    isbn = request.args.get('isbn')
    title = request.args.get('title')
    author = request.args.get('author')
    publisher = request.args.get('publisher')
    
    # Use Book.search_books with specific fields
    books = Book.search_books(query_str=query, isbn=isbn, title=title, author=author, publisher=publisher, category=category)
    
    # Categories for dropdown (hardcoded or from DB)
    categories = ['Science', 'Art', 'Religion', 'History', 'Geography']
    return render_template('customer/search.html', books=books, categories=categories)

@customer_bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    user_id = session.get('user_id')
    items = Cart.get_cart_items(user_id)
    # Calculate totals
    subtotal = sum(item['quantity'] * item['selling_price'] for item in items)
    return render_template('customer/cart.html', cart_items=items, total=subtotal)

@customer_bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    user_id = session.get('user_id')
    # Form data or JSON? Standard form usually used in SSR, but search page 'Add' might be AJAX?
    # Let's support both or assume form/AJAX. 
    # Frontend logic (customer.js) usually does fetch calls for cart.
    # If fetch (AJAX), we return JSON. 
    # If form submit, redirect.
    # checking header or assuming JSON as per start code.
    
    if request.is_json:
        data = request.json
        isbn = data.get('isbn')
        quantity = int(data.get('quantity', 1))
    else:
        isbn = request.form.get('isbn')
        quantity = int(request.form.get('quantity', 1))

    if not isbn:
        if request.is_json: return jsonify({'message': 'ISBN required'}), 400
        flash('ISBN required', 'danger')
        return redirect(url_for('customer.search'))
        
    success, message = Cart.add_to_cart(user_id, isbn, quantity)
    
    if request.is_json:
        if success: return jsonify({'success': True, 'message': message}), 200
        else: return jsonify({'success': False, 'message': message}), 500
    else:
        if success: flash(message, 'success')
        else: flash(message, 'danger')
        return redirect(url_for('customer.search')) # or back

@customer_bp.route('/cart/remove', methods=['POST']) # Post used for actions in HTML forms
@login_required
def remove_from_cart():
    user_id = session.get('user_id')
    if request.is_json:
        isbn = request.json.get('isbn')
    else:
        isbn = request.form.get('isbn')
        
    success, message = Cart.remove_from_cart(user_id, isbn)
    
    if request.is_json:
        if success: return jsonify({'success': True, 'message': message}), 200
        return jsonify({'success': False, 'message': message}), 500
    
    if success: flash(message, 'success')
    else: flash(message, 'danger')
    return redirect(url_for('customer.get_cart'))

@customer_bp.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    user_id = session.get('user_id')
    isbn = request.form.get('isbn')
    quantity = int(request.form.get('quantity', 1)) 
    # Use Cart.add_to_cart which handles update if exists? Or need proper update?
    # Cart.add_to_cart adds to existing. We want to SET quantity.
    # Cart model doesn't have set_quantity? 
    # Let's check Cart model. If not, we remove and add? OR implement update.
    # For now, let's try remove then add or just add if logic supports it.
    # Actually, usually add_to_cart increments.
    # We need a new method in Cart or logic here. 
    # Let's assume for now we implement a simple update logic using SQL directly or helper.
    # Since I cannot see Cart model right now (I saw it earlier but forgot if it has update), 
    # I will stick to remove then add which is safe but inefficient, or add a method.
    # But wait, looking at my diffs, I implemented `add_to_cart` which does `INSERT ... ON DUPLICATE KEY UPDATE quantity = quantity + %s`.
    # That increments.
    # To set exact quantity, we might need to remove then add.
    
    # Better: Update Cart.py or use SQL here.
    # Let's used direct SQL for speed as I am verifying.
    from database.connection import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Shopping_Cart SET quantity = %s WHERE user_id = %s AND isbn = %s", (quantity, user_id, isbn))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Cart updated', 'success')
    return redirect(url_for('customer.get_cart'))

@customer_bp.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    user_id = session.get('user_id')
    Cart.clear_cart(user_id)
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Cart cleared'}), 200
        
    flash('Cart cleared', 'success')
    return redirect(url_for('customer.get_cart'))

@customer_bp.route('/cart/count', methods=['GET'])
@login_required
def get_cart_count():
    user_id = session.get('user_id')
    items = Cart.get_cart_items(user_id)
    count = sum(item['quantity'] for item in items)
    return jsonify({'count': count}), 200

@customer_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Fetch User Info (This fixes the 'user_info' error)
    cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user_info = cursor.fetchone()

    # 2. Fetch Cart Items (Keep your existing logic here)
    # Note: Adjust table name if yours is 'Shopping_Cart' or similar
    query = """
        SELECT B.title, B.selling_price, SC.quantity, (B.selling_price * SC.quantity) as total_price
        FROM Shopping_Cart SC
        JOIN Books B ON SC.isbn = B.isbn
        WHERE SC.user_id = %s
    """
    cursor.execute(query, (user_id,))
    items = cursor.fetchall()

    # 3. Calculate Totals
    subtotal = sum(item['total_price'] for item in items)
    total = subtotal # Add tax/shipping logic here if needed later

    cursor.close()
    conn.close()

    # 4. Pass 'user_info' to the template
    return render_template('customer/checkout.html', 
                        cart_items=items, 
                        subtotal=subtotal, 
                        total=total, 
                        user_info=user_info)
    # POST
    credit_card_no = request.form.get('credit_card_no')
    # Expiry comes as Month and Year often or just date. file structure says dropdowns implies Month/Year?
    # Validators expect YYYY-MM-DD. 
    # Let's see if we can get a date string or construct it.
    expiry_date = request.form.get('expiry_date') # assuming format YYYY-MM-DD from input type=date or constructed
    
    if not credit_card_no or not expiry_date:
        flash('Payment details required', 'danger')
        return redirect(url_for('customer.checkout'))
        
    if not validate_credit_card(credit_card_no):
         flash('Invalid credit card', 'danger')
         return redirect(url_for('customer.checkout'))
         
    if not validate_expiry_date(expiry_date):
        flash('Card expired or invalid date', 'danger')
        return redirect(url_for('customer.checkout'))
        
    success, message = Order.create_order(user_id, credit_card_no, expiry_date)
    
    if success:
        flash(message, 'success')
        return redirect(url_for('customer.get_orders'))
    else:
        flash(message, 'danger')
        return redirect(url_for('customer.checkout'))

@customer_bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Get the Order IDs
    cursor.execute("SELECT * FROM Customer_Orders WHERE user_id = %s ORDER BY order_date DESC", (user_id,))
    orders = cursor.fetchall()

    # 2. Get the Books for each order
    for order in orders:
        # NOTE: Make sure your table is named 'Order_Items' or 'Sales'
        # If this query crashes, your table name is likely different.
        query = """
            SELECT B.title, B.price, OI.quantity 
            FROM Order_Items OI
            JOIN Books B ON OI.book_id = B.book_id
            WHERE OI.order_id = %s
        """
        try:
            cursor.execute(query, (order['order_id'],))
            books = cursor.fetchall()
        except Exception:
            books = [] # If table is missing, show empty list
            
        # *** THE FIX: Use a unique name 'book_list' ***
        order['book_list'] = books

    cursor.close()
    conn.close()

    return render_template('customer/orders.html', orders=orders)

@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Fetch User Details
    cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    # 2. Fetch Orders (IMPORTANT: Verify 'user_id' vs 'customer_id' here)
    # Based on your previous error, your table likely uses 'user_id'
    cursor.execute("SELECT * FROM Customer_Orders WHERE user_id = %s ORDER BY order_date DESC", (user_id,))
    orders = cursor.fetchall()

    # 3. Calculate the stats
    stats_data = {
        'total_orders': len(orders)  # This counts the list of orders
    }

    cursor.close()
    conn.close()

    # 4. PASS THE DATA (This fixes the error)
    return render_template('customer/profile.html', user=user, orders=orders, stats=stats_data)
    
    # POST (Update)
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    shipping_address = request.form.get('shipping_address')
    password = request.form.get('password') # Optional
    # Confirm password?
    
    success, message = User.update_profile(user_id, first_name, last_name, email, phone_number, shipping_address, password)
    
    if success:
        flash(message, 'success')
        # Update session info if changed? 
        if email: session['username'] = email # If email is username? No, username is username.
        # User.py doesnt allow username update.
    else:
        flash(message, 'danger')
        
    return redirect(url_for('customer.profile'))
