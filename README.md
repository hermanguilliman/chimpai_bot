# chimpai bot 🐵

[![Интерфейс бота](https://i.ibb.co/6066yqf/main.jpg 'gui')](https://i.ibb.co/6066yqf/main.jpg)

**ChimpAI - это Telegram бот с интерфейсом OpenAI.**

1. Использует ваш личный OpenAI API ключ
2. Имеет несколько базовых преднастроек для текстовых запросов
3. Может транскрибировать голосовые сообщения в текст
4. Может создавать голосовые сообщения из текста (TTS)
5. Использует Dall-E 3 для создания изображений

## Как начать пользоваться ботом?

Клонируйте репозиторий, заполните .env, соберите и запустите контейнер

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/hermanguilliman/chimpai_bot.git
```

### 2. Заполните переменные в .env файле

```bash
cp .env.example .env
nano .env
```

### 3. Соберите

```bash
docker-compose build
```

### 4. Запустите

```bash
docker-compose up -d
```
