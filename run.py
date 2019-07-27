import io
import time
import os
import string
import sys
import random
import subprocess
import stringdist

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
    print(text)
    cmd = "say \"{}\"".format(text)
    subprocess.call(cmd, shell=True)


def take_picture():
    n = random.randint(0, 100000)
    path = "/tmp/" + str(n) + ".jpg"
    cmd = "raspistill -o " + path
    print(cmd)
    subprocess.call(cmd, shell=True)
    return path

def match_station(input_text):
    station_map = {
	    'canalst': 'Canal St',
	    'canalstreet': 'Canal St',
	    'canalstreetstation': 'Canal St',
	    '42ndstportauthoritybusterm': '42nd St - Port Authority Bus Terminal',
	    '42ndst': '42nd St - Port Authority Bus Terminal',
	    '42ndstreet': '42nd St - Port Authority Bus Terminal',
	    'portauthority': '42nd St - Port Authority Bus Terminal',
	    'busterminal': '42nd St - Port Authority Bus Terminal',
	    'pennstation': '34th St - Penn Station',
	    'chambers': 'Chambers St',
	    'chambersst': 'Chambers St',
            'chambersstreet': 'Chambers St',
	    '23rdst': '23rd St',
	    '23rdstreet': '23rd St',
	    'courtsq': 'Court Sq',
	    'columbuscircle': '59th St - Columbus Circle',
	    'springst': 'Spring St',
	    'fultonst': 'Fulton St',
	    'worldtradecenter': 'World Trade Center',
            '14thst': '14th Street Station',
            '14thstreet': '14th Street Station',
            '14thstreetstation': '14th Street Station',
            'washingtonsquare': 'West 4th Street - Washington Square Station',
            'west4street': 'West 4th Street - Washington Square Station',
            'west4streetwashingtonsquare': 'West 4th Street - Washington Square Station'
	}
    station_map_list = [(k, v) for k, v in station_map.items()]
    return [i[1] for i in sorted(station_map_list, key=lambda x:stringdist.levenshtein_norm(x[0], input_text))][0]

def get_score(input_text):
    station_map = {
	    'canalst': 'Canal St',
	    'canalstreet': 'Canal St',
	    '42ndstportauthoritybusterm': '42nd St - Port Authority Bus Terminal',
	    '42ndst': '42nd St - Port Authority Bus Terminal',
	    '42ndstreet': '42nd St - Port Authority Bus Terminal',
	    'portauthority': '42nd St - Port Authority Bus Terminal',
	    'busterminal': '42nd St - Port Authority Bus Terminal',
	    'pennstation': '34th St - Penn Station',
	    'chambers': 'Chambers St',
	    'chambersst': 'Chambers St',
            'chambersstreet': 'Chambers St',
	    '23rdst': '23rd St',
	    '23rdstreet': '23rd St',
	    'courtsq': 'Court Sq',
	    'columbuscircle': '59th St - Columbus Circle',
	    'springst': 'Spring St',
	    'fultonst': 'Fulton St',
	    'worldtradecenter': 'World Trade Center',
            '14thst': '14th Street Station',
            '14thstreet': '14th Street Station',
            '14thstreetstation': '14th Street Station',
            'washingtonsquare': 'West 4th Street - Washington Square Station',
            'west4street': 'West 4th Street - Washington Square Station',
            'west4streetwashingtonsquare': 'West 4th Street - Washington Square Station'
	}
    station_map_list = [(k, v) for k, v in station_map.items()]
    return [stringdist.levenshtein_norm(i[0], input_text) for i in sorted(station_map_list, key=lambda x:stringdist.levenshtein_norm(x[0], input_text))][0]

def main():
    wait_for_connection()
    f = take_picture()
    print("got image")
    text = analyze_image(f)
    print(text)
    best_match = match_station(text)
    print(best_match)
    say("You are arriving at " + best_match)
    time.sleep(0.5)
    say("Prepare to exit at the next stop")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--loop':
        while True:
            main()
    else:
        main()
