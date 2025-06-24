from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Cancel,
    Next,
    ScrollingGroup,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.settings import on_base_url_selected
from tgbot.getters.settings import base_urls_getter
from tgbot.getters.system import system_data_getter
from tgbot.handlers.api_key import input_chat_api_key_handler
from tgbot.handlers.base_url import input_base_url_handler
from tgbot.misc.states import (
    SetupСhatService,
)

# Управление сервисом чата
chat_service_dialog = Dialog(
    Window(
        Const("<b>Меню управления сервисом чата</b>"),
        SwitchTo(
            Const("🔑 Установить API ключ"),
            when=~F["chat_api_key"],
            id="set_api_key",
            state=SetupСhatService.api_key,
        ),
        SwitchTo(
            Const("🔑 Изменить API ключ"),
            id="set_api_key",
            state=SetupСhatService.api_key,
            when=F["chat_api_key"],
        ),
        SwitchTo(
            Const("🗺 Сменить адрес сервера"),
            id="set_base_url",
            state=SetupСhatService.base_url,
        ),
        Cancel(Const("👈 Назад")),
        getter=system_data_getter,
        parse_mode=ParseMode.HTML,
        state=SetupСhatService.select,
    ),
    Window(
        MessageInput(
            input_chat_api_key_handler, content_types=[ContentType.TEXT]
        ),
        Const("<b>Укажите новый API ключ:</b>"),
        Const("<b>Подсказка:</b> Ключ OpenAI API выглядит как <b>sk-...</b>"),
        SwitchTo(Const("👈 Назад"), id="back", state=SetupСhatService.select),
        state=SetupСhatService.api_key,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        Format(
            "<b>Вы используете сервер {current_base_url}</b>\n",
            when="current_base_url",
        ),
        Const("<b>Выберите  API сервер из списка или используйте свой</b>"),
        ScrollingGroup(
            Select(
                Format("🗺 {item[1]}"),
                items="base_urls",
                item_id_getter=lambda x: x[1],
                id="base_url",
                on_click=on_base_url_selected,
                when="base_urls",
            ),
            id="scrolling_urls",
            width=1,
            height=8,
            when="base_urls",
        ),
        Next(Const("✏️ Использовать свой")),
        Cancel(Const("👈 Назад")),
        getter=base_urls_getter,
        parse_mode=ParseMode.HTML,
        state=SetupСhatService.base_url,
        disable_web_page_preview=True,
    ),
    Window(
        Const(
            "<b>Отправьте URL адрес API сервера, который хотите использовать</b>"
        ),
        MessageInput(input_base_url_handler, content_types=[ContentType.TEXT]),
        Back(Const("👈 Назад")),
        state=SetupСhatService.input_base_url,
        parse_mode=ParseMode.HTML,
    ),
)
