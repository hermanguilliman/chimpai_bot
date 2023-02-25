from tgbot.misc.states import Settings
from aiogram.types import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Cancel, Select, SwitchTo, Group
from aiogram_dialog.widgets.input import MessageInput
from tgbot.handlers.settings import api_key_handler
from tgbot.getters.settings import get_data_model_selector, get_temperature
from tgbot.getters.base_data import get_base_data
from tgbot.handlers.settings import api_key_handler
from tgbot.callbacks.settings import (
    on_decrease_temp,
    on_increase_temp,
    on_max_length_selected,
    on_new_model_selected,
    on_reset_temp,
    on_temperature_selected,
)


# Диалог настроек
settings_dialog = Dialog(
    Window(
        # Окно выбора настроек
        Const('<b>Выберите параметр, который хотели бы изменить:</b>'),
        Group(
        SwitchTo(Format('🔑 API ключ: {api_key}'), id='set_api_key', state=Settings.api_key, when='api_key'),
        SwitchTo(Format('🤖 Модель: {model}'), id='set_model', state=Settings.model, when='model'),
        SwitchTo(Format('🔋 Длина ответа: {max_length}'), id='set_max_length', state=Settings.max_length, when='max_length'),
        SwitchTo(Format('🌡️ Температура {temperature}'), id='set_temperature', state=Settings.temperature, when='temperature'),
        width=1),
        Cancel(Const('🤚 Отмена')),
        state=Settings.select,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
    Window(
        # Список доступных моделей
        MessageInput(api_key_handler, content_types=[ContentType.TEXT]),
        Const("<b>Укажите новый API ключ:</b>"),
        Const("Подсказка: OpenAI API ключ выглядит как <b>sk-...</b>"),
        Cancel(Const('🤚 Отмена')),
        state=Settings.api_key,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        # Список доступных моделей
        Const("<b>Выберите модель из списка:</b>"),
        Const("Подсказка: стандартное значение <b>text-davinci-003</b>"),
        Group(
            Select(
                Format("🤖 {item}"),
                # нужно кинуть сюда список моделей
                items='models',
                item_id_getter=lambda x: x,
                id='select_max_new_model',
                on_click=on_new_model_selected,
            ),
            width=1,
        ),
        Cancel(Const('🤚 Отмена')),
        state=Settings.model,
        parse_mode=ParseMode.HTML,
        getter=get_data_model_selector,
    ),
    Window(
        # окно выбора максимального числа токенов на запрос,
        # для разных моделей диапазон отличается
        # например от 1 до 4000 для модели text-davinci-003
        Const("<b>Укажите максимальную длину ответа:</b>"),
        Const("Подсказка: стандартное значение <b>256</b>, но лучше использовать <b>500+</b>"),
        Group(
            Select(
                Format("🔋 {item}"),
                items=list(range(100, 4000+1, 100)),
                item_id_getter=lambda x: x,
                id='select_max_length',
                on_click=on_max_length_selected,
            ),
            width=5,
        ),
        Cancel(Const('🤚 Отмена')),
        state=Settings.max_length,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        # окно выбора температуры 
        # от 0.00 до 1.00 с двумя знаками после запятой
        Const("Температура влияет на непредсказуемость ответа\nВыберите новое значение и нажмите на градусник."),
        Group(
            Button(Format('🌡 Установить значение: {temperature}'), id='new_temperature', when='temperature', on_click=on_temperature_selected),
            width=1,
        ),
        Group(
            Button(Const('🔻 0.1'), id='decrease', on_click=on_decrease_temp),
            Button(Const('0.1 🔺'), id='increase', on_click=on_increase_temp),
            width=2,
        ),
        Group(
            Button(Const('🌚 Как было'), id='reset_temp', on_click=on_reset_temp),
            Cancel(Const('🤚 Отмена')),
            width=2,
            
        ),
        state=Settings.temperature,
        parse_mode=ParseMode.HTML,
        getter=get_temperature,
    ),
)