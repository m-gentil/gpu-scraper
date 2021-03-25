# syntax = docker/dockerfile:1.0-experimental
FROM python:3.9-alpine

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

# Environment variables used at build time
ARG POETRY_VERSION=1.1.4
ARG POETRY_VIRTUALENVS_CREATE=false

# Add poetry to path
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /gpu_scraper

RUN apk update && apk --no-cache add curl && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY pyproject.toml poetry.lock ./

COPY gpu_scraper/__init__.py ./gpu_scraper/__init__.py

RUN poetry install --no-dev

COPY gpu_scraper ./gpu_scraper/

ENTRYPOINT ["scrape"]
