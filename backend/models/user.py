from backend.database.connection import db
import bcrypt
import jwt
from datetime import datetime, timedelta
from backend.config import config

class User:
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def generate_token(user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def register_user(data):
        query = """
        INSERT INTO Users (username, password, first_name, last_name, email, phone_number, shipping_address, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'customer')
        """
        hashed_password = User.hash_password(data['password'])
        params = (
            data['username'], hashed_password, data['first_name'], data['last_name'],
            data['email'], data.get('phone_number'), data.get('shipping_address')
        )
        db.execute_query(query, params)
        return True

    @staticmethod
    def authenticate_user(username, password):
        query = "SELECT user_id, password, role, first_name, last_name FROM Users WHERE username = %s"
        result = db.execute_query(query, (username,), fetch=True)

        if result and User.check_password(password, result[0]['password']):
            return {
                'user_id': result[0]['user_id'],
                'role': result[0]['role'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name']
            }
        return None

    @staticmethod
    def get_user_by_id(user_id):
        query = """
        SELECT user_id, username, first_name, last_name, email, phone_number, shipping_address, role
        FROM Users WHERE user_id = %s
        """
        result = db.execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def update_user_profile(user_id, data):
        # Check current password if changing password
        if 'new_password' in data:
            query = "SELECT password FROM Users WHERE user_id = %s"
            result = db.execute_query(query, (user_id,), fetch=True)
            if not result or not User.check_password(data['current_password'], result[0]['password']):
                raise ValueError("Current password is incorrect")

            # Update password
            hashed_password = User.hash_password(data['new_password'])
            query = "UPDATE Users SET password = %s WHERE user_id = %s"
            db.execute_query(query, (hashed_password, user_id))

        # Update other fields
        update_fields = []
        params = []
        for field in ['first_name', 'last_name', 'email', 'phone_number', 'shipping_address']:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if update_fields:
            query = f"UPDATE Users SET {', '.join(update_fields)} WHERE user_id = %s"
            params.append(user_id)
            db.execute_query(query, params)

        return True
