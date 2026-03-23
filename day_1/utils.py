from storage import load_users, save_users
from logger import log_message

MAX_LOGIN_ATTEMPTS = 3

def register_user():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        log_message("ERROR", "Registration failed — empty input.")
        return

    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            print(f"User '{username}' already exists.")
            log_message("WARNING", f"Duplicate registration attempt for '{username}'.")
            return

    data["users"].append({"username": username, "password": password})
    save_users(data)
    print(f"User '{username}' registered successfully.")
    log_message("INFO", f"User '{username}' registered successfully.")


def login_user():
    username = input("Enter username: ").strip()
    attempts = 0

    while attempts < MAX_LOGIN_ATTEMPTS:
        password = input("Enter password: ").strip()
        data = load_users()

        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                print(f"Login successful. Welcome, {username}!")
                log_message("INFO", f"User '{username}' logged in successfully.")
                return

        attempts += 1
        remaining = MAX_LOGIN_ATTEMPTS - attempts
        log_message("ERROR", f"Failed login attempt for user '{username}'.")

        if remaining > 0:
            print(f"Invalid credentials. {remaining} attempt(s) remaining.")
        else:
            print("Account locked after 3 failed attempts.")
            log_message("WARNING", f"Account locked for user '{username}' after 3 failed attempts.")


def view_users():
    data = load_users()
    if not data["users"]:
        print("No users found.")
    else:
        print("\n--- Registered Users ---")
        for user in data["users"]:
            print(f"  - {user['username']}")
        print("------------------------")
    log_message("INFO", "User list accessed.")


def delete_user():
    username = input("Enter username to delete: ").strip()
    data = load_users()

    for user in data["users"]:
        if user["username"] == username:
            data["users"].remove(user)
            save_users(data)
            print(f"User '{username}' deleted successfully.")
            log_message("INFO", f"User '{username}' deleted successfully.")
            return

    print(f"User '{username}' not found.")
    log_message("ERROR", f"Attempted to delete non-existing user '{username}'.")
