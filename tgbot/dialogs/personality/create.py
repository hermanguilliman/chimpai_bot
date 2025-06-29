from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row
from aiogram_dialog.widgets.text import Const

from tgbot.handlers.personality import (
    input_new_personality_name_handler,
    input_new_personality_text_handler,
)
from tgbot.misc.states import NewPersonality

new_person_dialog = Dialog(
    Window(
        MessageInput(
            input_new_personality_name_handler,
            content_types=[ContentType.TEXT],
        ),
        Const("🎭 <b>Введите имя личности, но не более 20 знаков:</b>"),
        Row(
            Cancel(Const("🤚 Отмена")),
        ),
        state=NewPersonality.name,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        MessageInput(
            input_new_personality_text_handler,
            content_types=[ContentType.TEXT],
        ),
        Const(
            "✒️ <b>Введите описание новой личности.</b>\
            \nОт полноты описания будет зависеть качество ответов:"
        ),
        Row(
            Back(Const("👈 Назад")),
            Cancel(Const("🤚 Отмена")),
        ),
        state=NewPersonality.text,
        parse_mode=ParseMode.HTML,
    ),
)
