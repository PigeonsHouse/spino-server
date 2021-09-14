from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, Depends, HTTPException, status
import firebase_admin
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session
from db import models, get_db
import sys

cert = credentials.Certificate('cert.json')
firebase_admin.initialize_app(cert)

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        decoded_token = firebase_admin.auth.verify_id_token(cred.credentials)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user = decoded_token

    return user

def create_user(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_info = models.User(
        username = current_user,
        email = current_user,
    )
