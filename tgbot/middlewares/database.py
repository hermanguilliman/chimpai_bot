from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot.services.repository.api_urls import BaseUrlService
from tgbot.services.repository.history import ConversationHistoryService
from tgbot.services.repository.personalities import (
    BasicPersonalityService,
    CustomPersonalityService,
)
from tgbot.services.repository.settings import SettingsService
from tgbot.services.repository.users import UserService


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker[AsyncSession]):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["user_service"] = UserService(session)
            data["settings_service"] = SettingsService(session)
            data["custom_personality_service"] = CustomPersonalityService(
                session
            )
            data["conversation_service"] = ConversationHistoryService(session)
            data["base_url_service"] = BaseUrlService(session)
            data["basic_personality_service"] = BasicPersonalityService(
                session
            )
            return await handler(event, data)
