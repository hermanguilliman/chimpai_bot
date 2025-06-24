from typing import List

from loguru import logger
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from tgbot.models.models import (
    BaseUrl,
    BasicPersonality,
    ChatSettings,
    ConversationHistory,
    CustomPersonality,
    Settings,
    SummarySettings,
    Users,
)


class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_user(self, user_id: int) -> None:
        """Создаём пользователя с базовыми настройками"""
        user = Users(id=user_id)
        settings = Settings(user=user)
        chat_settings = ChatSettings(settings=settings)
        summary_settings = SummarySettings(settings=settings)

        self.session.add_all([user, settings, chat_settings, summary_settings])
        await self.session.commit()
        logger.info(f"Добавлен пользователь {user_id}")

    async def get_user(self, user_id: int) -> Users | None:
        """Получить все данные о пользователе по id с настройками"""
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
        """Удаляем пользователя по id"""
        stmt = delete(Users).where(Users.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} удален")

    async def list_users(self) -> List[Users]:
        """Возвращаем список всех пользователей"""
        stmt = select(Users)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_settings(self, user_id: int) -> Settings | None:
        """Возвращает настройки пользователя по user_id"""
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
        """Обновляет максимальное количество токенов в настройках чата"""
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
        """Обновляет модель в настройках чата"""
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

    async def get_custom_personality_list(
        self, user_id: int
    ) -> List[CustomPersonality]:
        """Возвращает все кастомные личности по user_id"""
        stmt = select(CustomPersonality).where(
            CustomPersonality.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_custom_personality(
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

    async def get_basic_personality_list(self) -> List[BasicPersonality]:
        """Возвращает список стандартных личностей"""
        stmt = select(BasicPersonality)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_base_urls(
        self,
    ) -> list[BaseUrl] | None:
        """Возвращает список базовых адресов апи"""
        stmt = select(BaseUrl.id, BaseUrl.name)
        result = await self.session.execute(stmt)
        base_urls = result.all()
        return base_urls or None

    async def set_chat_base_url(self, user_id: int, name: str) -> None:
        """Устанавливает базовый адрес API для чата"""
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

    async def add_custom_personality(
        self, user_id: int, name: str, text: str
    ) -> None:
        """Добавляет кастомную личность"""
        personality = CustomPersonality(name=name, text=text, user_id=user_id)
        self.session.add(personality)
        await self.session.commit()
        logger.info(f"Пользователь {user_id} добавил личность {name}")

    async def select_basic_personality(self, user_id: int, name: str) -> None:
        """Устанавливает стандартную личность бота"""
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

    async def set_custom_personality(self, user_id: int, name: str) -> None:
        """Устанавливает кастомную личность бота"""
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

    async def add_message_to_history(
        self, user_id: int, role: str, content: str
    ) -> None:
        """Добавляет сообщение в историю беседы"""
        message = ConversationHistory(
            user_id=user_id, role=role, content=content
        )
        self.session.add(message)
        await self.session.commit()
        logger.info(f"Сообщение добавлено в историю для user_id={user_id}")

    async def get_conversation_history(
        self, user_id: int, limit: int = 10
    ) -> List[ConversationHistory]:
        """Получает последние сообщения из истории беседы"""
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
        """Получает полную историю беседы для пользователя"""
        stmt = (
            select(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
            .order_by(ConversationHistory.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def clear_conversation_history(self, user_id: int) -> None:
        """Очищает историю беседы для пользователя"""
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
