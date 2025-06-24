from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Cancel,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const

from tgbot.handlers.api_key import input_summary_api_key_handler
from tgbot.misc.states import (
    SetupSummaryService,
)

# Управление сервисом пересказчика
summary_service_dialog = Dialog(
    Window(
        Const("<b>Меню управления сервисом пересказчика</b>"),
        SwitchTo(
            Const("🔑 Установить API ключ"),
            id="set_api_key",
            state=SetupSummaryService.api_key,
        ),
        Cancel(Const("👈 Назад")),
        parse_mode=ParseMode.HTML,
        state=SetupSummaryService.select,
    ),
    Window(
        MessageInput(
            input_summary_api_key_handler, content_types=[ContentType.TEXT]
        ),
        Const("<b>Укажите новый API ключ для сервиса Пересказчик:</b>"),
        Const(
            "<b>Подсказка:</b> ключ можно получить на странице https://300.ya.ru/"
        ),
        SwitchTo(
            Const("👈 Назад"), id="back", state=SetupSummaryService.select
        ),
        state=SetupSummaryService.api_key,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    ),
)
