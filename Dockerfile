FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.1.14

RUN useradd -m app
USER app

WORKDIR /home/app/google_api

RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION
ENV PATH=/home/app/.local/bin:$PATH
RUN poetry config virtualenvs.in-project false

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-interaction

COPY . .
