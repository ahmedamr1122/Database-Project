from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from models.user import User
from models.cart import Cart
from utils.validators import validate_email

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
        # flash(message, 'success') # Optional: login success message
        
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
        
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    shipping_address = request.form.get('shipping_address')

    if not all([username, password, first_name, last_name, email]):
         flash('Missing required fields', 'danger')
         return render_template('register.html')

    if not validate_email(email):
         flash('Invalid email format', 'danger')
         return render_template('register.html')

    success, message = User.register_user(username, password, first_name, last_name, email, phone_number, shipping_address)
    
    if success:
        flash(message, 'success')
        return redirect(url_for('auth.login'))
    else:
        flash(message, 'danger')
        return render_template('register.html')

@auth_bp.route('/logout', methods=['GET', 'POST']) # Allow GET for simple link
def logout():
    user_id = session.get('user_id')
    if user_id:
        Cart.clear_cart(user_id)
        
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))
