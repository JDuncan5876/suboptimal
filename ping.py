import os
import time

def wait_for_connection():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)

    while (response != 0):
        time.sleep(0.05)
        response = os.system("ping -c 1 " + hostname)

if __name__ == "__main__":
    wait_for_connection()
