from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine

from tgbot.models.models import BaseUrl

base_urls = [
    {"name": "OpenAI", "url": "https://api.openai.com/v1"},
    {"name": "OpenRouter", "url": "https://openrouter.ai/api/v1"},
    {"name": "ProxyAPI", "url": "https://api.proxyapi.ru/openai/v1"},
]


async def add_base_urls(engine: AsyncEngine) -> None:
    try:
        # Пытаемся добавить стандартные значения
        async with engine.begin() as conn:
            for url in base_urls:
                await conn.execute(BaseUrl.__table__.insert(), url)
        logger.success("Базовые адреса API добавлены")
    except Exception:
        logger.info("Базовые адреса API уже добавлены")
