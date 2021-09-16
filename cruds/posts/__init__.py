from schemas.ComputerVision import ComputerVisionResponse
from typing import List
from sqlalchemy.orm.session import Session
from schemas.posts import Post
import os
import requests, json
from fastapi import HTTPException

subscription_key = os.environ.get('SUBSCRIPTION_KEY')
endpoint = os.environ.get('AZURE_ENDPOINT')

def image_scoring(images_url: List[str]) -> List[ComputerVisionResponse]:
    return list(map(image_post_azure, images_url))

def image_post_azure(image_url: str) -> ComputerVisionResponse:
    analyze_url = endpoint + "vision/v3.1/analyze"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'visualFeatures': 'Description', 'language': 'en'}
    data = {'url': image_url}

    try:
        response = requests.post(analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        print(response.json())

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="cannot get responce")

