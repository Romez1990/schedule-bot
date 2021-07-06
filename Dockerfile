# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /bot
COPY dev-requirements.txt dev-requirements.txt

RUN pip install -r dev-requirements.txt

COPY . .

CMD ["python", "scripts/run.py", "start"]
