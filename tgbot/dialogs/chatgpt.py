from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.getters.base_data import get_base_data
from tgbot.handlers.neural_chat import neural_handler

from tgbot.handlers.voice_chatgpt import voice_to_chatgpt_handler
from tgbot.misc.states import ChatSettings, ChatGPT

chat_gpt_dialog = Dialog(
    Window(
        Const("<b>🤖 ChatGPT</b>\n"),

        Format(
            "🧠 Модель нейросети: <b>{model}</b>",
            when="model"
        ),

        Format(
            "🔋 Длина ответа: <b>{max_length}</b> токенов",
            when="max_length"
        ),

        Format(
            "🌡 Оригинальность ответа: <b>{temperature}</b>",
            when="temperature"
        ),

        Format(
            "🎭 Личность: <b>{personality}</b>",
            when="personality"
        ),

        Const("\n<b>Задай мне любой вопрос текстом или голосом 😎</b>"),

        # Инпут для голосового ввода запроса
        MessageInput(
            voice_to_chatgpt_handler,
            content_types=[ContentType.VOICE]),

        # Инпут для текстового ввода запроса
        MessageInput(
            neural_handler,
            content_types=[ContentType.TEXT]),

        Row(
            Cancel(
                Const("👈 Назад")),
            Start(
                Const("📝 Настройки чата"),
                id="settings",
                state=ChatSettings.select),
        ),
        state=ChatGPT.chat,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    )
)
