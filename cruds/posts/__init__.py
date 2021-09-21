from sqlalchemy.sql.expression import desc
from db import models
from typing import List
from sqlalchemy.orm.session import Session
from schemas.posts import Post
import os
from fastapi import HTTPException
from google.cloud import vision
from gensim.models import word2vec
from firebase_admin import storage
from datetime import timedelta

client = vision.ImageAnnotatorClient()
image = vision.Image()
model = word2vec.Word2Vec.load('word2vec_summer_1.model')

mainus_word_list = ['Snow']

subscription_key = os.environ.get('SUBSCRIPTION_KEY')
endpoint = os.environ.get('AZURE_ENDPOINT')

def image_post_google(image_url: str) -> List[str]:
    request_counter = 0
    image.source.image_uri = image_url
    return_list = []
    while request_counter < 3 :
        response = client.label_detection(image=image)
        labels = response.label_annotations
        if len(labels) != 0:
            break
        request_counter += 1
    print(request_counter)
    if len(labels) == 0:
        raise HTTPException(400, 'We can not access the URL currently. Please download the content and pass it in.')
    for label in labels:
        new_list = label.description.split(' ')
        return_list.extend(new_list)
    return return_list

def scoring_word(image_words: List[str]) -> float:
    add_score = 0
    fil = word_filter(image_words)
    if fil == True:
        add_score = 0
        return 0
    each_score = []
    results = []
    for b in image_words:
        match_word_num = 0
        score_of_one_word = 0
        try:
            results = model.wv.most_similar(positive=[b], topn=20)
        except:
            continue

        for a in results:
            if a[0] in image_words:
                match_word_num += 1
                score_of_one_word += a[1] * 10
        score_element = {'match_word_num': match_word_num, 'score_of_one_word': score_of_one_word}
        each_score.append(score_element)
    
    result_score = _max_match_raito(each_score)
    b = result_score + add_score
    return b * b / 20

def word_filter(image_words: List[str]) -> bool:
    if mainus_word_list[0] in image_words:
        print("減点")
        return True

    return False

def _max_match_raito(each_score: List[dict]) -> float:
    max_point = 10
    max_raito = -1
    for index in each_score:
        if index['match_word_num'] > max_raito:
            max_point = index['score_of_one_word']
            max_raito = index['match_word_num']

    return max_point

def set_score_for_db(db: Session, user_id: str, score: float, image_url: str) -> Post:
    post_orm = models.Post(
        user_id = user_id,
        point = score,
        image_url = image_url
    )
    db.add(post_orm)
    db.commit()
    db.refresh(post_orm)
    set_high_score_post(db, user_id, score, image_url)
    return Post.from_orm(post_orm)

def set_high_score_post(db: Session, user_id: str, score: float, image_url: str) -> Post:
    my_top_post = db.query(models.TopPost).filter(models.TopPost.user_id == user_id).first()
    
    if my_top_post is None:
        post_orm = models.TopPost(
            user_id = user_id,
            point = score,
            image_url = image_url
        )
        db.add(post_orm)
        db.commit()
        db.refresh(post_orm)
        return Post.from_orm(post_orm)
    elif my_top_post.point < score:
        post_orm = models.TopPost(
            user_id = user_id,
            point = score,
            image_url = image_url
        )
        db.add(post_orm)
        db.delete(my_top_post)
        db.commit()
        db.refresh(post_orm)
        return Post.from_orm(post_orm)

def get_posts_me_by_limit(db: Session, user_id: str, limit: int) -> List[Post]:
    post_orms = db.query(models.Post).filter(models.Post.user_id == user_id).limit(limit).all()
    posts = []
    if len(post_orms) == 0:
        return post_orms
    for post_orm in post_orms:
        posts.append(Post.from_orm(post_orm))
    return posts

def get_posts_by_limit(db: Session, limit: int) -> List[Post]:
    posts_orm = db.query(models.Post).order_by(desc(models.Post.point)).limit(limit).all()
    posts = []
    for post_orm in posts_orm:
        post = Post.from_orm(post_orm)
        posts.append(post)
    return posts

def convert_http_url_from_gs(gs_url: str) -> str:
    bucket_name = "summer-scoring-app.appspot.com"

    blob_path = gs_url[gs_url.find(bucket_name)+len(bucket_name)+1:]

    backet = storage.bucket(bucket_name)

    url = backet.blob(blob_path).generate_signed_url(expiration=timedelta(minutes=30))

    return url

def delete_post_by_id(db: Session, post_id: str) -> bool:
    delete_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if delete_post == None:
        raise HTTPException(400, 'Post not exist.')
    user_id = delete_post.user_id
    delete_top_post = db.query(models.TopPost).filter(models.TopPost.user_id == user_id).first()
    db.delete(delete_post)
    db.delete(delete_top_post)
    db.commit()
    return True

def get_post_rank(db: Session, post_id: str) -> int:
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post == None:
        raise HTTPException(400, 'Post not exist.')
    upper_post_list = db.query(models.Post).filter(models.Post.point > post.point).all()
    return 1+len(upper_post_list)
