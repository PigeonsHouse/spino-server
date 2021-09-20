FROM python:3.9.5-slim

RUN apt-get update

RUN apt-get install -y gcc make libffi-dev musl-dev g++ libpq-dev

RUN apt-get install -y gcc musl-dev 

RUN mkdir /app
WORKDIR /app

COPY . /app/

RUN pip install fastapi sqlalchemy uvicorn pyjwt \
	psycopg2 python-multipart requests flake8 firebase_admin \
	pydantic pytest sqlalchemy_utils python-dotenv \
	google-cloud-vision gensim