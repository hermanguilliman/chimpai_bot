# chimpai bot 🐵

[![Интерфейс бота](https://i.ibb.co/Z8HvGRT/4.jpg 'gui')](https://ibb.co/Z8HvGRT)
[![Интерфейс бота](https://i.ibb.co/fFHrZLF/1.jpg 'gui')](https://ibb.co/fFHrZLF)
[![Интерфейс бота](https://i.ibb.co/HH3JpQg/2.jpg 'gui')](https://ibb.co/HH3JpQg)
[![Интерфейс бота](https://i.ibb.co/K6vjVZ7/3.jpg 'gui')](https://ibb.co/K6vjVZ7)
[![Интерфейс бота](https://i.ibb.co/Jm4G3WV/5.jpg 'gui')](https://ibb.co/Jm4G3WV)

Это ChimpAI - Telegram bot с интерфейсом OpenAI API. Он имеет возможность настройки параметров запроса, а так же поддерживает преднастройку личности по готовому или ручному описанию личности

## Команда для запуска докер контейнера с минимальными настройками

```bash
docker run -d --name chimpai -e BOT_TOKEN=<TOKEN> -e ADMINS=<IDS> gentlemantleman/chimpai:latest
```

***Telegram id администраторов перечисляются через запятую
ADMINS=1111,2222,3333***

### Полный список переменных окружения

* BOT_TOKEN: string
* ADMINS: int
* USE_REDIS: bool

## Пример docker-compose c использованием Redis для хранения контекста телеграм диалога

### Создайте директорию и поместите в неё файл docker-compose.yml

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

В этой конфигурации запускается контейнер с ботом и базой Redis, а так же создаётся директория **database** в которой хранится база данных **settings.db** с настройками

### Затем запустите в фоне помощью команды

```bash
docker-compose up -d
```

### Чтобы остановить

```bash
docker-compose down
```

### Чтобы перезапустить

```bash
docker-compose restart
```
