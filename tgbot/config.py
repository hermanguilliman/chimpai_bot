from dataclasses import dataclass
from sys import stdout

from environs import Env
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
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS", False),
        ),
        ai=AI(base_url=env.str("BASE_URL", None)),
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
