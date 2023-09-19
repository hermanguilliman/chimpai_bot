FROM python:3.11-alpine
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev
COPY . .
CMD [ "python", "./bot.py" ]