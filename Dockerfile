FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install pipenv && pipenv install --system

COPY . /code/
