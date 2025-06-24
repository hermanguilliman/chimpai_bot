from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Start,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.getters.system import system_data_getter
from tgbot.misc.states import (
    SetupSummaryService,
    SetupСhatService,
    SystemSettings,
)

system_settings_dialog = Dialog(
    Window(
        Const("<b>🛠 Системное меню 🛠</b>"),
        Start(
            Format("✅ Чат активен", when="chat_api_key"),
            id="set_chat_api_key",
            state=SetupСhatService.select,
        ),
        Start(
            Const("⛔️ Чат неактивен", when=~F["chat_api_key"]),
            id="set_chat_api_key",
            state=SetupСhatService.select,
        ),
        Start(
            Format("✅ Пересказчик активен", when="summary_api_key"),
            id="set_summary_api_key",
            state=SetupSummaryService.select,
        ),
        Start(
            Const("⛔️ Пересказчик неактивен", when=~F["summary_api_key"]),
            id="set_summary_api_key",
            state=SetupSummaryService.select,
        ),
        Cancel(Const("👈 Назад")),
        state=SystemSettings.select,
        parse_mode=ParseMode.HTML,
        getter=system_data_getter,
    ),
)
