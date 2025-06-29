FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN uv pip install --system --no-cache-dir -r <(uv export --no-hashes)

COPY . /app/

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]