# chimpai bot 🐵

Этот бот предоставляет администраторам бота доступ к OpenAI API с помощью уникальных токенов. Он позволяет настраивать параметры запроса, такие как модель, длину и температуру.

## Команда для запуска в докере

```bash
docker run -d \
    -e BOT_TOKEN=<TOKEN> \
    -e ADMINS=<IDS> \
    -e USE_REDIS=False \
    gentlemantleman/chimpai:latest
```

Пример docker-compose.yml

```yml
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
      - chimpai-redis-data:/data

volumes:
  chimpai-redis-data:

networks:
  chimpai-network:
    driver: bridge
```

Это файл Docker Compose. Он используется для определения и запуска многоконтейнерных приложений Docker. Этот конкретный файл настраивает два контейнера: один для приложения ChimpAI и один для Redis.

Контейнер ChimpAI настраивается с помощью переменных среды для токена бота, администраторов и того, следует ли использовать Redis. У него также есть том, смонтированный в каталоге «базы данных». Наконец, он настроен на запуск при запуске контейнера Redis и подключен к сети «chimpai-network».

Контейнер Redis настроен с помощью переменных среды, чтобы отключить определенные команды и разрешить пустой пароль. У него также есть том, смонтированный в каталоге «/data», и он подключен к сети «chimpai-network».

Наконец, файл устанавливает том с именем «chimpai-redis-data» и сеть с именем «chimpai-network» с установленным драйвером «bridge».
