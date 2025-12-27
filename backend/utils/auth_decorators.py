from functools import wraps
from flask import session, jsonify, redirect, url_for, flash, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # If it's an API request, return JSON? For now, assume SSR priority.
            # But customer.js might fetch API. 
            # We can check request.headers.get('Accept') or path.
            # Keep simple: Flash and redirect for now as we are doing SSR.
            flash('Please log in to access this resource', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in', 'warning')
            return redirect(url_for('auth.login'))
        
        if session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('customer.dashboard')) # Redirect to user home
            
        return f(*args, **kwargs)
    return decorated_function
