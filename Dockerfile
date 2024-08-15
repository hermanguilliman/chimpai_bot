FROM python:3.12-slim

# Create a non-root user
RUN useradd -m chimpai

WORKDIR /app

# Copy only the files needed for installation
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Copy the rest of your application
COPY bot.py /app/
COPY tgbot /app/tgbot

# Switch to non-root user
USER chimpai

ENTRYPOINT ["python", "bot.py"]