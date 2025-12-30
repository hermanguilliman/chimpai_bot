from aiogram_dialog import DialogManager

from tgbot.models.models import ChatSettings
from tgbot.services.repository.settings import SettingsService


async def system_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    settings_service: SettingsService = dialog_manager.middleware_data.get(
        "settings_service"
    )
    user_id: int = dialog_manager.event.from_user.id
    settings: ChatSettings = await settings_service.get_settings(user_id)
    data = {
        "chat_api_key": True if settings.chat_settings.api_key else None,
        "chat_base_url": settings.chat_settings.base_url or None,
    }

    return data
