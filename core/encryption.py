# File: SecureDataEncryptionSystem/core/encryption.py

from cryptography.fernet import Fernet
import hashlib

ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

def hash_passkey_pdkdf2(passkey: str) -> str:
    salt = b'secure_salt'
    return hashlib.pbkdf2_hmac('sha256', passkey.encode(), salt, 100000).hex()

def caesar_encrypt(text: str, shift: int = 3) -> str:
    """
    Encrypt text using Caesar cipher with a fixed shift.
    """
    result = ""
    for char in text:
        if char.isalpha():
            ascii_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - ascii_base + shift) % 26 + ascii_base)
        else:
            result += char
    return result

def caesar_decrypt(text: str, shift: int = 3) -> str:
    """
    Decrypt text using Caesar cipher with a fixed shift.
    """
    return caesar_encrypt(text, -shift)

def encrypt_data(text: str, passkey: str, use_caesar: bool = False) -> str:
    if not text or not passkey:
        return None
    if use_caesar:
        return caesar_encrypt(text)
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text: str, passkey: str, stored_hashed_passkey: str, use_caesar: bool = False) -> str | None:
    if not encrypted_text or not passkey:
        return None
    hashed_passkey = hash_passkey_pdkdf2(passkey)
    if hashed_passkey == stored_hashed_passkey:
        try:
            if use_caesar:
                return caesar_decrypt(encrypted_text)
            return cipher.decrypt(encrypted_text.encode()).decode()
        except Exception:
            return None
    return None