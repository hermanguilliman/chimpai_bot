import asyncio

from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.methods import DeleteWebhook
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from loguru import logger
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)

from tgbot.config import load_config, setup_logger
from tgbot.dialogs.main import main_dialog
from tgbot.dialogs.neural import neural_chat
from tgbot.dialogs.personality import person
from tgbot.dialogs.settings import settings_dialog
from tgbot.filters.is_admin import AdminFilter
from tgbot.handlers.admin_start import admin_start
from tgbot.handlers.unknown_errors import on_unknown_intent, on_unknown_state
from tgbot.handlers.user_start import user_start
from tgbot.middlewares.openai_api import OpenAIMiddleware
from tgbot.middlewares.repo import RepoMiddleware
from tgbot.models.base import Base


async def create_sessionmaker(echo) -> AsyncSession:
    url = "sqlite+aiosqlite:///database/settings.db"
    engine = create_async_engine(url, echo=echo, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    sessionmaker = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False,
    )
    return sessionmaker


async def main():
    setup_logger()
    config = load_config(".env")

    storage = (
        RedisStorage(
            Redis(host="redis", port=6379, db=5),
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
        if config.tg_bot.use_redis
        else MemoryStorage()
    )
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    sessionmaker = await create_sessionmaker(echo=False)
    openai = AsyncOpenAI(api_key="sk-")
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )

    dp.include_router(main_dialog)
    dp.include_router(settings_dialog)
    dp.include_router(neural_chat)
    dp.include_router(person)

    setup_dialogs(dp)

    dp.update.middleware(RepoMiddleware(sessionmaker))
    dp.update.middleware(OpenAIMiddleware(openai))
    dp.message.register(
        admin_start, CommandStart(), AdminFilter(config.tg_bot.admin_ids)
    )
    dp.message.register(user_start, CommandStart())
    await bot(DeleteWebhook(drop_pending_updates=True))
    logger.info(config.tg_bot.admin_ids)
    logger.info("Запуск ChimpAI")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("ChimpAI остановлен!")
