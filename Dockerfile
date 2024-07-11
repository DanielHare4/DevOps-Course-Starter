FROM python:3.12 AS base
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/root/.local/bin/
WORKDIR /app
COPY pyproject.toml poetry.toml /app/
RUN poetry install
COPY todo_app /app/todo_app

# Production
FROM base AS production
ENV FLASK_DEBUG=false
ENTRYPOINT poetry run flask run --host=0.0.0.0

# Development
FROM base AS development
ENV FLASK_DEBUG=true
ENTRYPOINT poetry run flask run --host=0.0.0.0

# CI
FROM base AS test
ENTRYPOINT poetry run pytest
