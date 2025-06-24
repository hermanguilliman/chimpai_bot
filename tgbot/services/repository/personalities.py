from typing import List

from loguru import logger
from sqlalchemy import delete, select, update

from tgbot.models.models import (
    BasicPersonality,
    ChatSettings,
    CustomPersonality,
    Settings,
)
from tgbot.services.repository.base import BaseService


class CustomPersonalityService(BaseService):
    async def is_custom_personality_exists(
        self, user_id: int, name: str
    ) -> bool:
        """Проверяет, существует ли кастомная личность"""
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
        )
        cp = await self.session.scalar(stmt)
        return bool(cp)

    async def add_custom_personality(
        self, user_id: int, name: str, text: str
    ) -> None:
        personality = CustomPersonality(name=name, text=text, user_id=user_id)
        self.session.add(personality)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} добавил личность {name}")

    async def delete_custom_personality(self, user_id: int, name: str) -> None:
        """Удаляет кастомную личность"""
        stmt = (
            delete(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} удалил личность {name}")

    async def get_custom_personality_description(
        self, user_id: int, personality_name: str
    ) -> CustomPersonality | None:
        """Возвращает кастомную личность по имени и user_id"""
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == personality_name)
        )
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        return result.text

    async def get_custom_personality_list(
        self, user_id: int
    ) -> List[CustomPersonality]:
        stmt = select(CustomPersonality).where(
            CustomPersonality.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def set_custom_personality(self, user_id: int, name: str) -> None:
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
        )
        cp = await self.session.scalar(stmt)
        if not cp:
            raise ValueError(f"Custom personality {name} not found")
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(personality_name=cp.name, personality_text=cp.text)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} выбрал кастомную личность {name}")

    async def update_personality_name(
        self, user_id: int, name: str, new_name: str
    ) -> None:
        """Обновление имени кастомной личности"""
        stmt = (
            update(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
            .values(name=new_name)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Пользователь {user_id} обновил имя личности с {name} на {new_name}"
        )

    async def update_personality_text(
        self, user_id: int, name: str, new_text: str
    ) -> None:
        """Обновление текста кастомной личности"""
        stmt = (
            update(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == name)
            .values(text=new_text)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} обновил текст личности {name}")


class BasicPersonalityService(BaseService):
    async def get_basic_personality_list(self) -> List[BasicPersonality]:
        stmt = select(BasicPersonality)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def select_basic_personality(self, user_id: int, name: str) -> None:
        stmt = select(BasicPersonality).where(BasicPersonality.name == name)
        bp = await self.session.scalar(stmt)
        if not bp:
            raise ValueError(f"Basic personality {name} not found")
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(personality_name=bp.name, personality_text=bp.text)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Пользователь {user_id} выбрал стандартную личность {name}"
        )
