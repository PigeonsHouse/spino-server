from cruds.users import get_current_user_id
from cruds.posts import image_post_google, scoring_word, set_score_for_db
from schemas.posts import CreatingPost, Post
from db import get_db
from fastapi import APIRouter
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
import statistics

scoring_router = APIRouter()

@scoring_router.post('/scoring', response_model=Post)
def post_scoring(payload: CreatingPost, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    print("start scoring")
    image_responce = image_post_google(payload.image_url)
    result_score = scoring_word(image_responce)
    post = set_score_for_db(db, user_id, result_score, payload.image_url)
    return post
