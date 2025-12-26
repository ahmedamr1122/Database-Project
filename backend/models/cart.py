from backend.database.connection import db

class Cart:
    @staticmethod
    def add_to_cart(user_id, isbn, quantity=1):
        # Check if book exists and has stock
        book = db.execute_query("SELECT stock FROM Books WHERE isbn = %s", (isbn,), fetch=True)
        if not book or book[0]['stock'] < quantity:
            raise ValueError("Insufficient stock")

        # Check if item already in cart
        existing = db.execute_query(
            "SELECT quantity FROM Shopping_Cart WHERE user_id = %s AND isbn = %s",
            (user_id, isbn), fetch=True
        )

        if existing:
            # Update quantity
            new_quantity = existing[0]['quantity'] + quantity
            if new_quantity > book[0]['stock']:
                raise ValueError("Insufficient stock")
            db.execute_query(
                "UPDATE Shopping_Cart SET quantity = %s WHERE user_id = %s AND isbn = %s",
                (new_quantity, user_id, isbn)
            )
        else:
            # Add new item
            db.execute_query(
                "INSERT INTO Shopping_Cart (user_id, isbn, quantity) VALUES (%s, %s, %s)",
                (user_id, isbn, quantity)
            )

        return True

    @staticmethod
    def get_cart_items(user_id):
        query = """
        SELECT sc.isbn, sc.quantity, b.title, b.selling_price,
               (sc.quantity * b.selling_price) as total_price,
               GROUP_CONCAT(a.author_name) as authors
        FROM Shopping_Cart sc
        JOIN Books b ON sc.isbn = b.isbn
        LEFT JOIN Book_Authors ba ON b.isbn = ba.isbn
        LEFT JOIN Authors a ON ba.author_id = a.author_id
        WHERE sc.user_id = %s
        GROUP BY sc.isbn, sc.quantity, b.title, b.selling_price
        """
        result = db.execute_query(query, (user_id,), fetch=True)
        return result if result else []

    @staticmethod
    def update_cart_item(user_id, isbn, quantity):
        if quantity <= 0:
            Cart.remove_from_cart(user_id, isbn)
            return True

        # Check stock
        book = db.execute_query("SELECT stock FROM Books WHERE isbn = %s", (isbn,), fetch=True)
        if not book or book[0]['stock'] < quantity:
            raise ValueError("Insufficient stock")

        db.execute_query(
            "UPDATE Shopping_Cart SET quantity = %s WHERE user_id = %s AND isbn = %s",
            (quantity, user_id, isbn)
        )
        return True

    @staticmethod
    def remove_from_cart(user_id, isbn):
        db.execute_query(
            "DELETE FROM Shopping_Cart WHERE user_id = %s AND isbn = %s",
            (user_id, isbn)
        )
        return True

    @staticmethod
    def clear_cart(user_id):
        db.execute_query("DELETE FROM Shopping_Cart WHERE user_id = %s", (user_id,))
        return True

    @staticmethod
    def get_cart_count(user_id):
        result = db.execute_query(
            "SELECT SUM(quantity) as total FROM Shopping_Cart WHERE user_id = %s",
            (user_id,), fetch=True
        )
        return result[0]['total'] if result and result[0]['total'] else 0

    @staticmethod
    def get_cart_total(user_id):
        query = """
        SELECT SUM(sc.quantity * b.selling_price) as total
        FROM Shopping_Cart sc
        JOIN Books b ON sc.isbn = b.isbn
        WHERE sc.user_id = %s
        """
        result = db.execute_query(query, (user_id,), fetch=True)
        return result[0]['total'] if result and result[0]['total'] else 0.0
