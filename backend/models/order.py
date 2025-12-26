from datetime import datetime
from database.connection import get_db_connection

class Order:
    @staticmethod
    def create_order(user_id, credit_card_no, expiry_date):
        """
        Create order from current cart contents.
        """
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        try:
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction()

            # 1. Get Cart Items
            cursor.execute("SELECT isbn, quantity FROM Shopping_Cart WHERE user_id = %s", (user_id,))
            cart_items = cursor.fetchall()
            
            if not cart_items:
                return False, "Cart is empty"

            # 2. Calculate Total Price and Check Stock? 
            # Note: Trigger 'Deduct_Stock_On_Purchase' handles deduction, 
            # and 'Prevent_Negative_Stock' handles validation.
            # But we might want to check price here or let the DB handle it if possible? Use Python for total calculation.
            
            total_price = 0
            order_items_data = [] # List of tuples (isbn, quantity, price)

            for item in cart_items:
                cursor.execute("SELECT selling_price FROM Books WHERE isbn = %s", (item['isbn'],))
                book = cursor.fetchone()
                if not book:
                     raise Exception(f"Book {item['isbn']} not found")
                
                price = book['selling_price']
                quantity = item['quantity']
                total_price += price * quantity
                order_items_data.append((item['isbn'], quantity, price))

            # 3. Create Order Header
            query_order = """
                INSERT INTO Customer_Orders (user_id, total_price, credit_card_no, expiry_date)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_order, (user_id, total_price, credit_card_no, expiry_date))
            order_id = cursor.lastrowid

            # 4. Insert Order Items (Triggers will fire here)
            query_item = """
                INSERT INTO Order_Items (order_id, isbn, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
            """
            for isbn, qty, price in order_items_data:
                cursor.execute(query_item, (order_id, isbn, qty, price))

            # 5. Clear Cart
            cursor.execute("DELETE FROM Shopping_Cart WHERE user_id = %s", (user_id,))

            conn.commit()
            return True, f"Order #{order_id} placed successfully"
        except Exception as e:
            conn.rollback()
            return False, f"Order failed: {str(e)}"
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_user_orders(user_id):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM Customer_Orders WHERE user_id = %s ORDER BY order_date DESC"
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()
    
    @staticmethod
    def get_order_details(order_id):
        # Could return header + items
        conn = get_db_connection()
        if not conn: 
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Customer_Orders WHERE order_id = %s", (order_id,))
            header = cursor.fetchone()
            
            cursor.execute("""
                SELECT oi.isbn, oi.quantity, oi.unit_price, b.title 
                FROM Order_Items oi
                JOIN Books b ON oi.isbn = b.isbn
                WHERE oi.order_id = %s
            """, (order_id,))
            items = cursor.fetchall()
            
            return {'header': header, 'items': items}
        finally:
             if conn.is_connected():
                cursor.close()
                conn.close()
