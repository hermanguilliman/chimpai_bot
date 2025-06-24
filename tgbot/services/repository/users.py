from typing import List

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from tgbot.models.models import (
    ChatSettings,
    Settings,
    SummarySettings,
    Users,
)
from tgbot.services.repository.base import BaseService


class UserService(BaseService):
    async def add_user(self, user_id: int) -> None:
        user = Users(id=user_id)
        settings = Settings(user=user)
        chat_settings = ChatSettings(settings=settings)
        summary_settings = SummarySettings(settings=settings)
        self.session.add_all([user, settings, chat_settings, summary_settings])
        await self.session.commit()
        logger.info(f"Добавлен пользователь {user_id}")

    async def get_user(self, user_id: int) -> Users | None:
        stmt = (
            select(Users)
            .where(Users.id == user_id)
            .options(
                selectinload(Users.settings).selectinload(
                    Settings.chat_settings
                ),
                selectinload(Users.settings).selectinload(
                    Settings.summary_settings
                ),
                selectinload(Users.conversation_history),
                selectinload(Users.custom_personality),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(Users).where(Users.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} удален")

    async def list_users(self) -> List[Users]:
        stmt = select(Users)
        result = await self.session.execute(stmt)
        return result.scalars().all()
