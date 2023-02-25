from aiogram_dialog import DialogManager
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo
from tgbot.models.aisettings import AISettings

async def get_data_model_selector(openai: OpenAIService, dialog_manager: DialogManager, **kwargs):
    # Получаем список моделей доступных в OpenAI
    repo: Repo = dialog_manager.data['repo']
    settings: AISettings = await repo.get_user_settings(dialog_manager.bg().user.id)
    engines = await openai.get_engines(api_key=settings.api_key)
    engine_ids = [engine['id'] for engine in engines['data']]
    return {
        'models': engine_ids,
    }


# Геттер температуры
async def get_temperature(dialog_manager: DialogManager, **kwargs):
    # При первом запуске получаем значение из предыдущего диалога?
    dialog_data = dialog_manager.current_context().dialog_data
    if len(dialog_data)==0:
        dialog_manager.current_context().dialog_data.update(dialog_manager.current_context().start_data)
    return dialog_data
    

async def settings_getter(dialog_manager: DialogManager, **kwargs):
    datatest = dialog_manager.current_context().dialog_data
    print('DATATEST!!!', datatest)
    # dialog_manager.current_context().dialog_data.update(datatest)
    return dialog_manager.current_context().dialog_data