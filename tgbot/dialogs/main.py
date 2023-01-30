from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from tgbot.dialogs.settings import Settings
from aiogram.types import CallbackQuery


class Main(StatesGroup):
    main = State()


async def show_settings(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    """ Стартует диалог с настройками"""
    data = manager.current_context().dialog_data
    await manager.start(Settings.select, data=data)


async def get_main_data(repo: Repo, dialog_manager: DialogManager, **kwargs) -> dict:
    # Здесь происходит первичный запрос данных из команды запустившей диалог и бд 
    start_data = dialog_manager.current_context().start_data
    user_id:int = start_data.get('user_id')
    full_name:str = start_data.get('full_name')
    settings: AISettings = await repo.get_user_settings(user_id)

    # Задача: вернуть данные для текущего контекста 
    # базовая схема с данными, которая доступна после старта
    base_view:dict = {
        'user_id': user_id,
        'full_name': full_name,
        'model': settings.model,
        'max_length': settings.max_tokens,
        'temperature': settings.temperature,
    }

    # обновляем текущий контекст?
    dialog_manager.current_context().dialog_data.update(base_view)
    return base_view


main_dialog = Dialog(
    Window(
        # Главное окно
        Const("<b>ChimpAI 🐵 [v0.1 beta]</b>\n"),
        # Format("Привет, <b>{full_name}</b>!\n", when='full_name'),
        Format("🤖 Выбрана модель: <b>{model}</b>", when='model'),
        Format("🔋 Длина ответа: <b>{max_length}</b>", when='max_length'),
        Format("🌡 Температура: <b>{temperature}</b>", when='temperature'),
        Button(Const("📝 Параметры"), id='settings', on_click=show_settings),
        state=Main.main,
        getter=get_main_data,
        parse_mode='HTML',
        preview_data={
            'full_name':'братик',
        }
    ),
)