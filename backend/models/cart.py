from database.connection import get_db_connection

class Cart:
    @staticmethod
    def add_to_cart(user_id, isbn, quantity=1):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        try:
            cursor = conn.cursor()
            
            # Check if item exists in cart
            cursor.execute("SELECT quantity FROM Shopping_Cart WHERE user_id = %s AND isbn = %s", (user_id, isbn))
            existing = cursor.fetchone()
            
            if existing:
                new_qty = existing[0] + quantity
                cursor.execute("UPDATE Shopping_Cart SET quantity = %s WHERE user_id = %s AND isbn = %s", (new_qty, user_id, isbn))
            else:
                cursor.execute("INSERT INTO Shopping_Cart (user_id, isbn, quantity) VALUES (%s, %s, %s)", (user_id, isbn, quantity))
                
            conn.commit()
            return True, "Item added to cart"
        except Exception as e:
            return False, str(e)
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_cart_items(user_id):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            # Join with Books to get title and price
            query = """
                SELECT sc.isbn, sc.quantity, b.title, b.selling_price
                FROM Shopping_Cart sc
                JOIN Books b ON sc.isbn = b.isbn
                WHERE sc.user_id = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def remove_from_cart(user_id, isbn):
        conn = get_db_connection()
        if not conn:
            return False, "Connection error"
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Shopping_Cart WHERE user_id = %s AND isbn = %s", (user_id, isbn))
            conn.commit()
            return True, "Item removed"
        except Exception as e:
            return False, str(e)
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def clear_cart(user_id):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Shopping_Cart WHERE user_id = %s", (user_id,))
            conn.commit()
            return True
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()
