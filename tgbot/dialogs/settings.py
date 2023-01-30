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


class Settings(StatesGroup):
    select = State()
    model = State()
    max_length = State()
    temperature = State()


async def on_new_model_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager,
                         item_id: str):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    repo: Repo = manager.data['repo']
    user_id = manager.current_context().start_data['user_id']
    await repo.update_user_model(user_id=user_id, model=item_id)
    await manager.done()


async def on_max_length_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager,
                         item_id: str):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    repo: Repo = manager.data['repo']
    user_id = manager.current_context().start_data['user_id']
    await repo.update_user_max_tokens(user_id=user_id, max_tokens=item_id)
    await manager.done()


async def get_data_model_selector(openai: OpenAIService, dialog_manager: DialogManager, **kwargs):
    engines = await openai.get_engines()
    engine_ids = [engine['id'] for engine in engines['data']]
    return {
        'models': engine_ids,
    }

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
        Group(
            Select(
                Format("{item}"),
                # нужно кинуть сюда список моделей
                items='models',
                item_id_getter=lambda x: x,
                id='select_max_new_model',
                on_click=on_new_model_selected,
            ),
            width=1,
        ),
        Cancel(Const('🙊 Отмена')),
        state=Settings.model,
        parse_mode='HTML',
        getter=get_data_model_selector,
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