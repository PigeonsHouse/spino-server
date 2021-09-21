from cruds.posts import set_high_score_post
import requests
import sqlalchemy
import pytest
from sqlalchemy.orm import sessionmaker
import sqlalchemy_utils
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import Session
import firebase_admin
from main import app
import os
from db import Base, get_db, models
from schemas.users import User
from schemas.posts import Post


DATABASE = 'postgresql'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = 'spino_test'

DATABASE_URL = "{}://{}:{}@{}/{}".format(DATABASE, USER, PASSWORD, HOST, DB_NAME)
ECHO_LOG = False
engine = sqlalchemy.create_engine(DATABASE_URL, echo=ECHO_LOG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

API_KEY = os.environ.get('API_KEY')

TEST_USER_EMAIL_1 = os.environ.get('TEST_USER_EMAIL_1')
TEST_USER_PASSWORD_1 = os.environ.get('TEST_USER_PASSWORD_1')
TEST_USER_EMAIL_2 = os.environ.get('TEST_USER_EMAIL_2')
TEST_USER_PASSWORD_2 = os.environ.get('TEST_USER_PASSWORD_2')

client = TestClient(app)

print(TEST_USER_EMAIL_1)

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
def user_token_factory_test():
  """
  test用Userのトークンを返す関数を返す
  """
  def user_token_for_test(user_num: int = 0):
    uri = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={API_KEY}"
    if user_num == 0:      
      data = {"email": TEST_USER_EMAIL_1, "password": TEST_USER_PASSWORD_1, "returnSecureToken": True}
    elif user_num == 1:
      data = {"email": TEST_USER_EMAIL_2, "password": TEST_USER_PASSWORD_2, "returnSecureToken": True}
    else:
      data = None

    result = requests.post(url=uri, data=data)

    user = result.json()

    return user['idToken']
  return user_token_for_test

@pytest.fixture
def post_user_for_test(session_for_test, user_token_factory_test):
  user_token_test = user_token_factory_test()
  user_id = firebase_admin.auth.verify_id_token(user_token_test)['user_id']
  user_orm = models.User(
    id = user_id,
    name = "username",
    img = "imgURL"
  )

  session_for_test.add(user_orm)
  session_for_test.commit()
  session_for_test.refresh(user_orm)
  user = User.from_orm(user_orm)

  return user

@pytest.fixture
def post_second_user_for_test(session_for_test, user_token_factory_test):
  user_token_test = user_token_factory_test(user_num=1)
  user_id = firebase_admin.auth.verify_id_token(user_token_test)['user_id']
  user_orm = models.User(
    id = user_id,
    name = "username",
    img = "imgURL"
  )

  session_for_test.add(user_orm)
  session_for_test.commit()
  session_for_test.refresh(user_orm)
  user = User.from_orm(user_orm)

  return user

@pytest.fixture
def post_factory_for_test(session_for_test, user_token_factory_test):
  def create_post_for_test(
    user_num: int = 0,
    point: int = 10000,
    image_url: str = 'https://example.com/'
  ):
    user_token_test = user_token_factory_test(user_num)
    user_id = firebase_admin.auth.verify_id_token(user_token_test)['user_id']
    post_orm = models.Post(
      user_id = user_id,
      point = point,
      image_url = image_url
    )

    session_for_test.add(post_orm)
    session_for_test.commit()
    session_for_test.refresh(post_orm)
    post = Post.from_orm(post_orm)

    set_high_score_post(session_for_test, post.id, user_id, point, image_url)

    return post
  return create_post_for_test
