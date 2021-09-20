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
    each_score = []
    
    results = []
    for b in image_words:
        match_word_num = 0
        score_of_one_word = 0
        try:
            results = model.wv.most_similar(positive=[b], topn=20)
            print('=====results====')
            print(results)
        except:
            print(results)
            print('============')
            continue

        for a in results:
            if a[0] in image_words:
                match_word_num += 1
                score_of_one_word += a[1] * 100
                print("a")
        score_element = {'match_word_num': match_word_num, 'score_of_one_word': score_of_one_word}
        each_score.append(score_element)
        print(each_score)
    print("new_scorering")
                    
    return _max_match_raito(each_score)

def _max_match_raito(each_score: List[dict]):
    max_point = 10
    max_raito = -1
    for index in each_score:
        if index['match_word_num'] > max_raito:
            max_point = index['score_of_one_word']
            max_raito = index['match_word_num']
    
    return max_point

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
