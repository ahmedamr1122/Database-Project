from database.connection import get_db_connection

class Book:
    @staticmethod
    def add_book(isbn, title, publisher_id, pub_year, selling_price, category, threshold, authors):
        """
        Add a new book and its authors.
        authors: list of author names (string)
        """
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        try:
            cursor = conn.cursor()
            conn.start_transaction()

            # Insert Book
            query_book = """
                INSERT INTO Books (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Initially stock is 0? or perhaps user provides it? Schema says default 0. 
            # The prompt says 'stock' is not in the 'add_book' fields in file-structure? 
            # Wait, file-structure line 196: "Add Book: Form with all book fields + threshold". 
            # Let's assume stock starts at 0 or we can add it. 
            # I'll stick to 0 default for new books as per typical flow unless specified.
            stock = 0
            cursor.execute(query_book, (isbn, title, publisher_id, pub_year, selling_price, category, stock, threshold))

            # Handle Authors
            for author_name in authors:
                # Check if author exists
                cursor.execute("SELECT author_id FROM Authors WHERE author_name = %s", (author_name,))
                author_row = cursor.fetchone()
                if author_row:
                     author_id = author_row[0]
                else:
                    cursor.execute("INSERT INTO Authors (author_name) VALUES (%s)", (author_name,))
                    author_id = cursor.lastrowid
                
                # Link Book-Author
                cursor.execute("INSERT INTO Book_Authors (isbn, author_id) VALUES (%s, %s)", (isbn, author_id))

            conn.commit()
            return True, "Book added successfully"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update_book(isbn, title, pub_year, selling_price, category, threshold):
        # Modification usually doesn't change ISBN or Authors easily, but let's see. 
        # File structure says "Edit/update books".
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        try:
            cursor = conn.cursor()
            query = """
                UPDATE Books 
                SET title=%s, pub_year=%s, selling_price=%s, category=%s, threshold=%s
                WHERE isbn=%s
            """
            cursor.execute(query, (title, pub_year, selling_price, category, threshold, isbn))
            conn.commit()
            return True, "Book updated"
        except Exception as e:
            return False, str(e)
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def search_books(query_str=None, category=None):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            # Basic query joining authors and publishers
            # Note: Group_Concat for authors might be useful
            base_query = """
                SELECT b.*, p.name as publisher_name, GROUP_CONCAT(a.author_name SEPARATOR ', ') as authors
                FROM Books b
                JOIN Publishers p ON b.publisher_id = p.publisher_id
                JOIN Book_Authors ba ON b.isbn = ba.isbn
                JOIN Authors a ON ba.author_id = a.author_id
            """
            
            where_clauses = []
            params = []

            if category:
                where_clauses.append("b.category = %s")
                params.append(category)

            if query_str:
                # naive search in title, isbn, author name
                # Since we are joining, we need to be careful with WHERE vs HAVING for aggregated columns?
                # Actually, filtering by author name before grouping is easier.
                search_term = f"%{query_str}%"
                where_clauses.append("(b.title LIKE %s OR b.isbn LIKE %s OR a.author_name LIKE %s)")
                params.extend([search_term, search_term, search_term])
            
            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)
            
            base_query += " GROUP BY b.isbn"
            
            cursor.execute(base_query, params)
            return cursor.fetchall()
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_book_details(isbn):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT b.*, p.name as publisher_name, GROUP_CONCAT(a.author_name SEPARATOR ', ') as authors
                FROM Books b
                JOIN Publishers p ON b.publisher_id = p.publisher_id
                JOIN Book_Authors ba ON b.isbn = ba.isbn
                JOIN Authors a ON ba.author_id = a.author_id
                WHERE b.isbn = %s
                GROUP BY b.isbn
            """
            cursor.execute(query, (isbn,))
            return cursor.fetchone()
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()
