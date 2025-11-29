# storage.py
import json, os
from config import SAVE_FILE, LOG_FILE

# Ensure directories exist
os.makedirs(os.path.dirname(SAVE_FILE) or ".", exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)

def load_posts():
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_posts(posts):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Failed to save posts:", e)

def log_notification(entry):
    logs = []
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
    except Exception:
        logs = []
    logs.append(entry)
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Failed to write log:", e)
