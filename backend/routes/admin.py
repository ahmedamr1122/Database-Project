from flask import Blueprint, request, jsonify
from models.book import Book
from models.publisher import Publisher
from utils.auth_decorators import admin_required
from utils.validators import validate_isbn

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/books', methods=['POST'])
@admin_required
def add_book():
    data = request.json
    isbn = data.get('isbn')
    title = data.get('title')
    publisher_id = data.get('publisher_id')
    pub_year = data.get('pub_year')
    selling_price = data.get('selling_price')
    category = data.get('category')
    threshold = data.get('threshold', 10)
    authors = data.get('authors', []) # List of names

    if not all([isbn, title, publisher_id, pub_year, selling_price, category, authors]):
        return jsonify({'message': 'Missing required fields'}), 400

    if not validate_isbn(isbn):
        return jsonify({'message': 'Invalid ISBN format'}), 400

    success, message = Book.add_book(isbn, title, publisher_id, pub_year, selling_price, category, threshold, authors)
    
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'message': message}), 500

@admin_bp.route('/books/<isbn>', methods=['PUT'])
@admin_required
def update_book(isbn):
    data = request.json
    title = data.get('title')
    pub_year = data.get('pub_year')
    selling_price = data.get('selling_price')
    category = data.get('category')
    threshold = data.get('threshold')
    
    if not all([title, pub_year, selling_price, category, threshold]):
        return jsonify({'message': 'Missing required fields'}), 400
        
    success, message = Book.update_book(isbn, title, pub_year, selling_price, category, threshold)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 500

@admin_bp.route('/orders/pending', methods=['GET'])
@admin_required
def get_pending_publisher_orders():
    orders = Publisher.get_pending_orders()
    return jsonify(orders), 200

@admin_bp.route('/orders/<int:po_id>/confirm', methods=['POST'])
@admin_required
def confirm_publisher_order(po_id):
    success, message = Publisher.confirm_order(po_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

@admin_bp.route('/reports/sales-month', methods=['GET'])
@admin_required
def report_sales_month():
    sales = Publisher.report_sales_last_month()
    return jsonify({'last_month_sales': sales}), 200

# Additional report routes can be added here
