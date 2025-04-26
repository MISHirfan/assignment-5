# File: SecureDataEncryptionSystem/core/validation.py

import re

def validate_passkey(passkey: str) -> tuple[bool, str]:
    """
    Validate passkey for length and special characters.
    
    Args:
        passkey (str): The passkey to validate.
    
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not passkey:
        return False, "Passkey cannot be empty."
    if len(passkey) < 8:
        return False, "Passkey must be at least 8 characters long."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', passkey):
        return False, "Passkey must contain at least one special character."
    return True, ""