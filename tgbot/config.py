import os
from dataclasses import dataclass
from sys import stdout

from dotenv import load_dotenv
from loguru import logger


@dataclass
class AI:
    base_url: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Config:
    ai: AI
    tg_bot: TgBot


def load_config(path: str = None):
    # Load environment variables from .env file if path is provided
    if path:
        load_dotenv(path)
    else:
        load_dotenv()

    return Config(
        tg_bot=TgBot(
            token=os.getenv("BOT_TOKEN"),
            admin_ids=list(map(int, os.getenv("ADMINS", "").split(",")))
            if os.getenv("ADMINS")
            else [],
            use_redis=os.getenv("USE_REDIS", "False").lower() == "true",
        ),
        ai=AI(base_url=os.getenv("BASE_URL")),
    )


def setup_logger():
    logger.remove()
    logger.add("logs/chimpai.log", level="DEBUG", rotation="10 MB")
    logger.add(
        stdout,
        colorize=True,
        format="<green>{time}</green> <level>{message}</level>",
        level="DEBUG",
    )
