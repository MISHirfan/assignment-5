# File: ui/store_data.py

import streamlit as st
from core.storage import store_data, get_data
from core.encryption import encrypt_data
from core.validation import validate_passkey

def show_store_data_page():
    # Apply custom CSS
    with open("styles/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.subheader("📂 Store Data Securely")

    cipher_choice = st.radio("Encryption Method:", ["Fernet", "Caesar Cipher"], key="cipher_choice")
    persistent = st.checkbox("💾 Enable Persistent Storage (JSON File)", key="store_persist", value=False)
    
    user_data = st.text_area("Enter Data:", key="store_data_input")
    passkey = st.text_input("Enter Passkey:", type="password", key="store_passkey")

    if st.button("Encrypt & Save"):
        is_valid, error_msg = validate_passkey(passkey)

        if not is_valid:
            st.error(f"⚠️ {error_msg}")
        elif user_data:
            encrypted_text = encrypt_data(user_data, passkey, use_caesar=(cipher_choice == "Caesar Cipher"))
            if encrypted_text:
                success = store_data(encrypted_text, passkey, use_persistence=persistent)
                if success:
                    stored_entry = get_data(encrypted_text, use_persistence=persistent)
                    st.success(f"✅ Data stored at {stored_entry['timestamp']}")
                else:
                    st.error("⚠️ Failed to store data!")
            else:
                st.error("⚠️ Encryption failed!")
        else:
            st.error("⚠️ Data field is required!")