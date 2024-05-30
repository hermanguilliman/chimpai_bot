from aiogram_dialog import DialogManager

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


async def basic_person_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем список личностей
    repo: Repo = dialog_manager.middleware_data.get("repo")
    pb_list = await repo.get_basic_personality_list()
    return {
        "persons": pb_list,
    }


async def custom_person_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем список личностей
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id = dialog_manager.bg().user.id
    cp_list = await repo.get_custom_personality_list(user_id=user_id)

    return {
        "persons": cp_list,
    }


async def activate_custom_personality_getter(
        dialog_manager: DialogManager, **kwargs):
    # Показываем название и описание кастомной личности
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id = dialog_manager.bg().user.id
    custom_name = dialog_manager.dialog_data.get("custom_name")
    custom_desc = await repo.get_custom_personality(
        user_id=user_id,
        personality_name=custom_name)

    return {
        "custom_name": custom_name,
        "custom_desc": custom_desc,
    }


# Геттер температуры
async def get_temperature(dialog_manager: DialogManager, **kwargs):
    # При первом запуске получаем значение из предыдущего диалога?
    if len(dialog_manager.dialog_data) == 0:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    return dialog_manager.dialog_data
