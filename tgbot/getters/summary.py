from aiogram_dialog import DialogManager

from tgbot.models.models import ChatSettings
from tgbot.services.repository import Repo


async def summary_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id: int = dialog_manager.bg()._event_context.user.id
    settings: ChatSettings = await repo.get_settings(user_id)
    data = {
        "summary_type": settings.summary_settings.summary_type or None,
    }

    return data
