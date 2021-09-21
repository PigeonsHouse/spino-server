from cruds import posts
from db import models, get_db
from schemas.users import BaseUser
from sqlalchemy.orm.session import Session
from fastapi import Depends
from cruds.posts import get_post_rank, get_posts_me_by_limit, delete_post_by_id
from cruds.users import get_current_user_id
from fastapi import APIRouter

post_router = APIRouter()

@post_router.get('/posts/me')
def posts_me(limit: int = 30, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    posts_me = get_posts_me_by_limit(db, current_user_id, limit)
    for post_me in posts_me:
        post_me.rank = get_post_rank(db, post_me.id)
    return posts_me

@post_router.delete('/posts/{post_id}', response_model=bool)
def delete_post(post_id: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    result = delete_post_by_id(db, post_id, user_id)
    return result