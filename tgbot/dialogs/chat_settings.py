from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Row,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.settings import (
    on_decrease_temp,
    on_increase_temp,
    on_max_length_selected,
    on_new_model_selected,
    on_basic_personality_selected,
    on_custom_personality_selected,
    on_reset_temp,
    on_temperature_selected,
)
from tgbot.getters.base_data import get_base_data
from tgbot.getters.settings import (
    get_data_model_selector,
    basic_person_getter,
    custom_person_getter,
    get_temperature,
)
from tgbot.misc.states import ChatSettings, Personality

chat_settings_dialog = Dialog(
    Window(
        Const("<b>💬 Окно настроек чата: 💬</b>"),
        Group(
            SwitchTo(
                Format("🤖 Модель: {model}"),
                id="set_model",
                state=ChatSettings.model
            ),
            SwitchTo(
                Format("🔋 Максимум токенов: {max_length}"),
                id="set_max_length",
                state=ChatSettings.max_length,
            ),
            SwitchTo(
                Format("🌡️ Температура {temperature}"),
                id="set_temperature",
                state=ChatSettings.temperature,
            ),
            SwitchTo(
                Format("Личность: {personality}"),
                id="personality",
                state=ChatSettings.basic_personality,
            ),
            width=2,
        ),
        Cancel(Const("🤚 Отмена")),
        state=ChatSettings.select,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
    Window(
        # Список доступных моделей
        Const("<b>Выберите модель из списка:</b>"),
        Const("<b>Подсказка:</b> стандартное значение <b>gpt-3.5-turbo</b>"),
        Group(
            Select(
                Format("🤖 {item}"),
                items="models",
                item_id_getter=lambda x: x,
                id="select_max_new_model",
                on_click=on_new_model_selected,
            ),
            width=2,
        ),
        Cancel(Const("🤚 Отмена")),
        state=ChatSettings.model,
        parse_mode=ParseMode.HTML,
        getter=get_data_model_selector,
    ),
    Window(
        Const("<b>Укажите максимальную длину ответа</b>"),
        Const("\n<b>Подсказка:</b> стандартное значение <b>1000</b> токенов"),
        Group(
            Select(
                Format("🔋 {item}"),
                items=list(range(1000, 17000, 1000)),
                item_id_getter=lambda x: x,
                id="select_max_length",
                on_click=on_max_length_selected,
            ),
            width=5,
        ),
        Cancel(Const("🤚 Отмена")),
        state=ChatSettings.max_length,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        # окно выбора температуры
        # от 0.00 до 1.00 с двумя знаками после запятой
        Const("<b>🌡 Температура отвечает за оригинальность ответа</b>"),
        Group(
            Button(
                Format("✅ Установить значение: {temperature}"),
                id="new_temperature",
                when="temperature",
                on_click=on_temperature_selected,
            ),
            width=1,
        ),
        Group(
            Button(Const("🔻 0.1"), id="decrease", on_click=on_decrease_temp),
            Button(Const("0.1 🔺"), id="increase", on_click=on_increase_temp),
            width=2,
        ),
        Group(
            Button(Const("🌚 Как было"),
                   id="reset_temp",
                   on_click=on_reset_temp),
            Cancel(Const("🤚 Отмена")),
            width=2,
        ),
        state=ChatSettings.temperature,
        parse_mode=ParseMode.HTML,
        getter=get_temperature,
    ),
    Window(
        # Это окно с выбором личности бота.
        Const(
            "<b>Выберите одну из стандартных 🎭личностей бота.</b>"
        ),
        Group(
            Select(
                Format("{item}"),
                items="persons",
                item_id_getter=lambda x: x,
                id="select_person",
                on_click=on_basic_personality_selected,
            ),
            width=2,
        ),
        Row(
            SwitchTo(
                Const("🏗 Выбрать свою"),
                id="custom_personality",
                state=ChatSettings.custom_personality,
            ),
            Cancel(Const("🤚 Отмена")),
        ),
        state=ChatSettings.basic_personality,
        parse_mode="HTML",
        getter=basic_person_getter,
    ),
    Window(
        Const("<b>Список созданных вами личностей:</b>\n"),
        Group(
            Select(
                Format("{item}"),
                items="persons",
                item_id_getter=lambda x: x,
                id="select_person",
                on_click=on_custom_personality_selected,
                when="persons",
            ),
            width=2,
        ),
        Row(
            Start(
                Const("✏️ Создать"),
                id="custom_person",
                state=Personality.name,
            ),
            Start(
                Const("♻️ Удалить"),
                id="reset_person",
                state=Personality.reset,
            ),
        ),
        Cancel(Const("🤚 Отмена")),
        state=ChatSettings.custom_personality,
        parse_mode="HTML",
        getter=custom_person_getter,
    ),
)
