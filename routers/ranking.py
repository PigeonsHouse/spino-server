from cruds.users import get_current_user_id
from cruds.posts import get_posts_by_limit
from schemas.posts import Post
from typing import List
from db import get_db
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

ranking_router = APIRouter()

@ranking_router.get('/ranking/posts', response_model=List[Post], dependencies=[Depends(get_current_user_id)])
def get_posts_ranking(limit: int = 30, db: Session = Depends(get_db)):
    ranking = get_posts_by_limit(db, limit)
    return ranking