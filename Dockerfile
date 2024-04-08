FROM python:3.12-alpine

WORKDIR /app

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

EXPOSE 80

CMD [ "poetry", "run", "hypercorn", "api:app", "--keyfile=key.pem", "--certfile=cert.pem", "--bind=0.0.0.0:80" ]
