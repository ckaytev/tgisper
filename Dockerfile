FROM python:3.10.11-slim

ENV POETRY_VENV=/app/.venv

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install poetry

ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY tgisper ./tgisper

ENTRYPOINT ["poetry", "run", "tgisper"]
