from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    ScrollingGroup,
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
    on_reset_temp,
    on_temperature_selected,
)
from tgbot.getters.base_data import get_base_data
from tgbot.getters.settings import (
    get_data_model_selector,
    get_temperature,
)
from tgbot.misc.states import ChatSettings, PersonalitySettings

chat_settings_dialog = Dialog(
    Window(
        Const("<b>💬 Текущие настройки чата: 💬</b>\n"),
        Format("🧠 Модель: <b>{model}</b>", when="model"),
        Format("🔋 Токены: <b>{max_length}</b>", when="max_length"),
        Format("🌡 Температура: <b>{temperature}</b>", when="temperature"),
        Format("🤡 Личность: <b>{personality}</b>", when="personality"),
        Format("💬 Контекст: {history_count}", when="history_count"),
        Const("<b>\nВыберите пункт который хотели бы изменить 👇🏻</b>\n"),
        Group(
            SwitchTo(
                Format("🧠 Модель"),
                id="set_model",
                state=ChatSettings.model,
            ),
            SwitchTo(
                Format("🔋 Токены"),
                id="set_max_length",
                state=ChatSettings.max_length,
            ),
            SwitchTo(
                Format("🌡️ Температура"),
                id="set_temperature",
                state=ChatSettings.temperature,
            ),
            Start(
                Format("🤡 Личность"),
                id="personality",
                state=PersonalitySettings.basic_list,
            ),
            width=2,
        ),
        Cancel(Const("👈 Назад")),
        state=ChatSettings.select,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
    Window(
        Const("<b>Выберите модель из списка:</b>"),
        Const("<b>Подсказка:</b> стандартное значение <b>gpt-4o-mini</b>"),
        ScrollingGroup(
            Select(
                Format(
                    "🧠 {item[1]}"
                ),  # Показываем только сокращённое имя модели
                items="models",
                item_id_getter=lambda x: x[
                    0
                ],  # Полное название модели для идентификатора
                id="select_max_new_model",
                on_click=on_new_model_selected,
            ),
            width=1,
            height=20,
            id="scrolling_models",
            when="models",
        ),
        SwitchTo(Const("👈 Назад"), id="back", state=ChatSettings.select),
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
        SwitchTo(Const("👈 Назад"), id="back", state=ChatSettings.select),
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
            SwitchTo(Const("👈 Назад"), id="back", state=ChatSettings.select),
            Button(
                Const("🌚 Стандартные"),
                id="reset_temp",
                on_click=on_reset_temp,
            ),
            width=2,
        ),
        state=ChatSettings.temperature,
        parse_mode=ParseMode.HTML,
        getter=get_temperature,
    ),
)
