from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from typing import Any

from aiogram_dialog import Dialog, DialogManager, Window, ChatEvent, Data
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Next, Cancel, Back, Row, Start, Select, SwitchTo, Column, Group
from aiogram_dialog.widgets.input import MessageInput
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from tgbot.services.openai import OpenAIService


class Main(StatesGroup):
    main = State()


class Settings(StatesGroup):
    select = State()
    model = State()
    max_length = State()
    temperature = State()


async def show_settings(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    """ Стартует диалог с настройками"""
    await manager.start(Settings.select, data=manager.current_context().data)


async def on_max_length_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager,
                         item_id: str):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    repo: Repo = manager.data['repo']
    user_id = manager.current_context().start_data['user_id']
    await repo.update_user_max_tokens(user_id=user_id, max_tokens=item_id)
    await manager.done()


async def get_model_selector(openai: OpenAIService, dialog_manager: DialogManager, **kwargs):
    engines = await openai.get_engines()
    return [
        {'engines': engines,}
    ]

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

# Главный диалог
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

# Диалог настроек
settings_dialog = Dialog(
    Window(
        # Окно выбора настроек
        Const('<b>Выберите параметр, который хотели бы изменить:</b>'),
        Row(
        SwitchTo(Const('🤖 Модель'), id='set_model', state=Settings.model),
        SwitchTo(Const('📏 Длина'), id='set_max_length', state=Settings.max_length),
        SwitchTo(Const('🌡️ Температура'), id='set_temperature', state=Settings.temperature),
        ),
        Cancel(Const('🙊 Отмена')),
        state=Settings.select,
        parse_mode='HTML',

    ),
    Window(
        # Список доступных моделей
        Const("<b>Выберите модель из списка:</b>"),

        Cancel(Const('🙊 Отмена')),
        state=Settings.model,
        parse_mode='HTML',
    ),
    Window(
        # окно выбора максимального числа токенов на запрос,
        # для разных моделей диапазон отличается
        # например от 1 до 4000 для модели text-davinci-003
        Const("<b>Укажите максимальное число токенов расходуемое для ответа нейросети:</b>"),
        Group(
            Select(
                Format("{item}"),
                items=list(range(0, 4000+1, 100)),
                item_id_getter=lambda x: x,
                id='select_max_length',
                on_click=on_max_length_selected,
            ),
            width=5,
        ),
        Cancel(Const('🙊 Отмена')),
        state=Settings.max_length,
        parse_mode='HTML',
    ),
    Window(
        # окно выбора температуры 
        # от 0.00 до 1.00 с двумя знаками после запятой
        Const("Укажите температуру"),
        Cancel(Const('🙊 Отмена')),
        state=Settings.temperature,
        parse_mode='HTML',
    ),
)