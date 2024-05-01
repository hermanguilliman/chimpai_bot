from aiogram.enums import ContentType, ParseMode
from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Select, Group
from aiogram_dialog.widgets.text import Const, Format
from tgbot.getters.settings import custom_person_getter
from tgbot.callbacks.settings import on_delete_custom_personality
from tgbot.handlers.personality import (
    new_personality_name, new_personality_text)
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
        Const("<b>♻️ Выберите личность, которую хотите удалить:</b>\n",
              when="persons"),
        Const("<b>🤷‍♀️ Вы еще не создали личности</b>", when=~F["persons"]),
        Group(
            Select(
                Format("{item}"),
                items="persons",
                item_id_getter=lambda x: x,
                id="select_person",
                on_click=on_delete_custom_personality,
                when="persons",
            ),
            width=2,
        ),
        Cancel(Const("🤚 Отмена")),
        state=Personality.reset,
        parse_mode="HTML",
        getter=custom_person_getter
    ),
)
