from typing import List, Optional
from uuid import uuid4

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

    async def get_custom_personality(
        self, user_id: int, personality_name: str
    ) -> Optional[CustomPersonality]:
        """Возвращает объект кастомной личности по имени и user_id"""
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == personality_name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def generate_shared_token(
        self, user_id: int, personality_name: str
    ) -> Optional[str]:
        """Генерирует и сохраняет уникальный shared_token для кастомной личности"""
        # Находим кастомную личность
        stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == user_id)
            .where(CustomPersonality.name == personality_name)
        )
        result = await self.session.execute(stmt)
        personality = result.scalars().first()

        if not personality:
            logger.error(
                f"Кастомная личность {personality_name} для user_id={user_id} не найдена"
            )
            return None

        # Генерируем уникальный токен
        max_attempts = 5
        for _ in range(max_attempts):
            shared_token = str(uuid4())
            # Проверяем уникальность токена
            token_check_stmt = select(CustomPersonality).where(
                CustomPersonality.shared_token == shared_token
            )
            token_exists = await self.session.execute(token_check_stmt)
            if not token_exists.scalars().first():
                # Обновляем shared_token
                update_stmt = (
                    update(CustomPersonality)
                    .where(CustomPersonality.user_id == user_id)
                    .where(CustomPersonality.name == personality_name)
                    .values(shared_token=shared_token)
                )
                await self.session.execute(update_stmt)
                await self.session.commit()
                logger.info(
                    f"Установлен shared_token для личности {personality_name} user_id={user_id}"
                )
                return shared_token

        logger.error(
            f"Не удалось сгенерировать уникальный shared_token для личности {personality_name} после {max_attempts} попыток"
        )
        return None

    async def copy_custom_personality_by_shared_token(
        self, shared_token: str, new_user_id: int
    ) -> Optional[CustomPersonality]:
        """Ищет CustomPersonality по shared_token и копирует её для нового пользователя"""
        # Находим личность по shared_token
        stmt = select(CustomPersonality).where(
            CustomPersonality.shared_token == shared_token
        )
        result = await self.session.execute(stmt)
        original_personality = result.scalars().first()

        if not original_personality:
            logger.error(
                f"Кастомная личность с shared_token={shared_token} не найдена"
            )
            return None

        # Проверяем, не существует ли уже личность с таким именем у нового пользователя
        check_stmt = (
            select(CustomPersonality)
            .where(CustomPersonality.user_id == new_user_id)
            .where(CustomPersonality.name == original_personality.name)
        )
        existing_personality = await self.session.execute(check_stmt)
        if existing_personality.scalars().first():
            logger.error(
                f"Личность с именем {original_personality.name} уже существует у пользователя {new_user_id}"
            )
            return None

        # Генерируем новый уникальный shared_token
        max_attempts = 5
        new_shared_token = None
        for _ in range(max_attempts):
            candidate_token = str(uuid4())
            token_check_stmt = select(CustomPersonality).where(
                CustomPersonality.shared_token == candidate_token
            )
            token_exists = await self.session.execute(token_check_stmt)
            if not token_exists.scalars().first():
                new_shared_token = candidate_token
                break

        if not new_shared_token:
            logger.error(
                f"Не удалось сгенерировать уникальный shared_token для нового пользователя {new_user_id}"
            )
            return None

        # Создаём новую личность
        new_personality = CustomPersonality(
            name=original_personality.name,
            text=original_personality.text,
            user_id=new_user_id,
            shared_token=new_shared_token,
        )
        self.session.add(new_personality)
        await self.session.commit()
        logger.info(
            f"Скопирована личность {original_personality.name} для пользователя {new_user_id} с новым shared_token={new_shared_token}"
        )
        return new_personality

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
