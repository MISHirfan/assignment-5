# File: SecureDataEncryptionSystem/core/security.py

import hashlib
import time
import logging
import os  # Added to handle directory and file creation
import streamlit as st

# Ensure the 'data' directory and log file exist
os.makedirs("data", exist_ok=True)  # Create data/ folder if it doesn't exist
log_file_path = "data/error_log.txt"

# Create empty log file if it doesn't exist
if not os.path.exists(log_file_path):
    with open(log_file_path, "w") as f:
        f.write("")

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Salt and Iterations for PBKDF2
SALT = b"secure_salt"  # In real-world apps, use a unique salt per user.
ITERATIONS = 100000  # Recommended for PBKDF2

# Session timeout configuration (in seconds)
SESSION_TIMEOUT = 300  # 5 minutes
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # 5 minutes

def hash_passkey_pdkdf2(passkey: str) -> str:
    """Hash the passkey using PBKDF2 with SHA-256."""
    return hashlib.pbkdf2_hmac('sha256', passkey.encode(), SALT, ITERATIONS).hex()

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "login_time" not in st.session_state:
        st.session_state.login_time = None
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0
    if "lockout_time" not in st.session_state:
        st.session_state.lockout_time = None

def is_session_expired():
    if not st.session_state.authenticated:
        return False
    if st.session_state.login_time is None:
        return True
    return (time.time() - st.session_state.login_time) > SESSION_TIMEOUT

def is_locked_out():
    if st.session_state.lockout_time:
        if (time.time() - st.session_state.lockout_time) < LOCKOUT_DURATION:
            return True
        else:
            # Reset lockout after time has passed
            st.session_state.failed_attempts = 0
            st.session_state.lockout_time = None
            return False
    return False

def reauthorize(input_pass: str) -> bool:
    from core.storage import load_data_from_file

    stored_data = load_data_from_file()
    for key, value in stored_data.items():
        if value["passkey"] == hash_passkey_pdkdf2(input_pass):
            st.session_state.authenticated = True
            st.session_state.login_time = time.time()
            st.session_state.failed_attempts = 0
            st.session_state.page = "Retrieve Data"
            return True

    # Failed reauthorization attempt
    st.session_state.failed_attempts += 1
    logging.info("Failed reauthorization attempt.")
    if st.session_state.failed_attempts >= MAX_FAILED_ATTEMPTS:
        st.session_state.lockout_time = time.time()
        logging.warning("User locked out due to repeated failed attempts.")
    return False

def increment_failed_attempts():
    """Increment the number of failed login attempts."""
    st.session_state.failed_attempts += 1
    logging.info(f"Failed attempts: {st.session_state.failed_attempts}")
    return st.session_state.failed_attempts

def get_failed_attempts():
    """Get the current number of failed login attempts."""
    return st.session_state.failed_attempts

def check_reauthorization_required():
    """Check if reauthorization is required (based on the number of failed attempts)."""
    if st.session_state.failed_attempts >= MAX_FAILED_ATTEMPTS:
        return True
    return False

def reset_failed_attempts():
    """Reset the failed login attempts to zero."""
    st.session_state.failed_attempts = 0
    logging.info("Failed attempts reset.")

def require_auth():
    init_session_state()
    if is_locked_out():
        st.error("⛔ Too many failed attempts. Try again after 5 minutes.")
        st.stop()
    if is_session_expired():
        st.error("⏱️ Session expired. Please log in again.")
        st.session_state.authenticated = False
        st.stop()