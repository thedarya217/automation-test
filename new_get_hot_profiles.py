import requests
import time
from datetime import datetime
import sys

url = "https://api.pantel.me/a/get_hot_profiles?$=bc4a32be16e8fff86487e32a26db9513&users"

def get_hot_profiles():
    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(url)
            print(f"HTTP Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                users = data.get('hot_profiles', [])
                if not users:
                    print("No users found in the response")
                    return None

                max_expiration_user = None
                max_expiration_date = None

                for user in users:
                    username = f"{user.get('first_name')} {user.get('last_name')}"
                    expiration_date_float = user.get('expiration_date')

                    if expiration_date_float is None:
                        print(f"Expiration date not found for user {username}")
                        continue

                    expiration_date = datetime.utcfromtimestamp(expiration_date_float)

                    #print(f"User: {username}, Expiration Date: {expiration_date}")

                    if max_expiration_date is None or expiration_date > max_expiration_date:
                        max_expiration_date = expiration_date
                        max_expiration_user = username

                return max_expiration_user, max_expiration_date
            else:
                print(f"Error: {response.status_code}")
                time.sleep(5)  # wait before retrying

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(5)  # wait before retrying

    return None

def main():
    previous_user = None
    while True:
        try:
            result = get_hot_profiles()

            if result:
                max_expiration_user, max_expiration_date = result

                if previous_user:
                    if previous_user == max_expiration_user:
                        print(
                            f"Error: Same user {max_expiration_user} with expiration date {max_expiration_date} appears again.")
                        break
                previous_user = max_expiration_user
                print(f"The user with the latest expiration date is: {max_expiration_user} with expiration date: {max_expiration_date}")

            print("\nWaiting for 15 minutes before checking again...")
            time.sleep(1 * 60)  # Wait for 15 minutes

        except KeyboardInterrupt:
            print("Program interrupted by user. Exiting...")
            sys.exit(0)

# Start the program
main()
