from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from tgbot.models.models import (
    ChatSettings,
    Settings,
    SummarySettings,
)
from tgbot.services.repository.base import BaseService


class SettingsService(BaseService):
    async def get_settings(self, user_id: int) -> Settings | None:
        stmt = (
            select(Settings)
            .where(Settings.user_id == user_id)
            .options(
                selectinload(Settings.chat_settings),
                selectinload(Settings.summary_settings),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_max_token(self, user_id: int, max_tokens: int) -> None:
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(max_tokens=max_tokens)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} установил {max_tokens} токенов")

    async def update_settings(self, user_id: int, model: str) -> None:
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(model=model)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} обновил модель на {model}")

    async def update_summary_type(self, user_id: int, type: str) -> None:
        stmt = (
            update(SummarySettings)
            .where(
                SummarySettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(summary_type=type)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Пользователь {user_id} обновил формат пересказа на {type}"
        )

    async def update_chat_export_format(
        self, user_id: int, export_format: str
    ) -> None:
        """Обновляет формат экспорта пересказчика"""
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(export_format=export_format)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Пользователь {user_id} обновил формат экспорта чата на {export_format}"
        )

    async def update_temperature(self, user_id: int, temperature: str) -> None:
        """Обновляет температуру в настройках чата"""
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(temperature=temperature)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(
            f"Пользователь {user_id} обновил температуру на {temperature}"
        )

    async def update_summary_api_key(self, user_id: int, api_key: str) -> None:
        """Обновляет API ключ для пересказчика"""
        stmt = (
            update(SummarySettings)
            .where(
                SummarySettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(api_key=api_key)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} обновил API ключ чата")

    async def update_chat_api_key(self, user_id: int, api_key: str) -> None:
        """Обновляет API ключ для чата"""
        stmt = (
            update(ChatSettings)
            .where(
                ChatSettings.settings_id
                == select(Settings.id)
                .where(Settings.user_id == user_id)
                .scalar_subquery()
            )
            .values(api_key=api_key)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} обновил API ключ пересказчика")
