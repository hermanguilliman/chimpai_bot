import html

from aiogram_dialog import DialogManager

from tgbot.misc.text_tools import get_short_id
from tgbot.models.models import Settings
from tgbot.services.neural import OpenAIService
from tgbot.services.repository import Repo


async def get_data_model_selector(dialog_manager: DialogManager, **kwargs):
    # Получаем список моделей доступных в OpenAI
    repo: Repo = dialog_manager.middleware_data.get("repo")
    openai: OpenAIService = dialog_manager.middleware_data.get("openai")
    settings: Settings = await repo.get_settings(
        dialog_manager.bg()._event_context.user.id
    )

    engines = await openai.get_engines(api_key=settings.api_key)
    if isinstance(engines, list):
        engine_ids = [engine.id for engine in engines]
    else:
        engine_ids = ["gpt-4o-mini"]

    # Сортируем модели по названию
    engine_ids.sort()

    # Генерируем сокращенные id для передачи в кнопки
    short_model_ids = [get_short_id(engine_id) for engine_id in engine_ids]

    # Сохраняем сопоставление в контексте сессии
    dialog_manager.dialog_data["model_mapping"] = {
        short_id: full_id for short_id, full_id in zip(short_model_ids, engine_ids)
    }

    # Возвращаем сокращенные id для кнопок
    return {
        "models": zip(
            short_model_ids, engine_ids
        )  # Пара (короткий id, полное название)
    }


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
async def get_temperature(dialog_manager: DialogManager, **kwargs):
    # При первом запуске получаем значение из предыдущего диалога?
    if len(dialog_manager.dialog_data) == 0:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    return dialog_manager.dialog_data
