from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from openai import AsyncOpenAI
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from tgbot.dialogs.neural.chat import chat_dialog
from tgbot.dialogs.neural.settings import chat_settings_dialog
from tgbot.dialogs.personality.create import new_person_dialog
from tgbot.dialogs.personality.menu import personality_menu_dialog
from tgbot.dialogs.root.menu import main_dialog
from tgbot.dialogs.system_settings.base_url import base_url_dialog
from tgbot.dialogs.system_settings.chat_service import chat_service_dialog
from tgbot.dialogs.system_settings.menu import system_settings_dialog
from tgbot.filters.is_admin import AdminFilter
from tgbot.handlers.admin_start import admin_start_handler
from tgbot.handlers.errors import on_unknown_intent, on_unknown_state
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.openai_api import OpenAIMiddleware
from tgbot.middlewares.trottling import ThrottlingMiddleware
from tgbot.misc.base_urls import add_base_urls
from tgbot.misc.personalities import add_basic_persons


async def create_session_pool(echo: bool) -> AsyncSession:
    url = "sqlite+aiosqlite:///database/settings.db"
    engine = create_async_engine(url, echo=echo, future=True)

    await add_basic_persons(engine)
    await add_base_urls(engine)

    pool = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False,
    )
    return pool


async def setup_bot(config):
    storage = (
        RedisStorage(
            Redis(host="valkey", port=6379, db=5),
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
        if config.tg_bot.use_redis
        else MemoryStorage()
    )
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    session_pool = await create_session_pool(echo=False)
    openai = AsyncOpenAI(api_key="dummy_key")

    dp.include_routers(
        main_dialog,
        chat_dialog,
        personality_menu_dialog,
        system_settings_dialog,
        new_person_dialog,
        chat_settings_dialog,
        base_url_dialog,
        chat_service_dialog,
    )
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )
    setup_dialogs(dp)

    dp.update.middleware(ThrottlingMiddleware(rate_limit=0.5))
    dp.callback_query.middleware(ThrottlingMiddleware(rate_limit=0.5))
    dp.update.middleware(DatabaseMiddleware(session_pool))
    dp.update.middleware(OpenAIMiddleware(openai))
    dp.message.register(
        admin_start_handler,
        CommandStart(deep_link_encoded=True),
        AdminFilter(config.tg_bot.admin_ids),
    )

    return bot, dp
