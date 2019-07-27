import io
import time
import os
import string
import sys
import random
import subprocess

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

def strip_text(text):
    return "".join([i for i in text.replace("\n", "").lower() if i in string.ascii_lowercase or i in string.digits])

def analyze_image(file_name):
    # Load credentials
    credentials = service_account.Credentials. from_service_account_file('/home/pi/suboptimal-dbf800ff4b45.json')

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return strip_text(texts[0].description) if len(texts) > 0 else ""

def wait_for_connection():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    while (response != 0):
        time.sleep(0.05)
        response = os.system("ping -c 1 " + hostname)

def say(text):
    cmd = "say \"{}\"".format(text)
    subprocess.call(cmd, shell=True)


def take_picture():
    n = random.randint(0, 100000)
    path = "/tmp/" + str(n) + ".jpg"
    cmd = "raspistill -o " + path
    print(cmd)
    subprocess.call(cmd, shell=True)
    return path

def main():
    wait_for_connection()
    f = take_picture()
    text = analyze_image(f)
    print(text)
    say(text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--loop':
        while True:
            main()
    else:
        main()
