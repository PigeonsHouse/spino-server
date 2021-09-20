from cruds import posts
from db import models, get_db
from schemas.users import BaseUser
from sqlalchemy.orm.session import Session
from fastapi import Depends
from cruds.posts import get_posts_me
from cruds.users import get_current_user_id
from fastapi import APIRouter

post_router = APIRouter()

@post_router.get('/posts/me')
def posts_me(db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    posts_me = get_posts_me(db, current_user_id)
    return posts_me