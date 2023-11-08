from aiogram_dialog import DialogManager

from tgbot.misc.personality import personality_base
from tgbot.models.settings import Settings
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo


async def get_data_model_selector(dialog_manager: DialogManager, **kwargs):
    # Получаем список моделей доступных в OpenAI
    repo: Repo = dialog_manager.middleware_data.get("repo")
    openai: OpenAIService = dialog_manager.middleware_data.get("openai")
    settings: Settings = await repo.get_settings(dialog_manager.bg().user.id)

    engines = await openai.get_engines(api_key=settings.api_key)
    if engines is not list:
        engine_ids = [engine.id for engine in engines]
    else:
        engine_ids = ["gpt-3.5-turbo"]
    return {
        "models": engine_ids,
    }


async def get_person_selector(dialog_manager: DialogManager, **kwargs):
    # Получаем список личностей
    return {
        "persons": [person["person"] for person in personality_base],
    }


# Геттер температуры
async def get_temperature(dialog_manager: DialogManager, **kwargs):
    # При первом запуске получаем значение из предыдущего диалога?
    if len(dialog_manager.dialog_data) == 0:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    return dialog_manager.dialog_data
