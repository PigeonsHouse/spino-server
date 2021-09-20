from cruds.users import get_current_user_id
from cruds.posts import image_scoring, scoring_word, set_images_for_db, set_score_for_db
from typing import List
from pydantic import HttpUrl
from schemas.posts import Post
from db import get_db
from fastapi import APIRouter
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
import statistics

scoring_router = APIRouter()

@scoring_router.post('/scoring', response_model=Post)
def post_scoring(payload: List[HttpUrl], db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    image_responces = image_scoring(payload)
    score_list = list(map(scoring_word, image_responces))
    result_score = statistics.mean(score_list)
    post = set_score_for_db(db, user_id, result_score)
    set_images_for_db(db, post.id, payload)
    return post