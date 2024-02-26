FROM python:3.9-alpine

RUN apk add --no-cache tzdata

ENV TZ=America/Bogota

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk add chromium

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT python -u -m src.backend.main



