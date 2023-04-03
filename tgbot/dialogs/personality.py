from aiogram_dialog import Dialog, Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from tgbot.handlers.new_personality import new_person_name, new_person_text
from aiogram.types import ContentType, ParseMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, Start, Row, Back, Next
from tgbot.misc.states import Personality
from tgbot.getters.base_data import get_base_data


person = Dialog(
    Window(
        MessageInput(new_person_name, content_types=[ContentType.TEXT]),

        Const('🎭 <b>Введите имя личности:</b>'),
        Row(
            Cancel(Const('🤚 Отмена')),
        ),
        state=Personality.name,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        MessageInput(new_person_text, content_types=[ContentType.TEXT]),
        Const('✒️ <b>Введите описание новой личности.</b>\
              \nОн полноты описания будет зависеть качество ответов:'),
        Row(
            Back(Const('👈 Назад')),
            Cancel(Const('🤚 Отмена')),
        ),
        state=Personality.text,
        parse_mode='HTML'
    ),
)