from flask import Blueprint, request, jsonify
from backend.models.book import Book
from backend.models.publisher import Publisher
from backend.utils.auth_decorators import login_required, admin_required
from backend.utils.validators import validate_isbn

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/books', methods=['POST'])
@login_required
@admin_required
def add_book():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['isbn', 'title', 'publisher_name', 'selling_price', 'category']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Validate ISBN
        if not validate_isbn(data['isbn']):
            return jsonify({'error': 'Invalid ISBN format'}), 400

        # Validate price
        try:
            price = float(data['selling_price'])
            if price <= 0:
                return jsonify({'error': 'Price must be positive'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400

        # Add book
        Book.add_book(data)

        return jsonify({'message': 'Book added successfully'}), 201

    except Exception as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'ISBN already exists'}), 409
        return jsonify({'error': 'Failed to add book'}), 500

@admin_bp.route('/books/<isbn>', methods=['PUT'])
@login_required
@admin_required
def update_book(isbn):
    try:
        data = request.get_json()

        # Validate price if provided
        if 'selling_price' in data:
            try:
                price = float(data['selling_price'])
                if price <= 0:
                    return jsonify({'error': 'Price must be positive'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid price format'}), 400

        # Update book
        Book.update_book(isbn, data)

        return jsonify({'message': 'Book updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to update book'}), 500

@admin_bp.route('/orders/pending', methods=['GET'])
@login_required
@admin_required
def get_pending_orders():
    try:
        orders = Publisher.get_pending_orders()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch orders'}), 500

@admin_bp.route('/orders/<int:po_id>/confirm', methods=['POST'])
@login_required
@admin_required
def confirm_order(po_id):
    try:
        Publisher.confirm_order(po_id)
        return jsonify({'message': 'Order confirmed successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to confirm order'}), 500

@admin_bp.route('/reports/sales-month', methods=['GET'])
@login_required
@admin_required
def monthly_sales():
    try:
        sales = Publisher.get_monthly_sales()
        return jsonify({'sales': sales}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to generate report'}), 500

@admin_bp.route('/reports/sales-day', methods=['POST'])
@login_required
@admin_required
def daily_sales():
    try:
        data = request.get_json()
        date = data.get('date')
        if not date:
            return jsonify({'error': 'Date is required'}), 400

        sales = Publisher.get_daily_sales(date)
        return jsonify({'sales': sales}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to generate report'}), 500

@admin_bp.route('/reports/top-customers', methods=['GET'])
@login_required
@admin_required
def top_customers():
    try:
        customers = Publisher.get_top_customers()
        return jsonify(customers), 200
    except Exception as e:
        return jsonify({'error': 'Failed to generate report'}), 500

@admin_bp.route('/reports/top-books', methods=['GET'])
@login_required
@admin_required
def top_books():
    try:
        books = Publisher.get_top_books()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': 'Failed to generate report'}), 500

@admin_bp.route('/reports/replenishment/<isbn>', methods=['GET'])
@login_required
@admin_required
def replenishment_count(isbn):
    try:
        count = Publisher.get_replenishment_count(isbn)
        return jsonify({'count': count}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to generate report'}), 500
