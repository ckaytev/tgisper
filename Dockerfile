FROM python:3.10.11-slim

ENV POETRY_VENV=/app/.venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN useradd -m appuser
USER appuser
WORKDIR /app

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY tgisper ./tgisper

ENTRYPOINT ["poetry", "run", "tgisper"]
