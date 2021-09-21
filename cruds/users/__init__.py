from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, Depends, HTTPException, status
import firebase_admin
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session
from db import models, get_db
from schemas.users import BaseUser, User, PutUser
import sys

cert = credentials.Certificate('cert.json')
firebase_admin.initialize_app(cert)

def get_current_user_id(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        decoded_token = firebase_admin.auth.verify_id_token(cred.credentials)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user = decoded_token['user_id']

    return user

def create_user(db: Session, name: str, img: str, id: str) -> User:
    
    user = _get_user(db, id)
    if user != None:
        raise HTTPException(400, 'Specified username has already taken')

    user_orm = models.User(
        id = id,
        name = name,
        img = img
    )

    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    user = User.from_orm(user_orm)
    return user

def _get_user(db: Session, id: str) -> User:
    user_orm = db.query(models.User).filter(models.User.id == id).first()
    if user_orm == None:
        return None
    return User.from_orm(user_orm)

def change_info(db: Session, payload: PutUser, id: str) -> User:
    user_orm = db.query(models.User).filter(models.User.id == id).first()
    if user_orm == None:
        raise HTTPException(
            status_code=400,
            detail="changing user is not exist"
        )
    user_orm.name = user_orm.name if payload.name is None else payload.name
    user_orm.img = user_orm.img if payload.img is None else payload.img

    db.commit()
    db.refresh(user_orm)
    user = User.from_orm(user_orm)
    return user