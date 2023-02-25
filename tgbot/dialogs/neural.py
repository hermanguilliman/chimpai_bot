from aiogram_dialog import Dialog, Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from tgbot.handlers.neural_chat import neural_handler
from aiogram.types import ContentType, ParseMode
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Cancel
from tgbot.misc.states import Neural


neural_chat = Dialog(
    Window(
        # Нейрочат. Пока просто непрерывно читает текст от пользователя
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),
        Const("<b>🤖 Введите новый запрос:</b>"),
        Cancel(Const('↩️ Назад')),
        state=Neural.chat,
        parse_mode=ParseMode.HTML,
    ),
)