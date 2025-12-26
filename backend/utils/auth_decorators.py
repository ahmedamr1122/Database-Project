from functools import wraps
from flask import request, jsonify
from backend.models.user import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            token = token.replace('Bearer ', '')
            user_id = User.verify_token(token)
            if not user_id:
                return jsonify({'error': 'Invalid token'}), 401
        except:
            return jsonify({'error': 'Invalid token'}), 401

        # Add user_id to request
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            token = token.replace('Bearer ', '')
            user_id = User.verify_token(token)
            if not user_id:
                return jsonify({'error': 'Invalid token'}), 401

            # Check if user is admin
            user = User.get_user_by_id(user_id)
            if not user or user['role'] != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
        except:
            return jsonify({'error': 'Invalid token'}), 401

        # Add user_id to request
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function
