from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.history import clear_context, download_history
from tgbot.getters.chat import chat_data_getter
from tgbot.handlers.neural_chat import input_text_chat_handler
from tgbot.misc.states import NeuralChat, NeuralChatSettings

chat_dialog = Dialog(
    Window(
        Const("<b>🤖 Нейро чат</b>\n", when=~F["personality"]),
        Format(
            "<b>🤖 Нейро чат с {personality}</b>\n",
            when="personality",
        ),
        Format(
            "💬 Сообщений в памяти: {history_count}\n", when="history_count"
        ),
        Const("<b>Спросите что-нибудь... 🙋‍♂️</b>"),
        MessageInput(
            input_text_chat_handler, content_types=[ContentType.TEXT]
        ),
        Row(
            Button(
                Format("📩 Экспорт {export_format}"),
                id="download_history",
                on_click=download_history,
                when="history_count",
            ),
            Button(
                Const("♻️ Начать заново"),
                id="clear_context",
                on_click=clear_context,
                when="history_count",
            ),
        ),
        Row(
            Cancel(Const("👈 Назад")),
            Start(
                Const("⚙️ Настройки"),
                id="settings",
                state=NeuralChatSettings.select,
            ),
        ),
        state=NeuralChat.chat,
        parse_mode=ParseMode.HTML,
        getter=chat_data_getter,
    )
)
