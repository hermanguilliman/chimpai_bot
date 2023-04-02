from aiogram_dialog import Dialog, Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from tgbot.handlers.neural_chat import neural_handler
from aiogram.types import ContentType, ParseMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, Start, Row
from tgbot.misc.states import Neural, Settings
from tgbot.getters.base_data import get_base_data


neural_chat = Dialog(
    Window(
        # Нейрочат. Пока просто непрерывно читает текст от пользователя
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),
        Const('<b>Введите запрос:</b>'),
        Format("<b>[ Личность: {personality_name} ]</b>", when='personality_name'),
        Row(
            Cancel(Const('👈 Назад')),
            Start(Const("📝 Настройки"), id='settings', state=Settings.select),
        ),
        state=Neural.chat,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
)