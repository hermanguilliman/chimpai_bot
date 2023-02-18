from typing import List
from loguru import logger
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from tgbot.models.user import Users
from tgbot.models.aisettings import AISettings


class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    # user operations
    async def add_user(self, user_id: int, fullname: str, language_code: str) -> None:
        """add new user / создаём пользователя"""
        user = Users(id=user_id, full_name=fullname, language_code=language_code)
        settings = AISettings(max_tokens=256, model="text-davinci-003", temperature="0.7", user=user)
        self.session.add(user)
        self.session.add(settings)
        await self.session.commit()
        logger.debug('Добавлен пользователь')

    async def get_user(self, user_id: int) -> Users | None:
        """получить все данные о пользователе по id"""
        return await self.session.get(Users, user_id)
    
    async def update_user_full_name(self, user_id: int, fullname: str) -> None:
        """update full_name of exist user / обновляет """
        stmt = (
            update(Users).
            where(Users.id == user_id).
            values(full_name=fullname)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.debug('Пользователь обновлен')

    async def delete_user(self, user_id):
        """ delete user by id / удаляем пользователя по id"""
        stmt = delete(Users).where(Users.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.debug('Пользователь удален')

    async def list_users(self) -> List:
        """ return count of users / возвращаем список всех пользователей """
        rows = select(Users)
        result = await self.session.execute(rows)
        curr = result.scalars()
        return list(curr)

    async def get_user_settings(self, user_id: int) -> AISettings | None:
        # Выбрать настройку пользователя user_id
        stmt = select(AISettings).where(AISettings.user_id == user_id)
        settings = await self.session.scalar(stmt)
        logger.debug('Получены настройки')
        return settings

    async def update_user_max_tokens(self, user_id: int, max_tokens: int) -> None:
        stmt = (
            update(AISettings).
            where(AISettings.user_id == user_id).
            values(max_tokens=max_tokens)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.debug('Токен обновлен')

    async def update_user_settings_model(self, user_id: int, model: str) -> None:
        stmt = (
            update(AISettings).
            where(AISettings.user_id == user_id).
            values(model=model)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.debug('Модель обновлена')

    async def update_temperature(self, user_id: int, temperature: str) -> None:
        stmt = (
            update(AISettings).
            where(AISettings.user_id == user_id).
            values(temperature=temperature)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.debug('Температура обновлена')

    async def update_user_api_key(self, user_id: int, api_key: str) -> None:
        stmt = (
            update(AISettings).
            where(AISettings.user_id == user_id).
            values(api_key=api_key)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.debug('Апи ключ обновлен')