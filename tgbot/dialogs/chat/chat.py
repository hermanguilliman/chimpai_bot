from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.history import clear_context, download_history
from tgbot.getters.base_data import get_base_data
from tgbot.handlers.neural_chat import neural_handler
from tgbot.handlers.voice import voice_handler
from tgbot.misc.states import ChatGPT, ChatSettings

chat_dialog = Dialog(
    Window(
        Const("<b>🤖 Нейро чат</b>\n"),
        Format("🧠 Модель: <b>{model}</b>", when="model"),
        Format("🔋 Токены: <b>{max_length}</b>", when="max_length"),
        Format("🌡 Температура: <b>{temperature}</b>", when="temperature"),
        Format("🎭 Личность: <b>{personality}</b>", when="personality"),
        Format("💬 Контекст: {history_count}", when="history_count"),
        Const("\n<b>Задай мне любой вопрос текстом или голосом 😎</b>"),
        MessageInput(voice_handler, content_types=[ContentType.VOICE]),
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),
        Row(
            Button(
                Const("📩 Экспорт в .md"),
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
                Const("⚙️ Настройки чата"),
                id="settings",
                state=ChatSettings.select,
            ),
        ),
        state=ChatGPT.chat,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    )
)
