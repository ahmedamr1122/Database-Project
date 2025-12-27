import re
from datetime import datetime

def validate_isbn(isbn):
    """
    Validate ISBN format (simple check for now, can be expanded to ISBN-10/13 regex).
    Assuming ISBN is a string, possibly with dashes.
    """
    if not isbn:
        return False
    # Remove dashes and spaces
    clean_isbn = isbn.replace('-', '').replace(' ', '')
    # Check length (10 or 13) and digits
    if not clean_isbn.isdigit():
        # ISBN-10 can have 'X' at the end
        if len(clean_isbn) == 10 and clean_isbn[-1].upper() == 'X' and clean_isbn[:-1].isdigit():
             return True
        return False
    return len(clean_isbn) in [10, 13]

def validate_email(email):
    """
    Validate email format using regex.
    """
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_credit_card(card_no):
    """
    Simple validation for credit card number (Luhn algorithm could be added).
    For now, check if it's 16 digits.
    """
    if not card_no:
        return False
    clean_card = card_no.replace(' ', '').replace('-', '')
    return clean_card.isdigit() and len(clean_card) == 16

def validate_expiry_date(expiry_date_str):
    """
    Check if expiry date (YYYY-MM-DD or MM/YY) is in the future.
    For this project, assuming input might be a date string from an input type='date' (YYYY-MM-DD).
    """
    if not expiry_date_str:
        return False
    try:
        exp_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
        return exp_date >= datetime.now().date()
    except ValueError:
        return False

# ===== NEW VALIDATION FUNCTIONS =====

def validate_phone(phone):
    """
    Validate phone number (10-15 digits, optional +)
    """
    if not phone:
        return False
    pattern = r'^\+?[0-9]{10,15}$'
    phone = phone.replace(' ', '').replace('-', '')
    return re.match(pattern, phone) is not None

def validate_password(password):
    """
    Validate password strength:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain number"
    
    return True, "Valid"

def validate_username(username):
    """
    Validate username:
    - 3-50 characters
    - Only letters, numbers, underscore, hyphen
    - Must start with a letter
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 50:
        return False, "Username cannot exceed 50 characters"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', username):
        return False, "Username must start with letter"
    
    return True, "Valid"