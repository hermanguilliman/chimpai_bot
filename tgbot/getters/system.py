from aiogram_dialog import DialogManager

from tgbot.models.models import ChatSettings
from tgbot.services.repository import Repo


async def system_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id: int = dialog_manager.bg()._event_context.user.id
    settings: ChatSettings = await repo.get_settings(user_id)
    data = {
        "chat_api_key": True if settings.chat_settings.api_key else None,
        "chat_base_url": settings.chat_settings.base_url or None,
        "summary_api_key": True if settings.summary_settings.api_key else None,
        "summary_base_url": settings.summary_settings.base_url or None,
    }

    return data
