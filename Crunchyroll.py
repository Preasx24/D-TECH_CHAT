import os
import time
import requests
import uuid
from datetime import datetime, timedelta

# Paths
VOUCHER_URL = "https://raw.githubusercontent.com/Preasx24/D-TECH_CHAT/refs/heads/main/voucher.txt"
USED_VOUCHERS_FILE = "used.txt"
AUTH_LOG = "auth_log.txt"

# Function to clear the screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Play audio file
def play_audio(file_name):
    if os.path.exists(file_name):
        os.system(f"termux-media-player play {file_name}")
    else:
        print("[ERROR] Audio file not found.")

# Check if a voucher exists in the remote file
def is_valid_voucher(voucher):
    try:
        response = requests.get(VOUCHER_URL)
        response.raise_for_status()
        valid_vouchers = response.text.splitlines()
        return voucher in valid_vouchers
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch vouchers: {e}")
        return False

# Check if voucher is already used
def is_voucher_used(voucher):
    if os.path.exists(USED_VOUCHERS_FILE):
        with open(USED_VOUCHERS_FILE, "r") as file:
            used_vouchers = file.read().splitlines()
        return voucher in used_vouchers
    return False

# Mark voucher as used
def use_voucher(voucher):
    with open(USED_VOUCHERS_FILE, "a") as file:
        file.write(f"{voucher}\n")

# Save authentication log
def save_auth_log():
    expiration_time = datetime.now() + timedelta(hours=24)
    with open(AUTH_LOG, "w") as file:
        file.write(str(expiration_time))

# Check if authentication is still valid
def is_auth_valid():
    if os.path.exists(AUTH_LOG):
        with open(AUTH_LOG, "r") as file:
            expiration_time = datetime.fromisoformat(file.read().strip())
        return datetime.now() < expiration_time
    return False

# Main authentication process
def authenticate():
    if is_auth_valid():
        print("[INFO] Authentication already valid. Proceeding...")
        return True

    clear_screen()
    print("[INFO] Welcome to the D-TECH Tool!")
    voucher = input("[INPUT] Enter your voucher code: ").strip()

    if not is_valid_voucher(voucher):
        print("[ERROR] Invalid voucher code. Please try again.")
        return False

    if is_voucher_used(voucher):
        print("[ERROR] Voucher has already been used. Please use a new one.")
        return False

    print("[INFO] Authentication successful. Preparing access...")
    use_voucher(voucher)
    save_auth_log()

    # Play the audio file
    play_audio("arise.mp3")
    return True

# Main tool function
def main_tool():
    print("[INFO] Access granted to the main tool.")
    print("Your tool functionality goes here!")
    # Add your tool functionality below
    time.sleep(2)

# Main script execution
def main():
    if authenticate():
        main_tool()
    else:
        print("[ERROR] Authentication failed. Exiting...")

if __name__ == "__main__":
    main()