import os
import time
hostname = "google.com"
response = os.system("ping -c 1 " + hostname)

while (response != 0):
    time.sleep(0.05)
    response = os.system("ping -c 1 " + hostname)

        # Run Scripts.
