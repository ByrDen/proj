FROM python:3.12-slim

ARG APP_PATH=/opt

WORKDIR $APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1


COPY ./shop $APP_PATH/shop
COPY ./src $APP_PATH/src

RUN pip install --no-cache-dir --upgrade -r $APP_PATH/shop/requirements.txt