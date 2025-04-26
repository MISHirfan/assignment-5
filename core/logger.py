# File: core/logger.py
import logging
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="data/error_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message: str):
    logging.info(message)

def log_warning(message: str):
    logging.warning(message)

def log_error(message: str):
    logging.error(message)