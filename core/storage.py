import streamlit as st
import hashlib
import json
import os
from datetime import datetime

# In-memory data storage
in_memory_data = {}

JSON_FILE = "data/encrypted_data.json"

def hash_passkey_pdkdf2(passkey: str) -> str:
    salt = b'secure_salt'
    return hashlib.pbkdf2_hmac('sha256', passkey.encode(), salt, 100000).hex()

def store_data(encrypted_text: str, passkey: str, use_persistence=False) -> bool:
    if not encrypted_text or not passkey:
        return False

    user_key = f"{st.session_state.current_user}_{encrypted_text}"
    hashed_passkey = hash_passkey_pdkdf2(passkey)
    entry = {
        "encrypted_text": encrypted_text,
        "passkey": hashed_passkey,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if use_persistence:
        stored_data = load_data()
        stored_data[user_key] = entry
        save_data_to_file(stored_data)
    else:
        in_memory_data[user_key] = entry

    return True

def get_data(encrypted_text: str, use_persistence=False) -> dict | None:
    user_key = f"{st.session_state.current_user}_{encrypted_text}"

    if use_persistence:
        stored_data = load_data()
        return stored_data.get(user_key)
    else:
        return in_memory_data.get(user_key)

def load_data() -> dict:
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, "r") as file:
        return json.load(file)

def save_data_to_file(data: dict):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)