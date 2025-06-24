import html

from aiogram_dialog import DialogManager

from tgbot.misc.text_tools import get_short_id
from tgbot.models.models import Settings
from tgbot.services.neural import NeuralChatService
from tgbot.services.repository.api_urls import BaseUrlService
from tgbot.services.repository.personalities import (
    BasicPersonalityService,
    CustomPersonalityService,
)
from tgbot.services.repository.settings import SettingsService


async def models_selector_getter(dialog_manager: DialogManager, **kwargs):
    settings_service: SettingsService = dialog_manager.middleware_data.get(
        "settings_service"
    )
    openai: NeuralChatService = dialog_manager.middleware_data.get("openai")
    settings: Settings = await settings_service.get_settings(
        dialog_manager.bg()._event_context.user.id
    )
    search_query = dialog_manager.dialog_data.get("search_query", "").lower()

    engines = await openai.get_engines(
        base_url=settings.chat_settings.base_url,
        api_key=settings.chat_settings.api_key,
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
    basic_personality_service: BasicPersonalityService = (
        dialog_manager.middleware_data.get("basic_personality_service")
    )
    pb_list = await basic_personality_service.get_basic_personality_list()
    return {
        "persons": pb_list,
    }


async def custom_person_list_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем список личностей
    custom_personality_service: CustomPersonalityService = (
        dialog_manager.middleware_data.get("custom_personality_service")
    )
    user_id = dialog_manager.bg()._event_context.user.id
    cp_list = await custom_personality_service.get_custom_personality_list(
        user_id=user_id
    )

    return {
        "persons": cp_list,
    }


async def custom_personality_getter(dialog_manager: DialogManager, **kwargs):
    # Показываем название и описание кастомной личности
    custom_personality_service: CustomPersonalityService = (
        dialog_manager.middleware_data.get("custom_personality_service")
    )
    user_id = dialog_manager.bg()._event_context.user.id
    custom_name = dialog_manager.dialog_data.get("custom_name")
    custom_desc = (
        await custom_personality_service.get_custom_personality_description(
            user_id=user_id, personality_name=custom_name
        )
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
    base_url_service: BaseUrlService = dialog_manager.middleware_data.get(
        "base_url_service"
    )
    settings_service: SettingsService = dialog_manager.middleware_data.get(
        "settings_service"
    )
    user_id = dialog_manager.bg()._event_context.user.id
    settings = await settings_service.get_settings(user_id=user_id)
    url_list = await base_url_service.get_base_urls()
    return {
        "current_base_url": settings.chat_settings.base_url,
        "base_urls": url_list,
    }
