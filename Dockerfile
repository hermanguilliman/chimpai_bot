FROM python:3.11-alpine
WORKDIR /app
RUN apk add --no-cache curl && curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev
COPY . .
CMD [ "python", "./bot.py" ]