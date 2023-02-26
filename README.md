# chimpai bot 🐵

Этот бот предоставляет возможность использовать OpenAI API выбранным администраторам бота.
Присутствует возможность использовать уникальные токены для каждого пользователя, настроить параметры запроса: модель, длина и температура.

## Команда для запуска в докере

```bash
docker run -d \
    -e BOT_TOKEN=<TOKEN> \
    -e ADMINS=<IDS> \
    -e USE_REDIS=False \
    gentlemantleman/chimpai:latest
```

Пример docker-compose.yml

```bash
version: '3'
services:
  chimpai:
    container_name: chimpai
    image: gentlemantleman/chimpai:latest
    restart: on-failure
    environment:
      - BOT_TOKEN=TOKEN
      - ADMINS=12345,54321
      - USE_REDIS=True
    volumes:
      - ./database:/app/database
    depends-on: 
      - redis

  redis:
    container_name: chimpai_redis
    image: redis:7.0.8-alpine
    restart: on-failure
    ports:
      - "6379:6379"
    volumes:
      - chimai-redis-data:/data

volumes:
  chimai-redis-data:
