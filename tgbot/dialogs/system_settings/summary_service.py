from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const

from tgbot.callbacks.summary import on_delete_summary_api_key
from tgbot.getters.system import system_data_getter
from tgbot.handlers.api_key import input_summary_api_key_handler
from tgbot.misc.states import (
    SetupSummaryService,
)

# Управление сервисом пересказчика
summary_service_dialog = Dialog(
    Window(
        Const("<b>👷‍♂️ Меню управления сервисом Пересказчик\n</b>"),
        Const("<b>💡 Удаление API ключа отключает сервис</b>"),
        SwitchTo(
            Const("🔑 Установить API ключ"),
            when=~F["summary_api_key"],
            id="set_api_key",
            state=SetupSummaryService.api_key,
        ),
        SwitchTo(
            Const("🔑 Изменить API ключ"),
            when=F["summary_api_key"],
            id="set_api_key",
            state=SetupSummaryService.api_key,
        ),
        Button(
            Const("♻️ Удалить API ключ"),
            when=F["summary_api_key"],
            id="delete_api_key",
            on_click=on_delete_summary_api_key,
        ),
        Cancel(Const("👈 Назад")),
        getter=system_data_getter,
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
