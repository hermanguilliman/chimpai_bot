from aiogram_dialog import DialogManager

from tgbot.models.personality import Personality
from tgbot.models.settings import Settings
from tgbot.services.repository import Repo


async def get_base_data(dialog_manager: DialogManager, **kwargs) -> dict:
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id: int = dialog_manager.bg().user.id
    full_name: str = dialog_manager.bg().user.full_name
    settings: Settings = await repo.get_settings(user_id)
    personality: Personality = await repo.get_personality(user_id)

    base_view = {
        "user_id": user_id,
        "full_name": full_name,
        "api_key": "✅ установлен" if settings.api_key else "⭕️ отсутствует",
        "model": settings.model if settings.model else "⭕️ отсутствует",
        "max_length": settings.max_tokens if settings.max_tokens else "⭕️ отсутствует",
        "temperature": settings.temperature
        if settings.temperature
        else "⭕️ отсутствует",
        "tts_voice": settings.tts_voice if settings.tts_voice else "alloy",
        "tts_speed": settings.tts_speed if settings.tts_speed else "1.0",
        "tts_model": settings.tts_model if settings.tts_model else "tts-1-hd",
        "personality": personality.name if personality else "💻 не используется",
    }

    dialog_manager.dialog_data.update(base_view)
    return base_view
