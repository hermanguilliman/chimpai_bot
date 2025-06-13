from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Cancel,
    Next,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.settings import on_base_url_selected
from tgbot.getters.settings import base_urls_getter
from tgbot.handlers.base_url import input_base_url_handler
from tgbot.misc.states import BaseUrl

# Диалог настроек
base_url_dialog = Dialog(
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
        state=BaseUrl.select,
        disable_web_page_preview=True,
    ),
    Window(
        Const(
            "<b>Отправьте URL адрес API сервера, который хотите использовать</b>"
        ),
        MessageInput(input_base_url_handler, content_types=[ContentType.TEXT]),
        Back(Const("👈 Назад")),
        state=BaseUrl.input_base_url,
        parse_mode=ParseMode.HTML,
    ),
)
