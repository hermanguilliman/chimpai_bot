# chimpai bot 🐵

Этот бот предоставляет возможность использовать OpenAI API выбранным администраторам бота.
Присутствует возможность настроить параметры запроса: модель, длина и температура.

## Команда для запуска в докере

```bash
docker run -d \
    -e BOT_TOKEN=<TOKEN> \
    -e ADMINS=<IDS> \
    -e OPENAI_API_KEY=<KEY> \
    gentlemantleman/chimpai:latest
```
