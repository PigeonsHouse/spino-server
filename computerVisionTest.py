import requests
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO
import os, sys
from dotenv import load_dotenv

load_dotenv()

subscription_key = os.environ.get('SUBSCRIPTION_KEY')
endpoint = os.environ.get('AZURE_ENDPOINT')

image_url = "https://images.unsplash.com/photo-1548247416-ec66f4900b2e"

analyze_url = endpoint + "vision/v3.1/analyze"

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {'visualFeatures': 'Description', 'language': 'ja'}
data = {'url': image_url}
response = requests.post(analyze_url, headers=headers,
                         params=params, json=data)
response.raise_for_status()

analysis = response.json()
print(json.dumps(response.json(), ensure_ascii=False))