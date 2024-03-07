FROM python:3.12-slim

RUN apt-get update

RUN apt-get install python3-dev build-essential -y

RUN pip install --upgrade pip
RUN pip install virtualenv && python -m virtualenv /opt/venv

ADD ./requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY . /srv/app

WORKDIR /srv/app
