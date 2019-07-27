import io
import os
import string

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

if __name__ == "__main__":
    file_name = os.path.join(
        os.path.dirname(__file__),
        '/home/pi/42st.jpg')
    print(analyze_image(file_name))

