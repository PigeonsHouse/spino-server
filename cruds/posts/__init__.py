from db import models
from schemas.ComputerVision import ComputerVisionResponse
from typing import List
from sqlalchemy.orm.session import Session
from schemas.posts import Post
import os
import requests, json
from fastapi import HTTPException
from google.cloud import vision
from gensim.models import word2vec

client = vision.ImageAnnotatorClient()
image = vision.Image()
model = word2vec.Word2Vec.load('word2vec.model')

subscription_key = os.environ.get('SUBSCRIPTION_KEY')
endpoint = os.environ.get('AZURE_ENDPOINT')

def image_scoring(images_url: List[str]) -> List[List[str]]:
    return list(map(image_post_google, images_url))

def image_post_google(image_url: str) -> List[str]:
    image.source.image_uri = image_url
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return_list = []
    for label in labels:
        new_list = label.description.split(' ')
        return_list.extend(new_list)
    print(return_list)
    return return_list

def scoring_word(responses: List[List[str]]) -> float:
    finally_score = 0
    for image_words in responses:
        point = 0
        results = []
        for b in image_words:
            try:
                results = model.wv.most_similar(positive=[b], topn=20)
                print('=====results====')
                print(results)
            except:
                print('=====減点====')
                point -= 1000
                continue

            for a in results:
                if a[0] in image_words:
                    point += a[1] * 1000
                else:
                    point -= a[1] * 100
        if len(results):
            finally_score += point / len(results)
        else:
            finally_score += point
    return finally_score / len(responses)

def set_score_for_db(db: Session, user_id: str, score: float):
    post_orm = models.Post(
        user_id = user_id,
        point = score
    )
    db.add(post_orm)
    db.commit()
    db.refresh(post_orm)
    return Post.from_orm(post_orm)

def set_images_for_db(db: Session, post_id: str, images_url: List[str]):
    for image_url in images_url:
        image_orm = models.Image(
            post_id = post_id,
            url = image_url
        )
        db.add(image_orm)
        db.commit()
        db.refresh(image_orm)

def get_posts_me(db: Session, id: str) -> Post:
    post_orms = db.query(models.Post).filter(models.Post.user_id == id).all()
    print(post_orms)
    posts = []
    if len(post_orms) == 0:
        return None
    for post_orm in post_orms:
        posts.append(Post.from_orm(post_orm))
    return posts
