import asyncio
import sys
from loguru import logger
from tgbot.config import load_config

# database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# models
from tgbot.models.base import Base
from tgbot.models.user import Users
from tgbot.models.aisettings import AISettings

# base aiogram with FSM
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

# filters
from tgbot.filters.admin import AdminFilter

# handlers
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user

# middlewares
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.openai import OpenAIMiddleware

# dialogs
from aiogram_dialog import DialogRegistry
from tgbot.dialogs.main import main_dialog
from tgbot.dialogs.settings import settings_dialog
# additional tools
import openai



async def create_sessionmaker(echo) -> AsyncSession:
    # url = f"postgresql+asyncpg://{user}:{password}@{host}/{database}"
    url = "sqlite+aiosqlite:///database/settings.db"

    engine = create_async_engine(url, echo=echo, future=True)

    # create metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # session
    session = sessionmaker(engine,
                           expire_on_commit=False,
                           class_=AsyncSession,
                           )
    return session


def register_all_middlewares(dp: Dispatcher, config, session: AsyncSession, openai):
    dp.setup_middleware(DbMiddleware(session=session))
    dp.setup_middleware(OpenAIMiddleware(openai=openai))


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user(dp)


async def main():
    logger.info("Starting ChimpAI")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    session = await create_sessionmaker(echo=False)

    register_all_middlewares(dp, config, session, openai)
    register_all_filters(dp)
    register_all_handlers(dp)

    registry = DialogRegistry(dp)
    registry.register(main_dialog)
    registry.register(settings_dialog)
    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("ChimpAI stopped!")
