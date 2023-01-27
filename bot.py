import asyncio
import logging
from tgbot.config import load_config

import openai

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from tgbot.models.base import Base
from tgbot.models.user import Users
from tgbot.models.aisettings import AISettings

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.filters.admin import AdminFilter
#handlers
from tgbot.handlers.admin import register_admin
from tgbot.handlers.settings import register_admin_settings
from tgbot.handlers.answer_ai import register_answer_ai
from tgbot.handlers.user import register_user

from tgbot.callbacks.settings import register_settings_callbacks

from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.openai import OpenAIMiddleware
logger = logging.getLogger(__name__)


async def create_sessionmaker(echo) -> AsyncSession:
    # url = f"postgresql+asyncpg://{user}:{password}@{host}/{database}"
    url = "sqlite+aiosqlite:///database.db"

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
    #dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(DbMiddleware(session=session))
    dp.setup_middleware(OpenAIMiddleware(openai=openai))


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user(dp)
    register_admin_settings(dp)
    register_answer_ai(dp)


def register_all_callbacks(dp: Dispatcher):
    register_settings_callbacks(dp)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    openai.api_key = config.openai.token
    bot['config'] = config

    session = await create_sessionmaker(echo=False)
    register_all_middlewares(dp, config, session, openai)
    register_all_filters(dp)
    register_all_handlers(dp)
    register_all_callbacks(dp)

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
        logger.error("Bot stopped!")
