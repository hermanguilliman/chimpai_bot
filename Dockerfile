FROM python:3.11-slim
WORKDIR /app
COPY poetry.lock pyproject.toml bot.py /app/
COPY tgbot /app/tgbot

RUN apt-get update && apt-get install -y python3-venv

RUN python3 -m venv /venv
ENV PATH="/venv/bin:${PATH}"

RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["python", "bot.py"]