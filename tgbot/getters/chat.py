from aiogram_dialog import DialogManager

from tgbot.models.models import ChatSettings
from tgbot.services.repository import Repo


async def chat_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id: int = dialog_manager.bg()._event_context.user.id
    settings: ChatSettings = await repo.get_settings(user_id)
    history_count: int = await repo.get_history_count(user_id)
    data = {
        "api_key": True if settings.chat_settings.api_key else None,
        "model": settings.chat_settings.model,
        "max_length": settings.chat_settings.max_tokens,
        "temperature": settings.chat_settings.temperature,
        "personality": settings.chat_settings.personality_name,
        "history_count": history_count or 0,
        "base_url": settings.chat_settings.base_url or None,
        "export_format": settings.chat_settings.export_format,
    }

    dialog_manager.dialog_data.update(data)
    return data
