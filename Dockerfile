FROM python:3.11-slim
WORKDIR /app
COPY poetry.lock pyproject.toml bot.py /app/
COPY tgbot /app/tgbot

ENV PATH="/root/.local/bin:${PATH}"
RUN pip install --upgrade pip --user
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

RUN python -m venv /venv
ENV PATH="/venv/bin:${PATH}"

ENTRYPOINT ["python", "bot.py"]