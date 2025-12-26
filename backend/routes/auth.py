from flask import Blueprint, request, jsonify
from backend.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Register user
        User.register_user(data)

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Username or email already exists'}), 409
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Authenticate user
        user = User.authenticate_user(username, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate token
        token = User.generate_token(user['user_id'])

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'user_id': user['user_id'],
                'username': username,
                'role': user['role'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # For stateless JWT, logout is handled on client side
    return jsonify({'message': 'Logged out successfully'}), 200
