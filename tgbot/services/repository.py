from datetime import datetime
from typing import List

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
        settings = AISettings(max_tokens=1024, model="text-davinci-003", temperature="0.7", user=user)
        self.session.add(user)
        self.session.add(settings)
        await self.session.commit()

    async def get_user(self, user_id: int) -> Users | None:
        """получить все данные о пользователе по id"""
        return await self.session.get(Users, user_id)
    
    async def get_user_settings(self, user_id: int) -> AISettings | None:
        # Выбрать настройку пользователя user_id
        stmt = select(AISettings).where(AISettings.user_id == user_id)
        settings = await self.session.scalar(stmt)
        return settings

    async def update_user_full_name(self, user_id: int, fullname: str) -> None:
        """update full_name of exist user / обновляет """
        stmt = (
            update(Users).
            where(Users.id == user_id).
            values(full_name=fullname)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_user(self, user_id):
        """ delete user by id / удаляем пользователя по id"""
        stmt = delete(Users).where(Users.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    # bonus data of users

    async def list_users(self) -> List:
        """ return count of users / возвращаем список всех пользователей """
        rows = select(Users)
        result = await self.session.execute(rows)
        curr = result.scalars()
        return list(curr)

