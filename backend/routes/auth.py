from flask import Blueprint, request, jsonify, session
from models.user import User
from models.cart import Cart
from utils.validators import validate_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user, message = User.login(username, password)
    
    if user:
        session['user_id'] = user['user_id']
        session['role'] = user['role']
        session['username'] = user['username']
        return jsonify({'message': message, 'user': {'username': user['username'], 'role': user['role']}}), 200
    else:
        return jsonify({'message': message}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    shipping_address = data.get('shipping_address')

    if not all([username, password, first_name, last_name, email]):
        return jsonify({'message': 'Missing required fields'}), 400

    if not validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    success, message = User.register_user(username, password, first_name, last_name, email, phone_number, shipping_address)
    
    if success:
        return jsonify({'message': message}), 201
    else:
        status_code = 409 if "exists" in message else 500
        return jsonify({'message': message}), status_code

@auth_bp.route('/logout', methods=['POST'])
def logout():
    user_id = session.get('user_id')
    if user_id:
        # Clear cart on logout? Requirement says "Logout (clears cart)" in file-structure notes (148)
        # But usually cart persistence is desired. However, I follow the notes.
        Cart.clear_cart(user_id)
        
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
