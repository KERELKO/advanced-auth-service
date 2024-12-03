FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt update && apt upgrade

WORKDIR app/

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev \
    nmap

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/
