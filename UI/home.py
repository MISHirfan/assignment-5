# File: SecureDataEncryptionSystem/ui/home.py

import streamlit as st

def show_home_page():
    """
    Display the Home Page with a welcome message and navigation instructions.
    """
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to *securely store and retrieve data* using unique passkeys.")
    st.write("Navigate using the sidebar to:")
    st.write("- *Store Data*: Encrypt and save your data.")
    st.write("- *Retrieve Data*: Decrypt and view your data.")