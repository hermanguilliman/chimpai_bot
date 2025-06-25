from aiogram_dialog import DialogManager

from tgbot.models.models import ChatSettings
from tgbot.services.repository.settings import SettingsService


async def summary_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    settings_service: SettingsService = dialog_manager.middleware_data.get(
        "settings_service"
    )
    user_id: int = dialog_manager.event.from_user.id
    settings: ChatSettings = await settings_service.get_settings(user_id)
    summary_type_mapping = {"detailed": "подробный", "short": "краткий"}
    summary_type = settings.summary_settings.summary_type
    data = {
        "summary_type": summary_type_mapping.get(summary_type, None)
        if summary_type
        else None,
    }

    return data
