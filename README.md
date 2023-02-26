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
version: '3.8'
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
    networks:
      - chimpai-network
    depends_on:
      - redis

  redis:
    container_name: chimpai_redis
    image: redis:7.0.8-alpine
    restart: on-failure
    networks:
      - chimpai-network
    environment:
      - REDIS_DISABLE_COMMANDS=FLUSHDB,FLUSHALL,CONFIG
      - ALLOW_EMPTY_PASSWORD=yes
    volumes:
      - chimai-redis-data:/data

volumes:
  chimai-redis-data:

networks:
  chimpai-network:
    driver: bridge
