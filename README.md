# chimpai bot 🐵

[![Интерфейс бота](https://i.ibb.co/N1JDST3/1.jpg 'gui')](https://ibb.co/N1JDST3)
[![Интерфейс бота](https://i.ibb.co/WP7T39Y/2.jpg 'gui')](https://ibb.co/WP7T39Y)
[![Интерфейс бота](https://i.ibb.co/Bg6Wf7g/3.jpg 'gui')](https://ibb.co/Bg6Wf7g)

Этот бот предоставляет администраторам бота доступ к OpenAI API с помощью уникальных токенов. Он позволяет настраивать параметры запроса, такие как модель, длину и температуру.
Общение с нейросетью происходит через отдельный диалог и позволяет отвечать на предыдущие сообщения

## Команда для запуска докер контейнера с минимальными настройками

```bash
docker run -d --name chimpai -e BOT_TOKEN=<TOKEN> -e ADMINS=<IDS> gentlemantleman/chimpai:latest
```

***Telegram id администраторов перечисляются через запятую
ADMINS=1111,2222,3333***

### Полный список переменных окружения

* BOT_TOKEN
* ADMINS
* USE_REDIS

## Пример docker-compose c использованием Redis для хранения контекста телеграм диалога

### Создайте директорию и поместите в неё файл docker-compose.yml используя шаблон

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

В этой конфигурации у нас запускается контейнер с ботом и базой Redis, а так же создаётся директория **database** в которой хранится база данных **settings.db** с настройками администраторов

### Затем запустите его с помощью команды

```bash
docker-compose up -d
```

### Аналогично можно остановить бота и Redis с помощью команды

```bash
docker-compose down
```