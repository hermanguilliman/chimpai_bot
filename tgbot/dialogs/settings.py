from tgbot.misc.states import Settings, Personality
from aiogram.types import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Cancel, Select, SwitchTo, Group, Start
from aiogram_dialog.widgets.input import MessageInput
from tgbot.handlers.api_key import api_key_handler
from tgbot.getters.settings import get_data_model_selector, get_temperature, get_person_selector
from tgbot.getters.base_data import get_base_data
from tgbot.handlers.api_key import api_key_handler
from tgbot.callbacks.settings import (
    on_decrease_temp,
    on_increase_temp,
    on_max_length_selected,
    on_new_model_selected,
    on_new_personality_selected,
    on_reset_temp,
    on_temperature_selected,
)


# Диалог настроек
settings_dialog = Dialog(
    Window(
        # Окно выбора настроек
        Const('<b>Выберите параметр, который хотели бы изменить:</b>'),
        Group(
        SwitchTo(Format('🔐 API ключ: {api_key}'), id='set_api_key', state=Settings.api_key),
        SwitchTo(Format('🤖 Модель: {model}'), id='set_model', state=Settings.model),
        SwitchTo(Format('🔋 Длина ответа: {max_length} токенов'), id='set_max_length', state=Settings.max_length),
        SwitchTo(Format('🌡️ Температура {temperature}'), id='set_temperature', state=Settings.temperature),
        width=1),
        SwitchTo(Format('Личность: {personality_name}'), id='personality', state=Settings.personality),
        Cancel(Const('🤚 Отмена')),
        state=Settings.select,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),

    Window(
        # Установка нового ключа апи
        MessageInput(api_key_handler, content_types=[ContentType.TEXT]),
        Const("<b>Укажите новый API ключ:</b>"),
        Const("Подсказка: Ключ OpenAI API выглядит как <b>sk-...</b>"),
        Cancel(Const('🤚 Отмена')),
        state=Settings.api_key,
        parse_mode=ParseMode.HTML,
    ),

    Window(
        # Список доступных моделей
        Const("<b>Выберите модель из списка:</b>"),
        Const("Подсказка: стандартное значение <b>gpt-3.5-turbo</b>"),
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
    
    Window(
    # Это окно с выбором характера бота.
    # Здесь будет выбор между готовыми характерами, а так же кнопка добавления своего
        Const('<b>Перед Вами список возможных 🎭личностей бота.</b>'
              '\nУстановка личности позволяет боту менять образ и стиль общения.'
              '\n\nВыберите любую из доступных личностей, либо добавьте описание вручную:'),
        Group(
            Select(
                Format("{item}"),
                items='persons',
                item_id_getter=lambda x: x,
                id='select_person',
                on_click=on_new_personality_selected,
            ),
            width=2,
        ),
        Group(
            Start(Const("✏️ Создать личность"), id='custom_person', state=Personality.name),
            Cancel(Const('🤚 Отмена')),
            width=1,
        )
        ,
        state=Settings.personality,
        parse_mode='HTML',
        getter=get_person_selector,
    ),
)