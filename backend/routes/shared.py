from flask import Blueprint, request, jsonify
from backend.models.book import Book

shared_bp = Blueprint('shared', __name__)

@shared_bp.route('/books/search', methods=['GET'])
def search_books():
    try:
        # Get search parameters
        isbn = request.args.get('isbn')
        title = request.args.get('title')
        author = request.args.get('author')
        category = request.args.get('category')
        publisher = request.args.get('publisher')

        # Perform search
        books = Book.search_books({
            'isbn': isbn,
            'title': title,
            'author': author,
            'category': category,
            'publisher': publisher
        })

        return jsonify(books), 200

    except Exception as e:
        return jsonify({'error': 'Search failed'}), 500

@shared_bp.route('/books/<isbn>', methods=['GET'])
def get_book_details(isbn):
    try:
        book = Book.get_book_details(isbn)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        return jsonify(book), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch book details'}), 500
