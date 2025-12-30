from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from tgbot.getters.system import system_data_getter
from tgbot.misc.states import (
    MainMenu,
    NeuralChat,
    SystemSettings,
)

main_dialog = Dialog(
    Window(
        Const("<b>Привет, я ChimpAI! 🐵</b>\n"),
        Row(
            Start(
                Const("🤖 Нейро чат"),
                id="neural_chat",
                state=NeuralChat.chat,
                when="chat_api_key",
            ),
        ),
        Start(
            Const("🔩 Системные настройки"),
            id="system_settings",
            state=SystemSettings.select,
        ),
        state=MainMenu.select,
        getter=system_data_getter,
        parse_mode=ParseMode.HTML,
    ),
)
