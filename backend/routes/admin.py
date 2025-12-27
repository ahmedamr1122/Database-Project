from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models.book import Book
from models.publisher import Publisher
from utils.auth_decorators import admin_required
from utils.validators import validate_isbn
from database.connection import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Get Total Books
    cursor.execute("SELECT COUNT(*) as count FROM Books")
    book_count = cursor.fetchone()['count']
    
    # 2. Get Total Customers
    cursor.execute("SELECT COUNT(*) as count FROM Users WHERE role = 'customer'")
    user_count = cursor.fetchone()['count']

    # 3. Get Pending Orders
    cursor.execute("SELECT COUNT(*) as count FROM Publisher_Orders WHERE status = 'Pending'")
    pending_orders_count = cursor.fetchone()['count']

    # 4. Get Monthly Sales (Last 30 days)
    # Using Publisher.report_sales_last_month helper or direct query. 
    # Let's use direct query for simplicity and speed here.
    cursor.execute("""
        SELECT COALESCE(SUM(total_price), 0) as total 
        FROM Customer_Orders 
        WHERE order_date >= date_sub(now(), interval 1 month)
    """)
    monthly_sales = cursor.fetchone()['total']

    # 5. Low Stock Books
    cursor.execute("SELECT * FROM Books WHERE stock < threshold")
    low_stock_books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    stats_data = {
        'total_books': book_count,
        'total_customers': user_count,
        'pending_orders': pending_orders_count,
        'monthly_sales': monthly_sales
    }

    return render_template('admin/dashboard.html', stats=stats_data, low_stock_books=low_stock_books)

@admin_bp.route('/add-book', methods=['GET', 'POST']) # Renaming to match frontend link /admin/add-book
@admin_required
def add_book():
    if request.method == 'GET':
        publishers = Publisher.get_all_publishers()
        return render_template('admin/add_book.html', publishers=publishers)

    # POST
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    publisher_id = request.form.get('publisher_id')
    pub_year = request.form.get('pub_year')
    selling_price = request.form.get('selling_price')
    category = request.form.get('category')
    threshold = request.form.get('threshold', 10)
    # Authors: Assuming comma-separated string from form or multiple inputs
    authors_str = request.form.get('authors')
    authors = [a.strip() for a in authors_str.split(',')] if authors_str else []

    if not all([isbn, title, publisher_id, pub_year, selling_price, category, authors]):
        flash('Missing required fields', 'danger')
        return redirect(url_for('admin.add_book'))

    if not validate_isbn(isbn):
        flash('Invalid ISBN format', 'danger')
        return redirect(url_for('admin.add_book'))

    success, message = Book.add_book(isbn, title, publisher_id, pub_year, selling_price, category, threshold, authors)
    
    if success:
        flash(message, 'success')
        return redirect(url_for('admin.dashboard'))
    else:
        flash(message, 'danger')
        return redirect(url_for('admin.add_book'))

# Modify/Search Book Route needed? Frontend has modify_book.html
# It likely needs a search first, then edit form.
# Let's assume /admin/modify-book ? 
# Frontend README: 
#   Search: GET /admin/modify-book
#   Update: POST /admin/modify-book (probably with ID or hidden field)
#   Wait, RESTful would be PUT /admin/books/<isbn> but forms don't support PUT easily without JS.
#   Let's stick to POST for web forms.

@admin_bp.route('/modify-book', methods=['GET', 'POST'])
@admin_required
def modify_book():
    book = None
    if request.args.get('search'):
        query = request.args.get('search')
        # Search for one book or list? 
        # modify_book.html implies "Search book, then edit form".
        # Let's search and pick first or exact match?
        # Book.search_books returns list.
        results = Book.search_books(query)
        # If specific ISBN update? 
        # Let's assume this route handles both listing results and showing edit form?
        # Or maybe just List.
        return render_template('admin/modify_book.html', search_results=results)
    
    # If POST (Update)
    if request.method == 'POST':
        isbn = request.form.get('isbn') # Readonly in form
        title = request.form.get('title')
        pub_year = request.form.get('pub_year')
        selling_price = request.form.get('selling_price')
        category = request.form.get('category')
        threshold = request.form.get('threshold')
        
        if not all([title, pub_year, selling_price, category, threshold]):
            flash('Missing required fields', 'danger')
            return redirect(url_for('admin.modify_book'))
            
        success, message = Book.update_book(isbn, title, pub_year, selling_price, category, threshold)
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
        return redirect(url_for('admin.modify_book'))
        
    return render_template('admin/modify_book.html')

@admin_bp.route('/orders', methods=['GET'])
@admin_required
def orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Get Pending Orders
    # Join with books and publishers for details
    query = """
        SELECT po.po_id, po.isbn, po.quantity, po.order_date, b.title as book_title, p.name as publisher_name
        FROM Publisher_Orders po
        JOIN Books b ON po.isbn = b.isbn
        JOIN Publishers p ON po.publisher_id = p.publisher_id
        WHERE po.status = 'Pending'
    """
    cursor.execute(query)
    pending_orders = cursor.fetchall()

    # 2. Get Confirmed Orders (Last 50 maybe?)
    query_confirmed = """
        SELECT po.po_id, po.isbn, po.quantity, po.order_date, b.title as book_title, p.name as publisher_name
        FROM Publisher_Orders po
        JOIN Books b ON po.isbn = b.isbn
        JOIN Publishers p ON po.publisher_id = p.publisher_id
        WHERE po.status = 'Confirmed'
        ORDER BY po.order_date DESC LIMIT 20
    """
    cursor.execute(query_confirmed)
    confirmed_orders = cursor.fetchall()
    
    # 3. Stats
    cursor.execute("SELECT COUNT(*) as count FROM Publisher_Orders")
    total_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM Publisher_Orders WHERE status = 'Pending'")
    pending_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM Publisher_Orders WHERE status = 'Confirmed'")
    confirmed_count = cursor.fetchone()['count']
    
    stats_data = {
        'total_orders': total_count,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count
    }

    cursor.close()
    conn.close()

    return render_template('admin/orders.html', 
                           pending_orders=pending_orders, 
                           confirmed_orders=confirmed_orders, 
                           stats=stats_data)

@admin_bp.route('/orders/<int:po_id>/confirm', methods=['POST'])
@admin_required
def confirm_order(po_id):
    success, message = Publisher.confirm_order(po_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400

@admin_bp.route('/reports', methods=['GET'])
@admin_required
def reports():
    # Render reports page. Reports calculation is likely via form submission or AJAX.
    # Frontend README says: POST /admin/reports/sales-month etc.
    # If page has 'Generate' buttons, they might post to these routes.
    # Let's keep separate report routes but make them return JSON or render back to reports page with data?
    # Usually easier to render reports.html with data.
    return render_template('admin/reports.html')

# Report calculation routes (returning JSON for AJAX or rendering?)
# Frontend README implies rendering or JSON. "Forms to select date... display results". 
# If separate POSTs, maybe AJAX.
# Let's keep them as JSON APIs for now if the JS does fetch.
# The README says: "Actions: POST /admin/reports/sales-month". 
# admin.js likely handles it.

@admin_bp.route('/reports/sales-month', methods=['POST'])
@admin_required
def report_sales_month():
    sales = Publisher.report_sales_last_month()
    return jsonify({'last_month_sales': sales}), 200

# Add other report routes as per README
