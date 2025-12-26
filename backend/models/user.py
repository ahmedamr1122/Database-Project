import bcrypt
from database.connection import get_db_connection

class User:
    @staticmethod
    def register_user(username, password, first_name, last_name, email, phone_number, shipping_address):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Check if username or email exists
            query_check = "SELECT user_id FROM Users WHERE username = %s OR email = %s"
            cursor.execute(query_check, (username, email))
            if cursor.fetchone():
                return False, "Username or Email already exists"

            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            query_insert = """
                INSERT INTO Users (username, password, first_name, last_name, email, phone_number, shipping_address, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'customer')
            """
            cursor.execute(query_insert, (username, hashed_password, first_name, last_name, email, phone_number, shipping_address))
            conn.commit()
            return True, "User registered successfully"
        except Exception as e:
            return False, str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def login(username, password):
        conn = get_db_connection()
        if not conn:
            return None, "Database connection error"
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return user, "Login successful"
            else:
                return None, "Invalid credentials"
        except Exception as e:
            return None, str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT user_id, username, first_name, last_name, email, phone_number, shipping_address, role FROM Users WHERE user_id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update_profile(user_id, first_name, last_name, email, phone_number, shipping_address, password=None):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        try:
            cursor = conn.cursor()
            
            if password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                query = """
                    UPDATE Users 
                    SET first_name=%s, last_name=%s, email=%s, phone_number=%s, shipping_address=%s, password=%s
                    WHERE user_id=%s
                """
                cursor.execute(query, (first_name, last_name, email, phone_number, shipping_address, hashed_password, user_id))
            else:
                query = """
                    UPDATE Users 
                    SET first_name=%s, last_name=%s, email=%s, phone_number=%s, shipping_address=%s
                    WHERE user_id=%s
                """
                cursor.execute(query, (first_name, last_name, email, phone_number, shipping_address, user_id))
                
            conn.commit()
            return True, "Profile updated"
        except Exception as e:
            return False, str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
