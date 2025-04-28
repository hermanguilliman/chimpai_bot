from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.history import clear_context, download_history
from tgbot.getters.base_data import get_base_data
from tgbot.handlers.neural_chat import neural_handler
from tgbot.handlers.voice_chatgpt import voice_to_chatgpt_handler
from tgbot.misc.states import ChatGPT, ChatSettings

chat_dialog = Dialog(
    Window(
        Const("<b>🤖 Чат</b>\n"),
        Format("🧠 Модель нейросети: <b>{model}</b>", when="model"),
        Format(
            "🔋 Длина ответа: <b>{max_length}</b> токенов", when="max_length"
        ),
        Format(
            "🌡 Оригинальность ответа: <b>{temperature}</b>", when="temperature"
        ),
        Format("🎭 Личность: <b>{personality}</b>", when="personality"),
        Format("💬 Сообщений в памяти: {history_count}", when="history_count"),
        Const("\n<b>Задай мне любой вопрос текстом или голосом 😎</b>"),
        # Инпут для голосового ввода запроса
        MessageInput(
            voice_to_chatgpt_handler, content_types=[ContentType.VOICE]
        ),
        # Инпут для текстового ввода запроса
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
