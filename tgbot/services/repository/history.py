from typing import List

from loguru import logger
from sqlalchemy import delete, func, select

from tgbot.models.models import (
    ConversationHistory,
)
from tgbot.services.repository.base import BaseService


class ConversationHistoryService(BaseService):
    async def add_message_to_history(
        self, user_id: int, role: str, content: str
    ) -> None:
        message = ConversationHistory(
            user_id=user_id, role=role, content=content
        )
        self.session.add(message)
        await self.session.commit()
        logger.info(f"Сообщение добавлено в историю для user_id={user_id}")

    async def get_conversation_history(
        self, user_id: int, limit: int = 10
    ) -> List[ConversationHistory]:
        stmt = (
            select(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
            .order_by(ConversationHistory.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def clear_conversation_history(self, user_id: int) -> None:
        stmt = delete(ConversationHistory).where(
            ConversationHistory.user_id == user_id
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"История беседы очищена для user_id={user_id}")

    async def get_history_count(self, user_id: int) -> int:
        """Возвращает количество сообщений в истории пользователя"""
        history_count = await self.session.scalar(
            select(func.count())
            .select_from(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
        )
        return history_count or 0

    async def get_full_conversation_history(
        self, user_id: int
    ) -> List[ConversationHistory]:
        """Получает полную историю беседы для пользователя"""
        stmt = (
            select(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
            .order_by(ConversationHistory.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
