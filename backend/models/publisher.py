from backend.database.connection import db

class Publisher:
    @staticmethod
    def get_pending_orders():
        query = """
        SELECT po.po_id, po.isbn, po.quantity, po.order_date,
               b.title, p.name as publisher_name
        FROM Publisher_Orders po
        JOIN Books b ON po.isbn = b.isbn
        JOIN Publishers p ON po.publisher_id = p.publisher_id
        WHERE po.status = 'Pending'
        ORDER BY po.order_date DESC
        """
        result = db.execute_query(query, fetch=True)
        return result if result else []

    @staticmethod
    def confirm_order(po_id):
        # Update order status - trigger will handle stock update
        query = "UPDATE Publisher_Orders SET status = 'Confirmed' WHERE po_id = %s"
        db.execute_query(query, (po_id,))
        return True

    @staticmethod
    def get_replenishment_count(isbn):
        query = "SELECT COUNT(*) as count FROM Publisher_Orders WHERE isbn = %s"
        result = db.execute_query(query, (isbn,), fetch=True)
        return result[0]['count'] if result else 0

    @staticmethod
    def get_monthly_sales():
        query = """
        SELECT SUM(total_price) as sales
        FROM Customer_Orders
        WHERE order_date >= DATE_FORMAT(CURRENT_DATE - INTERVAL 1 MONTH, '%Y-%m-01')
          AND order_date < DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
        """
        result = db.execute_query(query, fetch=True)
        return result[0]['sales'] if result and result[0]['sales'] else 0.0

    @staticmethod
    def get_daily_sales(date):
        query = "SELECT SUM(total_price) as sales FROM Customer_Orders WHERE DATE(order_date) = %s"
        result = db.execute_query(query, (date,), fetch=True)
        return result[0]['sales'] if result and result[0]['sales'] else 0.0

    @staticmethod
    def get_top_customers():
        query = """
        SELECT u.username, SUM(co.total_price) as total_spent
        FROM Customer_Orders co
        JOIN Users u ON co.user_id = u.user_id
        WHERE co.order_date >= CURRENT_DATE - INTERVAL 3 MONTH
        GROUP BY u.username
        ORDER BY total_spent DESC
        LIMIT 5
        """
        result = db.execute_query(query, fetch=True)
        return result if result else []

    @staticmethod
    def get_top_books():
        query = """
        SELECT b.isbn, b.title, SUM(oi.quantity) as copies_sold
        FROM Order_Items oi
        JOIN Books b ON oi.isbn = b.isbn
        JOIN Customer_Orders co ON oi.order_id = co.order_id
        WHERE co.order_date >= CURRENT_DATE - INTERVAL 3 MONTH
        GROUP BY b.isbn, b.title
        ORDER BY copies_sold DESC
        LIMIT 10
        """
        result = db.execute_query(query, fetch=True)
        return result if result else []
