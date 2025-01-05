import os
import random
import time
import requests

# Set URLs for files
ACC_URL = "https://raw.githubusercontent.com/Preasx24/...../refs/heads/main/ACC.txt"
VOUCHER_URL = "https://raw.githubusercontent.com/Preasx24/D-TECH_CHAT/refs/heads/main/voucher.txt"

# Temporary files to store fetched data
ACC_FILE = "ACC.txt"
VOUCHER_FILE = "voucher_used.txt"
LAST_ACCESS_FILE = "last_access.txt"

# Function to add a cool loading effect
def loading_effect(message):
    print(f"\033[1;35m{message}", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("\033[0m")

# Fetch exactly 3 Crunchyroll accounts
def fetch_accounts():
    loading_effect("Fetching Crunchyroll accounts")
    response = requests.get(ACC_URL)
    accounts = response.text.strip().splitlines()
    
    # Select only 3 random accounts
    selected_accounts = random.sample(accounts, 3)
    
    with open(ACC_FILE, "w") as f:
        for account in selected_accounts:
            f.write(account + "\n")
    
    return selected_accounts

# Display the fetched account(s) for 5 minutes
def display_accounts_for_5_minutes(accounts):
    for account in accounts:
        print(f"\033[1;32mHere is your free Crunchyroll account: \033[1;37m{account}\033[0m")
    print("\033[1;33mYou have 5 minutes to copy the accounts. \033[0m")
    
    start_time = time.time()
    while time.time() - start_time < 300:  # 5 minutes (300 seconds)
        time.sleep(1)  # Keeps the script running while showing the account

    print("\033[1;31mTime's up! You can now request a new account or exit.\033[0m")

# Check if voucher is valid
def check_voucher(voucher):
    print("\033[1;36mChecking voucher...\033[0m")
    response = requests.get(VOUCHER_URL)
    if voucher in response.text:
        print("\033[1;32mVoucher is valid! ✅\033[0m")
        return True
    else:
        print("\033[1;31mInvalid voucher! ❌\033[0m")
        return False

# Give user 3 accounts with a voucher
def give_3_accounts(voucher):
    if check_voucher(voucher):
        print("\033[1;35mFetching 3 Crunchyroll accounts...\033[0m")
        accounts = fetch_accounts()

        # Check if any of the accounts has already been used
        with open(VOUCHER_FILE, "r") as f:
            used_accounts = f.readlines()

        valid_accounts = []
        for account in accounts:
            if account + "\n" not in used_accounts:
                valid_accounts.append(account)
        
        # If any accounts are unused, display them
        if len(valid_accounts) > 0:
            display_accounts_for_5_minutes(valid_accounts)

            # Save the accounts as used
            with open(VOUCHER_FILE, "a") as f:
                for acc in valid_accounts:
                    f.write(acc + "\n")

            print("\033[1;32mYou have received 3 accounts using your voucher! 🎉\033[0m")
        else:
            print("\033[1;31mAll accounts have already been used. Try again later. ❌\033[0m")
    else:
        print("\033[1;31mVoucher is invalid. No accounts granted. ❌\033[0m")

# Check if it's been 6 hours since last access
def check_time_interval():
    if not os.path.exists(LAST_ACCESS_FILE):
        with open(LAST_ACCESS_FILE, "w") as f:
            f.write(str(time.time()))
        print("\033[1;32mFirst time using the script. You can get a free account!\033[0m")
        return True
    
    with open(LAST_ACCESS_FILE, "r") as f:
        last_access_time = float(f.read().strip())
    
    current_time = time.time()
    
    # Check if 6 hours (21600 seconds) have passed
    if current_time - last_access_time >= 21600:
        print("\033[1;32m6 hours have passed, you can get a free account! 🕒\033[0m")
        with open(LAST_ACCESS_FILE, "w") as f:
            f.write(str(current_time))
        return True
    else:
        remaining_time = 21600 - (current_time - last_access_time)
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60
        
        print(f"\033[1;31mYou need to wait for {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds before requesting another free account. ⏳\033[0m")
        time.sleep(5)  # Give them enough time to read the message
        return False

# Main menu for users
def main_menu():
    while True:
        os.system('clear')
        print("\033[1;36m=====================================\033[0m")
        print("\033[1;32m        D-TECH Crunchyroll \033[0m")
        print("\033[1;35m       Premium Account Grabber\033[0m")
        print("\033[1;36m=====================================\033[0m")
        print("\033[1;33m1. Get a free Crunchyroll account (every 6 hours)\033[0m")
        print("\033[1;33m2. Get 3 free accounts with a voucher \033[0m")
        print("\033[1;31m3. Exit\033[0m")
        
        choice = input("\033[1;37mPlease select an option: \033[0m")
        
        if choice == "1":
            if check_time_interval():
                fetch_accounts()
                give_account()
        elif choice == "2":
            voucher = input("\033[1;37mEnter your D-TECH voucher: \033[0m")
            if check_voucher(voucher):  # Skip time check for voucher usage
                fetch_accounts()
                give_3_accounts(voucher)
            else:
                print("\033[1;31mInvalid voucher! ❌\033[0m")
                time.sleep(2)  # Pause for a moment before showing the menu again
        elif choice == "3":
            print("\033[1;32mExiting... Thanks for using D-TECH!\033[0m")
            break
        else:
            print("\033[1;31mInvalid option. Please try again. ❌\033[0m")

# Start the script
if __name__ == "__main__":
    main_menu()
