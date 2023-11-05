from aiogram_dialog import DialogManager

from tgbot.models.personality import Personality
from tgbot.models.settings import Settings
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo


async def get_base_data(dialog_manager: DialogManager, **kwargs) -> dict:
    # Здесь происходит первичный запрос данных из команды запустившей диалог и бд
    repo: Repo = dialog_manager.middleware_data.get("repo")
    openai: OpenAIService = dialog_manager.middleware_data.get("openai")
    
    user_id: int = dialog_manager.bg().user.id
    full_name: str = dialog_manager.bg().user.full_name
    settings: Settings = await repo.get_settings(user_id)
    personality: Personality = await repo.get_personality(user_id)
    dialog_manager.dialog_data["repo"] = repo
    dialog_manager.dialog_data["openai"] = openai

    base_view = {
        "user_id": user_id,
        "full_name": full_name,
        "api_key": "🛡 сохранён" if settings.api_key else "🤷‍♂️ отсутствует",
        "model": settings.model if settings.model else "🤷‍♂️ отсутствует",
        "max_length": settings.max_tokens if settings.max_tokens else "🤷‍♂️ отсутствует",
        "temperature": settings.temperature
        if settings.temperature
        else "🤷‍♂️ отсутствует",
        "personality": personality.name if personality else "💻 не используется",
    }

    # обновляем текущий контекст
    dialog_manager.dialog_data.update(base_view)
    return base_view
