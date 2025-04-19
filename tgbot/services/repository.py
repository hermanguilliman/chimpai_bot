from typing import List

from loguru import logger
from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from tgbot.models.history import ConversationHistory
from tgbot.models.personality import BasicPersonality, CustomPersonality
from tgbot.models.settings import Settings
from tgbot.models.user import Users


class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_user(
        self,
        user_id: int,
    ) -> None:
        """создаём пользователя с базовыми настройками"""
        user = Users(id=user_id)
        settings = Settings(user=user)
        self.session.add(user)
        self.session.add(settings)
        await self.session.commit()
        logger.info("Добавлен пользователь")

    async def get_user(self, user_id: int) -> Users | None:
        """получить все данные о пользователе по id"""
        return await self.session.get(Users, user_id)

    async def delete_user(self, user_id):
        """удаляем пользователя по id"""
        stmt = delete(Users).where(Users.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} удален")

    async def list_users(self) -> List:
        """возвращаем список всех пользователей"""
        rows = select(Users)
        result = await self.session.execute(rows)
        curr = result.scalars()
        return list(curr)

    async def get_settings(self, user_id: int) -> Settings | None:
        # Возвращает настройки пользователя по user_id
        stmt = select(Settings).where(Settings.user_id == user_id)
        settings = await self.session.scalar(stmt)
        return settings

    async def update_max_token(self, user_id: int, max_tokens: int) -> None:
        # Обновляет токен
        stmt = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(max_tokens=max_tokens)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"""
            Пользователь {user_id} установил ответ {max_tokens} токенов"""
        )

    async def update_settings(self, user_id: int, model: str) -> None:
        # Обновляет настройки
        stmt = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(model=model)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_tts_voice(self, user_id: int, tts_voice: str) -> None:
        # Обновляет настройки
        stmt = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(tts_voice=tts_voice)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_tts_speed(self, user_id: int, tts_speed: str) -> None:
        # Обновляет настройки
        stmt = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(tts_speed=tts_speed)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_temperature(self, user_id: int, temperature: str) -> None:
        # Обновляет температуру
        stmt = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(temperature=temperature)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_api_key(self, user_id: int, api_key: str) -> None:
        # обновляет api ключ
        stmt = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(api_key=api_key)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} обновил ключ API")

    async def update_personality(
        self,
        # Обновление значения личности бота
        user_id: int,
        name: str,
        text: str,
    ) -> None:
        stmt = (
            update(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
            .values(text=text)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_custom_personality_list(
        self, user_id: int
    ) -> list[CustomPersonality] | None:
        # Возвращает все кастомные личности по user_id
        stmt = select(CustomPersonality).where(
            CustomPersonality.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_custom_personality(
        self,
        user_id: int,
        personality_name: str,
    ) -> CustomPersonality | None:
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == personality_name)
        )
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        return result.text

    async def get_basic_personality_list(
        self,
    ) -> list[BasicPersonality] | None:
        """Возвращает список стандартных личностей"""
        rows = select(BasicPersonality)
        result = await self.session.execute(rows)
        return result.scalars().all()

    async def delete_custom_personality(self, user_id: int, name: str) -> None:
        stmt = (
            delete(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} удалил личность")

    async def add_custom_personality(
        self, user_id: int, name: str, text: str
    ) -> None:
        personality = CustomPersonality(name=name, text=text, user_id=user_id)
        self.session.add(personality)
        await self.session.commit()

    async def select_basic_personality(self, user_id: int, name: str) -> None:
        """установка стандартной личности бота"""
        stmt = select(BasicPersonality).where(BasicPersonality.name == name)
        bp = await self.session.scalar(stmt)
        settings = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(personality_name=bp.name, personality_text=bp.text)
        )
        await self.session.execute(settings)
        await self.session.commit()

    async def set_custom_personality(self, user_id: int, name: str) -> None:
        """установка кастомной личности бота"""
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
        )
        cp = await self.session.scalar(stmt)
        settings = (
            update(Settings)
            .where(Settings.user_id == user_id)
            .values(personality_name=cp.name, personality_text=cp.text)
        )
        await self.session.execute(settings)
        await self.session.commit()

    async def is_custom_personality_exists(
        self, user_id: int, name: str
    ) -> bool:
        """Проверяет существует ли кастомная личность"""
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
        )
        cp = await self.session.scalar(stmt)
        return bool(cp)

    async def add_message_to_history(
        self, user_id: int, role: str, content: str
    ) -> None:
        """Добавляет сообщение в историю беседы."""
        message = ConversationHistory(
            user_id=user_id, role=role, content=content
        )
        self.session.add(message)
        await self.session.commit()
        logger.info(f"Сообщение добавлено в историю для user_id={user_id}")

    async def get_conversation_history(
        self, user_id: int, limit: int = 10
    ) -> List[ConversationHistory]:
        """Получает последние сообщения из истории беседы."""
        stmt = (
            select(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
            .order_by(ConversationHistory.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_full_conversation_history(
        self, user_id: int
    ) -> List[ConversationHistory]:
        """Получает полную историю беседы для пользователя."""
        stmt = (
            select(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
            .order_by(ConversationHistory.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def clear_conversation_history(self, user_id: int) -> None:
        """Очищает историю беседы для пользователя."""
        stmt = delete(ConversationHistory).where(
            ConversationHistory.user_id == user_id
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"История беседы очищена для user_id={user_id}")

    async def get_history_count(self, user_id: int) -> int | None:
        history_count = await self.session.scalar(
            select(func.count())
            .select_from(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
        )
        return history_count
