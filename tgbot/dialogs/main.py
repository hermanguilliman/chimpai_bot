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
    await manager.start(Settings.select, data=manager.current_context().data)


async def get_main_data(repo: Repo, dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data
    settings: AISettings = await repo.get_user_settings(data.get('user_id'))
    # какой то костыль получается, временное решение для обновления данных в бд
    if data.get('new_model'):
        print('got new model', data.get('new_model'))
        # await repo.update_model(data.get('user_id'), data.get('new_model'))
    if data.get('new_max_length'):
        print("Обнаружена новая хуйня:", data)
        # await repo.update_model(data.get('user_id'), data.get('new_max_length'))
    if data.get('new_temperature'):
        print(data.get('new_temperature'))
        # await repo.update_model(data.get('user_id'), data.get('new_temperature'))


    base = {
        'full_name': data.get('full_name'),
        'model': settings.model,
        'max_length': settings.max_tokens,
        'temperature': settings.temperature,
    }
    return base


main_dialog = Dialog(
    Window(
        # Главное окно
        Const("<b>ChimpAI [beta]</b>\n"),
        Format("Привет, <b>{full_name}</b>!\n", when='full_name'),
        Format("Активная модель: {model}", when='model'),
        Format("Максимальная длина: {max_length}", when='max_length'),
        Format("Температура: {temperature}", when='temperature'),
        # Start(Const("🛠 Настройки"), id='settings', state=Settings.select, data="user_id"),
        Button(Const("🛠 Настройки"), id='settings', on_click=show_settings),
        state=Main.main,
        getter=get_main_data,
        parse_mode='HTML',
        preview_data={
            'full_name':'Незнакомец',
        }
    ),
)