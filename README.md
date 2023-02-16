# chimpai bot 🐵

Этот бот предоставляет возможность использовать OpenAI API выбранным администраторам бота.
Присутствует возможность использовать уникальные токены для каждого пользователя, настроить параметры запроса: модель, длина и температура.

## Команда для запуска в докере

```bash
docker run -d \
    -e BOT_TOKEN=<TOKEN> \
    -e ADMINS=<IDS> \
    gentlemantleman/chimpai:latest
```

Так же пример docker-compose.yml

```bash
version: '3'
services:
  chimpai:
    container_name: chimpai
    image: gentlemantleman/chimpai:latest
    environment:
      - BOT_TOKEN=TOKEN
      - ADMINS=12345,54321
    volumes:
      - ./database:/app/database
