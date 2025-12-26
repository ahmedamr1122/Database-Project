from backend.database.connection import db
from backend.models.cart import Cart

class Order:
    @staticmethod
    def create_order(user_id, order_data):
        # Get cart items
        cart_items = Cart.get_cart_items(user_id)
        if not cart_items:
            raise ValueError("Cart is empty")

        # Calculate total
        total_price = sum(item['total_price'] for item in cart_items)

        # Create order
        query = """
        INSERT INTO Customer_Orders (user_id, order_date, total_price, status)
        VALUES (%s, NOW(), %s, 'Pending')
        """
        db.execute_query(query, (user_id, total_price))
        order_id = db.connection.cursor().lastrowid

        # Add order items
        for item in cart_items:
            query = """
            INSERT INTO Order_Items (order_id, isbn, quantity, price)
            VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, (order_id, item['isbn'], item['quantity'], item['selling_price']))

            # Update book stock
            query = "UPDATE Books SET stock = stock - %s WHERE isbn = %s"
            db.execute_query(query, (item['quantity'], item['isbn']))

        # Clear cart
        Cart.clear_cart(user_id)

        return order_id

    @staticmethod
    def get_user_orders(user_id):
        query = """
        SELECT co.order_id, co.order_date, co.total_price, co.status,
               GROUP_CONCAT(CONCAT(b.title, ' (', oi.quantity, ')') SEPARATOR ', ') as items
        FROM Customer_Orders co
        JOIN Order_Items oi ON co.order_id = oi.order_id
        JOIN Books b ON oi.isbn = b.isbn
        WHERE co.user_id = %s
        GROUP BY co.order_id, co.order_date, co.total_price, co.status
        ORDER BY co.order_date DESC
        """
        result = db.execute_query(query, (user_id,), fetch=True)
        return result if result else []

    @staticmethod
    def get_order_details(order_id, user_id):
        # Verify order belongs to user
        query = "SELECT * FROM Customer_Orders WHERE order_id = %s AND user_id = %s"
        order = db.execute_query(query, (order_id, user_id), fetch=True)
        if not order:
            return None

        # Get order items
        query = """
        SELECT oi.isbn, b.title, oi.quantity, oi.price, (oi.quantity * oi.price) as total
        FROM Order_Items oi
        JOIN Books b ON oi.isbn = b.isbn
        WHERE oi.order_id = %s
        """
        items = db.execute_query(query, (order_id,), fetch=True)

        return {
            'order': order[0],
            'items': items if items else []
        }
