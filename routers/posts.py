from cruds import posts
from db import models, get_db
from schemas.users import BaseUser
from sqlalchemy.orm.session import Session
from fastapi import Depends
from cruds.posts import get_post_rank, get_posts_me, delete_post_by_id
from cruds.users import get_current_user_id
from fastapi import APIRouter

post_router = APIRouter()

@post_router.get('/posts/me')
def posts_me(db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    posts_me = get_posts_me(db, current_user_id)
    for post_me in posts_me:
        post_me.rank_post = get_post_rank(db, post_me.id)
    return posts_me

@post_router.delete('/posts/{post_id}', response_model=bool, dependencies=[Depends(get_current_user_id)])
def delete_post(post_id: str, db: Session = Depends(get_db)):
    result = delete_post_by_id(db, post_id)
    return result