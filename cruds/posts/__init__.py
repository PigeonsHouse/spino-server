from db import models
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

def image_post_google(image_url: str) -> List[str]:
    image.source.image_uri = image_url
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return_list = []
    if len(labels) == 0:
        raise HTTPException(400, 'We can not access the URL currently. Please download the content and pass it in.')
    for label in labels:
        new_list = label.description.split(' ')
        return_list.extend(new_list)
    print(return_list)
    return return_list

def scoring_word(image_words: List[str]) -> float:
    point = 0
    results = []
    for image_word in image_words:
        try:
            results = model.wv.most_similar(positive=[image_word], topn=20)
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
        return point / len(results)
    else:
        return point

def set_score_for_db(db: Session, user_id: str, score: float, image_url: str):
    post_orm = models.Post(
        user_id = user_id,
        point = score,
        image_url = image_url
    )
    db.add(post_orm)
    db.commit()
    db.refresh(post_orm)
    return Post.from_orm(post_orm)

def get_posts_me(db: Session, id: str) -> Post:
    post_orms = db.query(models.Post).filter(models.Post.user_id == id).all()
    print(post_orms)
    posts = []
    if len(post_orms) == 0:
        return None
    for post_orm in post_orms:
        posts.append(Post.from_orm(post_orm))
    return posts
