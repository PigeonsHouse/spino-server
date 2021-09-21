from fastapi.exceptions import HTTPException
from firebase_strage_adaptor import convert_http_url_from_gs
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
def post_scoring(payload: CreatingPost, product: bool = True, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    image_url = payload.image_url
    if product:
        if image_url[:2] != 'gs':
            raise HTTPException(status_code=400, detail="image_url's type is wrong")
        image_url = convert_http_url_from_gs(image_url)
    else:
        if image_url[:4] != 'http':
            raise HTTPException(status_code=400, detail="image_url's type is wrong")
    image_responce = image_post_google(image_url)
    result_score = scoring_word(image_responce)
    post = set_score_for_db(db, user_id, result_score, image_url)
    return post
