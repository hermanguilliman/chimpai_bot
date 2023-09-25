FROM python:3.11-alpine
WORKDIR /app
COPY poetry.lock pyproject.toml bot.py /app/
COPY tgbot /app/tgbot

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["python", "bot.py"]