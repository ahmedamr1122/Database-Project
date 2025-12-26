from flask import Blueprint, request, jsonify
from models.book import Book

shared_bp = Blueprint('shared', __name__)

@shared_bp.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('query')
    category = request.args.get('category')
    
    books = Book.search_books(query, category)
    return jsonify(books), 200

@shared_bp.route('/books/<isbn>', methods=['GET'])
def get_book(isbn):
    book = Book.get_book_details(isbn)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({'message': 'Book not found'}), 404
