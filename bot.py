import asyncio

from loguru import logger

from tgbot.bot_init import setup_bot
from tgbot.config import load_config, setup_logger


async def main():
    setup_logger()
    config = load_config(".env")
    bot, dp = await setup_bot(config)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Starting ChimpAI")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("ChimpAI stopped!")
