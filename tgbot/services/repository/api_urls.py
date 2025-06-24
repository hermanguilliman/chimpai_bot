from loguru import logger
from sqlalchemy import select, update

from tgbot.models.models import (
    BaseUrl,
    ChatSettings,
    Settings,
)
from tgbot.services.repository.base import BaseService


class BaseUrlService(BaseService):
    async def get_base_urls(self) -> list[BaseUrl] | None:
        stmt = select(BaseUrl.id, BaseUrl.name)
        result = await self.session.execute(stmt)
        base_urls = result.all()
        return base_urls or None

    async def set_chat_base_url(self, user_id: int, name: str) -> None:
        stmt = select(BaseUrl).where(BaseUrl.name == name)
        base_url = await self.session.scalar(stmt)
        if not base_url:
            raise ValueError(f"Base URL with name {name} not found")
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(base_url=base_url.url)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Пользователь {user_id} установил базовый URL {base_url.url}"
        )

    async def set_chat_custom_base_url_to_user(
        self, user_id: int, new_url: str
    ) -> None:
        """Устанавливает пользователю собственный адрес API для чата"""
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(base_url=new_url)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Пользователь {user_id} установил свой адрес API {new_url}"
        )
