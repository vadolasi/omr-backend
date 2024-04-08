FROM python:3.12-alpine

WORKDIR /app

RUN pip install poetry

ARG PYTHON=python3.12
RUN curl https://bootstrap.pypa.io/get-pip.py | \
    $PYTHON - pip==21.3 && \
    # pip adopts the behaviour which is unsupported by debian
    # https://github.com/pypa/get-pip/issues/124
    mkdir /usr/lib/$PYTHON/dist-packages && \
    echo /usr/lib/$PYTHON/site-packages > /usr/lib/$PYTHON/dist-packages/site-packages.pth && \
    rm -rf /tmp/*

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

EXPOSE 80

CMD [ "poetry", "run", "gunicorn", "api:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:80" ]
