import requests
from pprint import pprint
import os

from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "apiKey": os.environ.get('API_KEY'),
    "authDomain": os.environ.get('AUTHDO_MAIN'),
    "projectId": os.environ.get('PROJECT_ID'),
    "storageBucket": os.environ.get('STORAGE_BUCKET'),
    "messagingSenderId": os.environ.get('MESSAGING_SENDER_ID'),
    "appId": os.environ.get('APP_ID'),
    "measurementId": os.environ.get('MEASUREMENT_ID')
}
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')


def main():
    api_key = CONFIG["apiKey"]
    uri = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
    data = {"email": EMAIL, "password": PASSWORD, "returnSecureToken": True}

    result = requests.post(url=uri, data=data)

    user = result.json()

    pprint(user)
    print(user['idToken'])


if __name__ == '__main__':
    main()