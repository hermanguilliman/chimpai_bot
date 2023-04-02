from aiogram_dialog import DialogManager
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo
from tgbot.models.aisettings import AISettings
from tgbot.misc.personality import personality

async def get_data_model_selector(openai: OpenAIService, dialog_manager: DialogManager, **kwargs):
    # Получаем список моделей доступных в OpenAI
    repo: Repo = dialog_manager.data['repo']
    settings: AISettings = await repo.get_user_settings(dialog_manager.bg().user.id)
    engines = await openai.get_engines(api_key=settings.api_key)
    if engines is not list:
        engine_ids = [engine['id'] for engine in engines['data']]
    else:
        engine_ids = ["gpt-3.5-turbo"]
    return {
        'models': engine_ids,
    }


async def get_person_selector(openai: OpenAIService, dialog_manager: DialogManager, **kwargs):
    # Получаем список личностей
    return {
        'persons': [person['person'] for person in personality],
    }


# Геттер температуры
async def get_temperature(dialog_manager: DialogManager, **kwargs):
    # При первом запуске получаем значение из предыдущего диалога?
    dialog_data = dialog_manager.current_context().dialog_data
    if len(dialog_data)==0:
        dialog_manager.current_context().dialog_data.update(dialog_manager.current_context().start_data)
    return dialog_data
    