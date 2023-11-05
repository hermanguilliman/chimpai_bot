from typing import List

from loguru import logger
from sqlalchemy import delete, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from tgbot.models.personality import Personality
from tgbot.models.settings import Settings
from tgbot.models.user import Users


class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_user(self,
                       user_id: int,
                       fullname: str,
                       language_code: str) -> None:
        """создаём пользователя с базовыми настройками"""
        user = Users(id=user_id,
                     full_name=fullname,
                     language_code=language_code,)
        settings = Settings(
            max_tokens=256,
            model="gpt-3.5-turbo",
            temperature="0.7",
            user=user,)
        self.session.add(user)
        self.session.add(settings)
        await self.session.commit()
        logger.info("Добавлен пользователь")

    async def get_user(self, user_id: int) -> Users | None:
        """получить все данные о пользователе по id"""
        return await self.session.get(Users, user_id)

    async def update_full_name(self, user_id: int, fullname: str) -> None:
        """обновляет пользователя по id"""
        stmt = update(Users).where(Users.id == user_id).values(full_name=fullname)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} сменил имя на {fullname}")

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
            f"Пользователь {user_id} установил длину ответа {max_tokens} токенов"
        )

    async def update_settings(self, user_id: int, model: str) -> None:
        # Обновляет настройки
        stmt = update(Settings).where(Settings.user_id == user_id).values(model=model)
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
            update(Settings).where(Settings.user_id == user_id).values(api_key=api_key)
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
            update(Personality)
            .where(Personality.user_id == user_id)
            .values(name=name, text=text)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_personality(self, user_id: int) -> Personality | None:
        # Возвращает личность по user_id
        stmt = select(Personality).where(Personality.user_id == user_id)
        personality = await self.session.scalar(stmt)
        return personality

    async def delete_personality(self, user_id: int) -> None:
        stmt = text(f"DELETE FROM personality WHERE user_id = {user_id}")
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} удалил личность")

    async def add_new_personality(self, user_id: int, name: str, text: str) -> None:
        personality = Personality(name=name, text=text, user_id=user_id)
        self.session.add(personality)
        await self.session.commit()
