import re
from datetime import datetime

def validate_isbn(isbn):
    """Validate ISBN format (basic check)"""
    # Remove hyphens and spaces
    clean_isbn = re.sub(r'[- ]', '', isbn)
    # Check if it's 10 or 13 digits
    if not re.match(r'^\d{10}(\d{3})?$', clean_isbn):
        return False
    return True

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_credit_card(card_number):
    """Basic credit card validation (length and Luhn algorithm)"""
    # Remove spaces and hyphens
    card_number = re.sub(r'[- ]', '', card_number)

    if not re.match(r'^\d{13,19}$', card_number):
        return False

    # Luhn algorithm
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10

    return luhn_checksum(card_number) == 0

def validate_expiry_date(expiry_date):
    """Validate expiry date format (MM/YY) and not expired"""
    try:
        if isinstance(expiry_date, str):
            month, year = map(int, expiry_date.split('/'))
        else:
            # Assume it's a date object
            month, year = expiry_date.month, expiry_date.year

        # Convert to full year
        if year < 100:
            year += 2000

        # Check if date is in the future
        expiry = datetime(year, month, 1)
        now = datetime.now()

        return expiry > now
    except (ValueError, AttributeError):
        return False

def validate_phone_number(phone):
    """Validate phone number (basic international format)"""
    # Remove spaces, hyphens, parentheses
    clean_phone = re.sub(r'[- ()]', '', phone)
    # Check if it's 10-15 digits
    return re.match(r'^\d{10,15}$', clean_phone) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

def validate_quantity(quantity, max_stock=None):
    """Validate quantity"""
    try:
        qty = int(quantity)
        if qty <= 0:
            return False, "Quantity must be positive"
        if max_stock and qty > max_stock:
            return False, f"Only {max_stock} items available in stock"
        return True, ""
    except (ValueError, TypeError):
        return False, "Invalid quantity"
