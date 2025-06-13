from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.settings import on_base_url_selected
from tgbot.getters.settings import base_urls_getter
from tgbot.misc.states import BaseUrl

# Диалог настроек
base_url_dialog = Dialog(
    Window(
        Const("Выбрите сервер API, который будет использоваться для запросов"),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),
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
        Cancel(Const("👈 Назад")),
        getter=base_urls_getter,
        parse_mode=ParseMode.HTML,
        state=BaseUrl.select,
    )
)
