from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.getters.base_data import get_base_data
from tgbot.handlers.neural_chat import neural_handler
from tgbot.handlers.voice_transcribe import voice_handler
from tgbot.handlers.images import image_creator_handler
from tgbot.misc.states import Neural, Settings

neural_chat = Dialog(
    Window(
        # Нейрочат. Пока просто непрерывно читает текст от пользователя
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),
        Format("<b>Личность: {personality}\n</b>", when="personality"),
        Const("<b>Задай мне любой вопрос...</b>"),
        Row(
            Cancel(Const("👈 Назад")),
            Start(Const("📝 Настройки"), id="settings", state=Settings.select),
        ),
        state=Neural.chat,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
    Window(
        MessageInput(voice_handler, content_types=[ContentType.VOICE]),
        Const("<b>📢 Запишите или перешлите войс</b>"),
        Cancel(Const("👈 Назад")),
        state=Neural.transcribe,
        parse_mode=ParseMode.HTML,
    ),

    Window(
        MessageInput(image_creator_handler, content_types=[ContentType.TEXT]),
        Const("<b>🖌 Напишите описание несуществующего изображения...</b>"),
        Cancel(Const("👈 Назад")),
        state=Neural.image_create,
        parse_mode=ParseMode.HTML,
    ),
)
