from sqlalchemy.sql.expression import desc
from db import models
from sqlalchemy.orm.session import Session
from schemas.users import RankingUser

def get_user_rank_by_limit(db: Session, limit: int):
    top_user_post_list = db.query(models.TopPost).order_by(desc(models.TopPost.point)).limit(limit).all()
    ranking_user = []
    for top_user_post in top_user_post_list:
        top_user = RankingUser.from_orm(top_user_post.user)
        top_user.high_score = top_user_post.point
        top_user.rank = get_user_rank(db, top_user.id)
        ranking_user.append(top_user)
    return ranking_user
    
def get_user_rank(db: Session, user_id: str) -> int:
    top_post = db.query(models.TopPost).filter(models.TopPost.user_id == user_id).first()
    if top_post == None:
        return None
    upper_post_list = db.query(models.TopPost).filter(models.TopPost.point > top_post.point).all()
    return 1+len(upper_post_list)
