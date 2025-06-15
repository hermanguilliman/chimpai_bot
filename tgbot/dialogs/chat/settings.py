from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
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
    on_clear_search_query,
    on_decrease_temp,
    on_increase_temp,
    on_max_length_selected,
    on_new_model_selected,
    on_reset_temp,
    on_temperature_selected,
    toggle_export_format,
)
from tgbot.getters.base_data import get_base_data
from tgbot.getters.settings import (
    models_selector_getter,
    temperature_getter,
)
from tgbot.handlers.engines import search_engines_handler
from tgbot.misc.states import ChatSettings, PersonalitySettings

chat_settings_dialog = Dialog(
    Window(
        Const("<b>💬 Текущие настройки чата: 💬</b>\n"),
        Format("🧠 Модель: <b>{model}</b>", when="model"),
        Format("🗺 API сервер: <b>{base_url}</b>", when="base_url"),
        Format("🔋 Токены: <b>{max_length}</b>", when="max_length"),
        Format("🌡 Температура: <b>{temperature}</b>", when="temperature"),
        Format("🤡 Личность: <b>{personality}</b>", when="personality"),
        Format(
            "💬 Сообщений в памяти: <b>{history_count}</b>",
            when="history_count",
        ),
        Format(
            "📩 Формат сохранения истории: <b>{export_format}</b>",
            when="export_format",
        ),
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
            Button(
                Const("🔄 Сменить формат экспорта истории"),
                id="toggle_format",
                on_click=toggle_export_format,
                when="history_count",
            ),
            width=2,
        ),
        Cancel(Const("👈 Назад")),
        state=ChatSettings.select,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
        disable_web_page_preview=True,
    ),
    Window(
        # Если не задан поисковый запрос и есть модели
        Const(
            "<b>📖 Перед вами все имеющиеся модели</b>\n",
            when=~F["dialog_data"]["search_query"] & F["models"],
        ),
        # Если задан поисковый запрос и есть модели
        Format(
            "<b>🔎 Перед вами все модели по запросу: {dialog_data[search_query]}</b>\n",
            when=F["dialog_data"]["search_query"] & F["models"],
        ),
        # Если есть список моделей, но нет поискового запроса
        Const(
            "<b>👇 Выберите модель, либо используйте поисковый запрос для фильтрации</b>",
            when=F["models"] & ~F["dialog_data"]["search_query"],
        ),
        # Если есть список результатов по поисковому запросу
        Const(
            "<b>👇 Выберите модель, либо используйте другой поисковый запрос</b>",
            when=F["models"] & F["dialog_data"]["search_query"],
        ),
        # Если есть поисковый запрос, но нет результатов
        Format(
            "<b>🔎 По запросу '{dialog_data[search_query]}' ничего не найдено</b>",
            when=~F["models"] & F["dialog_data"]["search_query"],
        ),
        # Если нет результатов и нет поискового запроса
        Const(
            "<b>🤷 В данный момент нет моделей</b>",
            when=~F["models"] & ~F["dialog_data"]["search_query"],
        ),
        MessageInput(search_engines_handler, content_types=[ContentType.TEXT]),
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
        SwitchTo(
            Const("👈 Назад"),
            id="back",
            state=ChatSettings.select,
            on_click=on_clear_search_query,
        ),
        state=ChatSettings.model,
        parse_mode=ParseMode.HTML,
        getter=models_selector_getter,
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
        getter=temperature_getter,
    ),
)
