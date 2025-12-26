from flask import Blueprint, request, jsonify
from backend.models.cart import Cart
from backend.models.order import Order
from backend.models.user import User
from backend.utils.auth_decorators import login_required

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    try:
        user_id = request.user_id
        cart_items = Cart.get_cart_items(user_id)
        cart_count = Cart.get_cart_count(user_id)
        cart_total = Cart.get_cart_total(user_id)

        return jsonify({
            'items': cart_items,
            'count': cart_count,
            'total': cart_total
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch cart'}), 500

@customer_bp.route('/cart', methods=['POST'])
@login_required
def add_to_cart():
    try:
        user_id = request.user_id
        data = request.get_json()

        isbn = data.get('isbn')
        quantity = data.get('quantity', 1)

        if not isbn:
            return jsonify({'error': 'ISBN is required'}), 400

        Cart.add_to_cart(user_id, isbn, quantity)

        return jsonify({'message': 'Item added to cart'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to add item to cart'}), 500

@customer_bp.route('/cart/<isbn>', methods=['PUT'])
@login_required
def update_cart_item(isbn):
    try:
        user_id = request.user_id
        data = request.get_json()

        quantity = data.get('quantity')
        if quantity is None:
            return jsonify({'error': 'Quantity is required'}), 400

        Cart.update_cart_item(user_id, isbn, quantity)

        return jsonify({'message': 'Cart updated'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update cart'}), 500

@customer_bp.route('/cart/<isbn>', methods=['DELETE'])
@login_required
def remove_from_cart(isbn):
    try:
        user_id = request.user_id
        Cart.remove_from_cart(user_id, isbn)

        return jsonify({'message': 'Item removed from cart'}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to remove item from cart'}), 500

@customer_bp.route('/cart', methods=['DELETE'])
@login_required
def clear_cart():
    try:
        user_id = request.user_id
        Cart.clear_cart(user_id)

        return jsonify({'message': 'Cart cleared'}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to clear cart'}), 500

@customer_bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    try:
        user_id = request.user_id
        orders = Order.get_user_orders(user_id)

        return jsonify(orders), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch orders'}), 500

@customer_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    try:
        user_id = request.user_id
        data = request.get_json()

        order_id = Order.create_order(user_id, data)

        return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create order'}), 500

@customer_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order_details(order_id):
    try:
        user_id = request.user_id
        order_details = Order.get_order_details(order_id, user_id)

        if not order_details:
            return jsonify({'error': 'Order not found'}), 404

        return jsonify(order_details), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch order details'}), 500

@customer_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    try:
        user_id = request.user_id
        user = User.get_user_by_id(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile'}), 500

@customer_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    try:
        user_id = request.user_id
        data = request.get_json()

        User.update_user_profile(user_id, data)

        return jsonify({'message': 'Profile updated successfully'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update profile'}), 500

@customer_bp.route('/cart/count', methods=['GET'])
@login_required
def get_cart_count():
    try:
        user_id = request.user_id
        count = Cart.get_cart_count(user_id)

        return jsonify({'count': count}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get cart count'}), 500

@customer_bp.route('/orders/recent', methods=['GET'])
@login_required
def get_recent_orders():
    try:
        user_id = request.user_id
        orders = Order.get_user_orders(user_id)

        # Return only recent 3 orders
        recent_orders = orders[:3] if orders else []

        return jsonify(recent_orders), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch recent orders'}), 500

@customer_bp.route('/profile/password', methods=['PUT'])
@login_required
def update_password():
    try:
        user_id = request.user_id
        data = request.get_json()

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password are required'}), 400

        User.update_user_profile(user_id, {
            'current_password': current_password,
            'new_password': new_password
        })

        return jsonify({'message': 'Password updated successfully'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update password'}), 500
