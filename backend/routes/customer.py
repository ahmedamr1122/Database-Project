from flask import Blueprint, request, jsonify, session
from models.cart import Cart
from models.order import Order
from models.user import User
from utils.auth_decorators import login_required
from utils.validators import validate_credit_card, validate_expiry_date

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    user_id = session.get('user_id')
    items = Cart.get_cart_items(user_id)
    return jsonify(items), 200

@customer_bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    user_id = session.get('user_id')
    data = request.json
    isbn = data.get('isbn')
    quantity = data.get('quantity', 1)
    
    if not isbn:
        return jsonify({'message': 'ISBN required'}), 400
        
    success, message = Cart.add_to_cart(user_id, isbn, quantity)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 500

@customer_bp.route('/cart/<isbn>', methods=['DELETE'])
@login_required
def remove_from_cart(isbn):
    user_id = session.get('user_id')
    success, message = Cart.remove_from_cart(user_id, isbn)
    if success:
        return jsonify({'message': message}), 200
    else:
         return jsonify({'message': message}), 500

@customer_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    user_id = session.get('user_id')
    data = request.json
    credit_card_no = data.get('credit_card_no')
    expiry_date = data.get('expiry_date') # YYYY-MM-DD
    
    if not credit_card_no or not expiry_date:
        return jsonify({'message': 'Payment details required'}), 400
        
    if not validate_credit_card(credit_card_no):
         return jsonify({'message': 'Invalid credit card'}), 400
         
    if not validate_expiry_date(expiry_date):
        return jsonify({'message': 'Card expired or invalid date'}), 400
        
    success, message = Order.create_order(user_id, credit_card_no, expiry_date)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

@customer_bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    user_id = session.get('user_id')
    orders = Order.get_user_orders(user_id)
    return jsonify(orders), 200

@customer_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    user_id = session.get('user_id')
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    shipping_address = data.get('shipping_address')
    password = data.get('password') # Optional
    
    success, message = User.update_profile(user_id, first_name, last_name, email, phone_number, shipping_address, password)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 500
