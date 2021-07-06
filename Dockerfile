# syntax=docker/dockerfile:1

FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot

RUN apt-get update \
    && apt-get install -y postgresql-server-dev-11 gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY dev-requirements.txt /bot
RUN pip install -r dev-requirements.txt

COPY . /bot

CMD ["python", "scripts/run.py", "start"]
