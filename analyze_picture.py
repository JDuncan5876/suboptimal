import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

# Load credentials
credentials = service_account.Credentials. from_service_account_file('suboptimal-dbf800ff4b45.json')

# Instantiates a client
client = vision.ImageAnnotatorClient(credentials=credentials)

file_name = os.path.join(
    os.path.dirname(__file__),
    'image6.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

print('Texts:')
for text in texts:
    print('\n"{}"'.format(text.description))
