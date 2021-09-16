from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, Depends, HTTPException, status
import firebase_admin
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session
from db import models, get_db
from schemas.users import User
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
    print(user)

    return user

def create_user(db: Session, name: str, current_user: str) -> User:
    
    user = _get_user(db, name)
    if user != None:
        raise HTTPException(400, 'Specified username has already taken')

    user_orm = models.User(
        id = current_user,
        name = name
    )

    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    user = User.from_orm(user_orm)
    return user

def _get_user(db: Session, name: str) -> User:
	user_orm = db.query(models.User).filter(models.User.name == name).first()
	if user_orm == None:
		return None
	return User.from_orm(user_orm)