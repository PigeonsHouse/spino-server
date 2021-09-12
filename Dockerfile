FROM python:3.9.5-alpine

RUN apk add gcc linux-headers make libffi-dev musl-dev g++

RUN apk add --no-cache postgresql-libs && \
	apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN mkdir /app
WORKDIR /app

COPY . /app/

RUN pip install pipenv
RUN pipenv install