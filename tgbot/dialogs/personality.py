from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Const

from tgbot.callbacks.personality import reset_personality
from tgbot.handlers.personality import new_personality_name, new_personality_text
from tgbot.misc.states import Personality

person_settings_dialog = Dialog(
    Window(
        MessageInput(new_personality_name, content_types=[ContentType.TEXT]),
        Const("🎭 <b>Введите имя личности, но не более 20 знаков:</b>"),
        Row(
            Cancel(Const("🤚 Отмена")),
        ),
        state=Personality.name,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        MessageInput(new_personality_text, content_types=[ContentType.TEXT]),
        Const(
            "✒️ <b>Введите описание новой личности.</b>\
              \nОт полноты описания будет зависеть качество ответов:"
        ),
        Row(
            Back(Const("👈 Назад")),
            Cancel(Const("🤚 Отмена")),
        ),
        state=Personality.text,
        parse_mode="HTML",
    ),
    Window(
        Const("🤔 <b>Хотите сбросить личность?</b>\nЭто действие необратимо"),
        Row(
            Button(Const("♻️ Сбросить!"), id="reset_button", on_click=reset_personality),
            Cancel(Const("🤚 Отмена")),
        ),
        state=Personality.reset,
        parse_mode="HTML",
    ),
)
