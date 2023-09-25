FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install --no-root --no-dev
CMD [ "python", "./bot.py" ]