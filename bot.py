import asyncio

# additional tools
import openai

# base aiogram with FSM
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

# dialogs
from aiogram_dialog import DialogRegistry
from loguru import logger

# database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.dialogs.main import main_dialog
from tgbot.dialogs.neural import neural_chat
from tgbot.dialogs.personality import person
from tgbot.dialogs.settings import settings_dialog

# filters
from tgbot.filters.admin_filter import AdminFilter, RoleFilter

# handlers
from tgbot.handlers.admin_start import register_admin
from tgbot.handlers.user_start import register_user

# middlewares
from tgbot.middlewares.db_and_repo import DbMiddleware
from tgbot.middlewares.openai_api import OpenAIMiddleware

# models
from tgbot.models.base import Base


async def create_sessionmaker(echo) -> AsyncSession:
    # url = f"postgresql+asyncpg://{user}:{password}@{host}/{database}"
    url = "sqlite+aiosqlite:///database/settings.db"

    engine = create_async_engine(url, echo=echo, future=True)

    # create metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # session
    session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return session


def register_all_middlewares(dp: Dispatcher, config, session: AsyncSession, openai):
    dp.setup_middleware(DbMiddleware(session=session))
    dp.setup_middleware(OpenAIMiddleware(openai=openai))


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user(dp)


async def main():
    logger.info("Starting ChimpAI")
    config = load_config(".env")

    storage = (
        RedisStorage2("redis", 6379, db=5, pool_size=10, prefix="chimpai_fsm")
        if config.tg_bot.use_redis
        else MemoryStorage()
    )
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    bot["config"] = config

    session = await create_sessionmaker(echo=False)

    register_all_middlewares(dp, config, session, openai)
    register_all_filters(dp)
    register_all_handlers(dp)

    registry = DialogRegistry(dp)
    registry.register(main_dialog)
    registry.register(settings_dialog)
    registry.register(neural_chat)
    registry.register(person)
    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("ChimpAI stopped!")
