import requests
from pprint import pprint

import sqlalchemy
import pytest
from sqlalchemy.orm import sessionmaker
import sqlalchemy_utils
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import Session


from main import app
import os
from db import Base, get_db, models
from schemas.users import User


DATABASE = 'postgresql'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = 'spino_test'

DATABASE_URL = "{}://{}:{}@{}/{}".format(DATABASE, USER, PASSWORD, HOST, DB_NAME)
ECHO_LOG = False
engine = sqlalchemy.create_engine(DATABASE_URL, echo=ECHO_LOG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



CONFIG = {
    "apiKey": os.environ.get('API_KEY'),
    "authDomain": os.environ.get('AUTHDO_MAIN'),
    "projectId": os.environ.get('PROJECT_ID'),
    "storageBucket": os.environ.get('STORAGE_BUCKET'),
    "messagingSenderId": os.environ.get('MESSAGING_SENDER_ID'),
    "appId": os.environ.get('APP_ID'),
    "measurementId": os.environ.get('MEASUREMENT_ID')
}
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

client = TestClient(app)

@pytest.fixture(scope="function")
def use_test_db_fixture():
  """
  Override get_db with test DB
  get_db関数をテストDBで上書きする
  """
  if not sqlalchemy_utils.database_exists(DATABASE_URL):
    print('[INFO] CREATE DATABASE')
    sqlalchemy_utils.create_database(DATABASE_URL)

  # Reset test tables
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)

  def override_get_db():
    try:
      db = SessionLocal()
      yield db
    finally:
      db.close()

  app.dependency_overrides[get_db] = override_get_db
  yield SessionLocal()

@pytest.fixture
def session_for_test():
  """
  DB Session for test
  """
  session = SessionLocal()
  yield session
  
  session.close()

@pytest.fixture
def user_token_test():
    api_key = CONFIG["apiKey"]
    uri = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
    data = {"email": EMAIL, "password": PASSWORD, "returnSecureToken": True}

    result = requests.post(url=uri, data=data)

    user = result.json()

    return user['idToken']

@pytest.fixture
def post_user_for_test(session_for_test, user_token_test):
  user_orm = models.User(
    id = user_token_test,
    name = "username"
  )

  session_for_test.add(user_orm)
  session_for_test.commit()
  session_for_test.refresh(user_orm)
  user = User.from_orm(user_orm)

  return user