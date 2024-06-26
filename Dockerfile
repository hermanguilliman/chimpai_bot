FROM python:3.12-slim
WORKDIR /app
COPY poetry.lock pyproject.toml bot.py /app/
COPY tgbot /app/tgbot

RUN pip install --upgrade pip
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

ENTRYPOINT ["python", "bot.py"]