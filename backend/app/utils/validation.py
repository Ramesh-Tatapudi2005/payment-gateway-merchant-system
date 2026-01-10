import re
from datetime import datetime

def validate_vpa(vpa: str) -> bool:
    """Validates VPA format."""
    # Matches alphanumeric handles and providers (e.g., user@bank)
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+$"
    return bool(re.match(pattern, vpa))

def validate_luhn(card_number: str) -> bool:
    """Implements the Luhn algorithm for card validation."""
    card_number = card_number.replace(" ", "").replace("-", "")
    
    if not card_number.isdigit() or not (13 <= len(card_number) <= 19):
        return False

    digits = [int(d) for d in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
            
    return sum(digits) % 10 == 0

def detect_card_network(card_number: str) -> str:
    """Detects card network (Visa, Mastercard, Amex, RuPay)."""
    card_number = card_number.replace(" ", "").replace("-", "")
    
    if card_number.startswith('4'):
        return "visa"
    elif any(card_number.startswith(str(x)) for x in range(51, 56)):
        return "mastercard"
    elif card_number.startswith(('34', '37')):
        return "amex"
    elif card_number.startswith(('60', '65')) or any(card_number.startswith(str(x)) for x in range(81, 90)):
        return "rupay"
    
    return "unknown"

def validate_expiry(month, year):
    """Checks if the card expiry date is valid and in the future."""
    try:
        month = int(month)
        year = int(year)
        
        # Handle 4-digit year conversion (2028 -> 28)
        if year > 1000:
            year = year % 100
            
        now = datetime.now()
        current_year = now.year % 100 
        current_month = now.month
        
        if not (1 <= month <= 12):
            return False
            
        # If year is in the past
        if year < current_year:
            return False
        # If year is current but month is past
        if year == current_year and month < current_month:
            return False
            
        return True
    except (ValueError, TypeError):
        return False