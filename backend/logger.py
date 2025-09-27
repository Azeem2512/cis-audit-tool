# backend/logger.py
import os
import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def log_error(message: str) -> str:
    """
    Write an error message to a timestamped log file and return the path.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"errors_{timestamp}.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(message)
    return log_file
