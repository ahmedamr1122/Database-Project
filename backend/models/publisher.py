from database.connection import get_db_connection

class Publisher:
    @staticmethod
    def get_pending_orders():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            # Join with Publisher name and Book title
            query = """
                SELECT po.po_id, po.isbn, po.quantity, po.order_date, b.title, p.name as publisher_name
                FROM Publisher_Orders po
                JOIN Books b ON po.isbn = b.isbn
                JOIN Publishers p ON po.publisher_id = p.publisher_id
                WHERE po.status = 'Pending'
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def confirm_order(po_id):
        """
        Mark order as confirmed. Trigger will update stock.
        """
        conn = get_db_connection()
        if not conn:
            return False, "Connection error"
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Publisher_Orders SET status='Confirmed' WHERE po_id=%s", (po_id,))
            rows_affected = cursor.rowcount
            conn.commit()
            if rows_affected > 0:
                return True, "Order confirmed"
            else:
                return False, "Order not found"
        except Exception as e:
            return False, str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_all_publishers():
        # Helper for dropdowns
        conn = get_db_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Publishers")
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def add_publisher(name, address, email, phone, banking):
        conn = get_db_connection()
        if not conn: return False, "DB Connection Error"
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO Publishers (name, address, email_address, phone_number, banking_account)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, address, email, phone, banking))
            conn.commit()
            return True, "Publisher added successfully"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    # Reports Logic can be here or in a separate Report model, 
    # but file-structure says models/publisher.py generates reports (line 141)
    
    @staticmethod
    def report_sales_last_month():
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            # Query from db.sql line 160
            query = """
                SELECT SUM(total_price) AS Last_Month_Sales
                FROM Customer_Orders 
                WHERE order_date >= DATE_FORMAT(CURRENT_DATE - INTERVAL 1 MONTH, '%Y-%m-01') 
                AND order_date < DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
            """
            cursor.execute(query)
            result = cursor.fetchone()
            return result['Last_Month_Sales'] if result else 0
        finally:
            if conn: conn.close()

    @staticmethod
    def report_sales_day(date_str):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT SUM(total_price) AS Daily_Sales
                FROM Customer_Orders 
                WHERE date(order_date) = %s
            """
            cursor.execute(query, (date_str,))
            result = cursor.fetchone()
            return result['Daily_Sales'] if result and result['Daily_Sales'] else 0
        finally:
            if conn: conn.close()

    @staticmethod
    def get_replenishment_history(isbn):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT COUNT(*) as order_count
                FROM Publisher_Orders
                WHERE isbn = %s
            """
            cursor.execute(query, (isbn,))
            result = cursor.fetchone()
            return result['order_count'] if result else 0
        finally:
            if conn: conn.close()
