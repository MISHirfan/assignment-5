# File: SecureDataEncryptionSystem/ui/retrieve_data.py

import streamlit as st
from core.storage import get_data
from core.encryption import decrypt_data
from core.security import increment_failed_attempts, get_failed_attempts, check_reauthorization_required, reset_failed_attempts

from core.security import require_auth

require_auth()
def show_retrieve_data_page():
    """
    Display the Retrieve Data Page to input passkey and decrypt data.
    """
    st.subheader("🔍 Retrieve Your Data")
    
    # Input fields
    encrypted_text = st.text_area("Enter Encrypted Data:", key="retrieve_encrypted_input")
    passkey = st.text_input("Enter Passkey:", type="password", key="retrieve_passkey")
    
    if st.button("Decrypt"):
        if encrypted_text and passkey:
            # Fetch stored data
            stored_entry = get_data(encrypted_text)
            if stored_entry:
                # Attempt decryption
                decrypted_text = decrypt_data(encrypted_text, passkey, stored_entry["passkey"])
                if decrypted_text:
                    reset_failed_attempts()
                    st.success(f"✅ Decrypted Data: {decrypted_text}")
                else:
                    attempts = increment_failed_attempts()
                    st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - attempts}")
                    
                    # Check if reauthorization is required
                    if check_reauthorization_required():
                        st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
                        st.session_state.page = "Login"  # For main.py navigation
            else:
                st.error("❌ No data found for this encrypted text!")
        else:
            st.error("⚠️ Both fields are required!")
    
    # Display current failed attempts
    attempts = get_failed_attempts()
    if attempts > 0:
        st.write(f"Failed attempts: {attempts}")