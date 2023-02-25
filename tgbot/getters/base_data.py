
from aiogram_dialog import DialogManager
from tgbot.services.repository import Repo
from tgbot.models.aisettings import AISettings


async def get_base_data(repo: Repo, dialog_manager: DialogManager, **kwargs) -> dict:
    # Здесь происходит первичный запрос данных из команды запустившей диалог и бд 
    user_id:int = dialog_manager.bg().user.id
    full_name:str = dialog_manager.bg().user.full_name
    settings: AISettings = await repo.get_user_settings(user_id)
    chimpai:int = dialog_manager.current_context().dialog_data.get('chimpai', 'ChimpAI')

    base_view:dict = {
        'user_id': user_id,
        'chimpai': chimpai,
        'full_name': full_name,
        'api_key': '✅ Установлен' if settings.api_key else '❌ Отсутствует',
        'model': settings.model if settings.model else 'отсутствует',
        'max_length': settings.max_tokens if settings.max_tokens else '❌ Отсутствует',
        'temperature': settings.temperature if settings.temperature else '❌ Отсутствует',
    }

    # обновляем текущий контекст?
    dialog_manager.current_context().dialog_data.update(base_view)
    return base_view