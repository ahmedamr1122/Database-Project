from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from models.user import User
from models.cart import Cart
from utils.validators import validate_email, validate_phone, validate_password, validate_username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash('Missing username or password', 'danger')
        return render_template('login.html')
    
    user, message = User.login(username, password)
    
    if user:
        session['user_id'] = user['user_id']
        session['role'] = user['role']
        session['username'] = user['username']
        
        if user['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('customer.dashboard'))
    else:
        flash(message, 'danger')
        return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    # Get and clean form data
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    phone_number = request.form.get('phone_number', '').strip()
    shipping_address = request.form.get('shipping_address', '').strip()

    # Check required fields
    if not all([username, password, first_name, last_name, email]):
         flash('Missing required fields', 'danger')
         return render_template('register.html')

    # === NEW VALIDATIONS START HERE ===
    
    # Validate username
    is_valid, msg = validate_username(username)
    if not is_valid:
         flash(msg, 'danger')
         return render_template('register.html')

    # Validate password strength
    is_valid, msg = validate_password(password)
    if not is_valid:
         flash(msg, 'danger')
         return render_template('register.html')

    # Validate email format
    if not validate_email(email):
         flash('Invalid email format', 'danger')
         return render_template('register.html')

    # Validate phone number (if provided)
    if phone_number and not validate_phone(phone_number):
         flash('Invalid phone number format', 'danger')
         return render_template('register.html')

    # Validate names (only letters and spaces)
    if not first_name.replace(' ', '').isalpha():
         flash('First name should only contain letters', 'danger')
         return render_template('register.html')
    
    if not last_name.replace(' ', '').isalpha():
         flash('Last name should only contain letters', 'danger')
         return render_template('register.html')

    # === NEW VALIDATIONS END HERE ===

    success, message = User.register_user(username, password, first_name, last_name, email, phone_number, shipping_address)
    
    if success:
        flash(message, 'success')
        return redirect(url_for('auth.login'))
    else:
        flash(message, 'danger')
        return render_template('register.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    user_id = session.get('user_id')
    if user_id:
        Cart.clear_cart(user_id)
        
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))