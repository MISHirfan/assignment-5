# File: SecureDataEncryptionSystem/ui/user_auth.py

import streamlit as st

def show_user_auth_page():
    """
    Display user authentication page for login/registration.
    """
    st.subheader("👤 User Authentication")
    username = st.text_input("Username", key="auth_username")
    password = st.text_input("Password", type="password", key="auth_password")
    
    if 'users' not in st.session_state:
        st.session_state.users = {"admin": "admin123"}  # Simple in-memory user store
    
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.current_user = username
            st.session_state.authenticated = True
            st.session_state.page = "Home"
            st.success(f"✅ Logged in as {username}")
            st.rerun()
        else:
            st.error("❌ Invalid credentials!")
    
    if st.button("Register"):
        if username and password and username not in st.session_state.users:
            st.session_state.users[username] = password
            st.success(f"✅ Registered {username}")
        else:
            st.error("⚠️ Username taken or fields empty!")