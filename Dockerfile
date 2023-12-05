FROM python:3.11-slim
WORKDIR /app
COPY poetry.lock pyproject.toml bot.py /app/
COPY tgbot /app/tgbot

RUN pip install --upgrade pip --user
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["python", "bot.py"]