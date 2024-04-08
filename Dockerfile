FROM python:3.12-slim

WORKDIR /app

RUN apt update && \
    apt install -y libopencv-dev libgl1-mesa-glx && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

EXPOSE 80

CMD [ "poetry", "run", "gunicorn", "api:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:80" ]
