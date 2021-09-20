from sqlalchemy.orm import Session
from db import models
from schemas.posts import Post

def _get_posts_me(db: Session, id: str) -> Post:
    post_orm = db.query(models.Post).filter(models.Post.user_id == id).all()
    print(post_orm)
    if len(post_orm) == 0:
        return None
    return Post.from_orm(post_orm)