FROM python:3.11-slim-bullseye

WORKDIR /usr/src

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./backend/requirements.txt /usr/src/app/requirements.txt

COPY ./backend/main.py /usr/src/main.py

RUN pip3 install --upgrade pip setuptools wheel \
    && pip3 install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip
