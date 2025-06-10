from aiogram_dialog import DialogManager

from tgbot.models.models import Settings
from tgbot.services.repository import Repo


async def get_base_data(dialog_manager: DialogManager, **kwargs) -> dict:
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id: int = dialog_manager.bg()._event_context.user.id
    settings: Settings = await repo.get_settings(user_id)
    history_count: int = await repo.get_history_count(user_id)

    base_view = {
        "api_key": settings.api_key,
        "model": settings.model,
        "max_length": settings.max_tokens,
        "temperature": settings.temperature,
        "tts_voice": settings.tts_voice,
        "tts_speed": settings.tts_speed,
        "tts_model": settings.tts_model,
        "personality": settings.personality_name,
        "history_count": history_count or 0,
    }

    dialog_manager.dialog_data.update(base_view)
    return base_view
