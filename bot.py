import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.methods import DeleteWebhook
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from loguru import logger
from openai import AsyncOpenAI
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine)

from tgbot.config import load_config, setup_logger
from tgbot.dialogs.chat_settings import chat_settings_dialog
from tgbot.dialogs.main import main_dialog
from tgbot.dialogs.chatgpt import chat_gpt_dialog
from tgbot.dialogs.dalle import dalle_dialog
from tgbot.dialogs.tts import text_to_speech_dialog
from tgbot.dialogs.stt import speech_to_text_dialog
from tgbot.dialogs.person_menu import personality_menu_dialog
from tgbot.dialogs.create_person import new_person_dialog
from tgbot.dialogs.settings_menu import root_settings_dialog
from tgbot.dialogs.tts_settings import tts_settings_dialog
from tgbot.filters.is_admin import AdminFilter
from tgbot.handlers.admin_start import admin_start
from tgbot.handlers.unknown_errors import on_unknown_intent, on_unknown_state
from tgbot.handlers.user_start import user_start
from tgbot.middlewares.openai_api import OpenAIMiddleware
from tgbot.middlewares.repo import RepoMiddleware
from tgbot.models.base import Base
from tgbot.models.personality import BasicPersonality
from tgbot.misc.personality import personality_base


async def create_sessionmaker(echo) -> AsyncSession:
    url = "sqlite+aiosqlite:///database/settings.db"
    engine = create_async_engine(url, echo=echo, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        # Пытаемся добавить стандартные значения
        async with engine.begin() as conn:
            for person in personality_base:
                await conn.execute(BasicPersonality.__table__.insert(), person)
        logger.success("Стандартные настройки личностей добавлены")
    except Exception:
        logger.info("Стандартные настройки личностей уже добавлены")

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
    if config.ai.base_url:
        openai.base_url = config.ai.base_url
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )

    dp.include_routers(
        main_dialog,
        chat_gpt_dialog,
        dalle_dialog,
        speech_to_text_dialog,
        text_to_speech_dialog,
        personality_menu_dialog,
        root_settings_dialog,
        new_person_dialog,
        chat_settings_dialog,
        tts_settings_dialog
    )

    setup_dialogs(dp)

    dp.update.middleware(RepoMiddleware(sessionmaker))
    dp.update.middleware(OpenAIMiddleware(openai))
    dp.message.register(
        admin_start, CommandStart(), AdminFilter(config.tg_bot.admin_ids)
    )
    dp.message.register(user_start, CommandStart())
    await bot(DeleteWebhook(drop_pending_updates=True))
    logger.info("Запуск ChimpAI")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("ChimpAI остановлен!")
