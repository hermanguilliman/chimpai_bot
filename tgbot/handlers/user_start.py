from aiogram.types import Message
from loguru import logger

from tgbot.services.repository import Repo


async def user_start(m: Message, repo: Repo):
    logger.debug(
        f"Пользователь {m.from_user.full_name} ({m.from_user.id}) постучался в бота"
    )
    await m.answer("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
