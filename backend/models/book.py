from backend.database.connection import db

class Book:
    @staticmethod
    def add_book(data):
        query = """
        INSERT INTO Books (isbn, title, publisher_id, publication_year, selling_price, category, stock, threshold)
        VALUES (%s, %s, (SELECT publisher_id FROM Publishers WHERE name = %s), %s, %s, %s, %s, %s)
        """
        params = (
            data['isbn'], data['title'], data['publisher_name'], data.get('publication_year'),
            data['selling_price'], data['category'], data.get('stock', 0), data.get('threshold', 10)
        )
        db.execute_query(query, params)

        # Add authors if provided
        if 'authors' in data:
            for author_name in data['authors']:
                # Insert author if not exists
                db.execute_query(
                    "INSERT IGNORE INTO Authors (author_name) VALUES (%s)",
                    (author_name,)
                )
                # Get author_id
                author_result = db.execute_query(
                    "SELECT author_id FROM Authors WHERE author_name = %s",
                    (author_name,), fetch=True
                )
                if author_result:
                    author_id = author_result[0]['author_id']
                    # Link book to author
                    db.execute_query(
                        "INSERT INTO Book_Authors (isbn, author_id) VALUES (%s, %s)",
                        (data['isbn'], author_id)
                    )

        return True

    @staticmethod
    def update_book(isbn, data):
        update_fields = []
        params = []

        fields = ['title', 'publication_year', 'selling_price', 'category', 'stock', 'threshold']
        for field in fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if update_fields:
            query = f"UPDATE Books SET {', '.join(update_fields)} WHERE isbn = %s"
            params.append(isbn)
            db.execute_query(query, params)

        return True

    @staticmethod
    def search_books(search_params):
        conditions = []
        params = []

        if search_params.get('isbn'):
            conditions.append("b.isbn LIKE %s")
            params.append(f"%{search_params['isbn']}%")

        if search_params.get('title'):
            conditions.append("b.title LIKE %s")
            params.append(f"%{search_params['title']}%")

        if search_params.get('author'):
            conditions.append("a.author_name LIKE %s")
            params.append(f"%{search_params['author']}%")

        if search_params.get('category'):
            conditions.append("b.category LIKE %s")
            params.append(f"%{search_params['category']}%")

        if search_params.get('publisher'):
            conditions.append("p.name LIKE %s")
            params.append(f"%{search_params['publisher']}%")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"""
        SELECT DISTINCT b.isbn, b.title, b.selling_price, b.category, b.stock,
               p.name as publisher_name, GROUP_CONCAT(a.author_name) as authors
        FROM Books b
        LEFT JOIN Publishers p ON b.publisher_id = p.publisher_id
        LEFT JOIN Book_Authors ba ON b.isbn = ba.isbn
        LEFT JOIN Authors a ON ba.author_id = a.author_id
        WHERE {where_clause}
        GROUP BY b.isbn, b.title, b.selling_price, b.category, b.stock, p.name
        """
        result = db.execute_query(query, params, fetch=True)
        return result if result else []

    @staticmethod
    def get_book_details(isbn):
        query = """
        SELECT b.isbn, b.title, b.publication_year, b.selling_price, b.category, b.stock,
               p.name as publisher_name, GROUP_CONCAT(a.author_name) as authors
        FROM Books b
        LEFT JOIN Publishers p ON b.publisher_id = p.publisher_id
        LEFT JOIN Book_Authors ba ON b.isbn = ba.isbn
        LEFT JOIN Authors a ON ba.author_id = a.author_id
        WHERE b.isbn = %s
        GROUP BY b.isbn, b.title, b.publication_year, b.selling_price, b.category, b.stock, p.name
        """
        result = db.execute_query(query, (isbn,), fetch=True)
        return result[0] if result else None
