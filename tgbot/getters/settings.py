import html

from aiogram_dialog import DialogManager

from tgbot.misc.text_tools import get_short_id
from tgbot.models.models import Settings
from tgbot.services.neural import OpenAIService
from tgbot.services.repository import Repo


async def models_selector_getter(dialog_manager: DialogManager, **kwargs):
    repo: Repo = dialog_manager.middleware_data.get("repo")
    openai: OpenAIService = dialog_manager.middleware_data.get("openai")
    settings: Settings = await repo.get_settings(
        dialog_manager.bg()._event_context.user.id
    )
    search_query = dialog_manager.dialog_data.get("search_query", "").lower()

    engines = await openai.get_engines(
        base_url=settings.base_url, api_key=settings.api_key
    )
    if isinstance(engines, list):
        engine_ids = [engine.id for engine in engines]
    else:
        engine_ids = ["gpt-4o-mini"]

    engine_ids.sort()
    short_model_ids = [get_short_id(engine_id) for engine_id in engine_ids]

    if search_query:
        filtered_pairs = [
            (short_id, full_id)
            for short_id, full_id in zip(short_model_ids, engine_ids)
            if search_query in short_id.lower()
            or search_query in full_id.lower()
        ]
    else:
        filtered_pairs = list(zip(short_model_ids, engine_ids))

    dialog_manager.dialog_data["model_mapping"] = {
        short_id: full_id for short_id, full_id in filtered_pairs
    }

    return {"models": filtered_pairs}


async def basic_person_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем список личностей
    repo: Repo = dialog_manager.middleware_data.get("repo")
    pb_list = await repo.get_basic_personality_list()
    return {
        "persons": pb_list,
    }


async def custom_person_list_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем список личностей
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id = dialog_manager.bg()._event_context.user.id
    cp_list = await repo.get_custom_personality_list(user_id=user_id)

    return {
        "persons": cp_list,
    }


async def custom_personality_getter(dialog_manager: DialogManager, **kwargs):
    # Показываем название и описание кастомной личности
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id = dialog_manager.bg()._event_context.user.id
    custom_name = dialog_manager.dialog_data.get("custom_name")
    custom_desc = await repo.get_custom_personality(
        user_id=user_id, personality_name=custom_name
    )

    return {
        "custom_name": html.escape(custom_name),
        "custom_desc": html.escape(custom_desc),
    }


# Геттер температуры
async def temperature_getter(dialog_manager: DialogManager, **kwargs):
    # При первом запуске получаем значение из предыдущего диалога?
    if len(dialog_manager.dialog_data) == 0:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    return dialog_manager.dialog_data


async def base_urls_getter(dialog_manager: DialogManager, **kwargs):
    repo: Repo = dialog_manager.middleware_data.get("repo")
    user_id = dialog_manager.bg()._event_context.user.id
    current_base_url = await repo.get_settings(user_id=user_id)
    url_list = await repo.get_base_urls()
    return {
        "current_base_url": current_base_url.base_url,
        "base_urls": url_list,
    }
