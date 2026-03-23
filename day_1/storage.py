import json
import os
from logger import log_message

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        save_users({"users": []})
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_message("ERROR", "Corrupted JSON file. Resetting storage.")
        save_users({"users": []})
        return {"users": []}

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
