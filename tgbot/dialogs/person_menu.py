from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Back,
    Cancel,
    Group,
    Row,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.settings import (
    on_custom_personality_activate,
    on_basic_personality_selected,
    on_custom_personality_delete,
    on_custom_personality_selected,
)
from tgbot.getters.settings import (
    custom_personality_getter,
    basic_person_getter,
    custom_person_list_getter,
)
from tgbot.misc.states import NewPersonality, PersonalitySettings


personality_menu_dialog = Dialog(
    Window(
        Const("<b>Выберите одну из стандартных 🎭личностей бота.</b>"),
        Group(
            Select(
                Format("{item}"),
                items="persons",
                item_id_getter=lambda x: x,
                id="select_person",
                on_click=on_basic_personality_selected,
            ),
            width=2,
        ),
        Row(
            Cancel(Const("👈 Назад")),
            SwitchTo(
                Const("📝 Свой список"),
                id="custom_personality",
                state=PersonalitySettings.custom_list,
            ),
        ),
        state=PersonalitySettings.basic_list,
        parse_mode=ParseMode.HTML,
        getter=basic_person_getter,
    ),
    Window(
        Const("<b>Список созданных вами личностей:</b>\n", when="persons",),
        Const(
            "<b>Вы еще не создали ни одну личность</b>",
            when=~F["persons"],
        ),
        Group(
            Select(
                Format("{item}"),
                items="persons",
                item_id_getter=lambda x: x,
                id="select_person",
                on_click=on_custom_personality_selected,
                when="persons",
            ),
            width=2,
        ),
        Row(
            Cancel(Const("👈 Назад")),
            Start(
                Const("📋 Добавить"),
                id="custom_person",
                state=NewPersonality.name,
            ),
        ),
        state=PersonalitySettings.custom_list,
        parse_mode=ParseMode.HTML,
        getter=custom_person_list_getter,
    ),
    Window(
        Format("<b>Имя личности:\n{custom_name}</b>\n", when="custom_name"),
        Format("<b>Описание личности:</b>\n{custom_desc}", when="custom_desc"),
        Row(
            Button(
                Const("✅ Активировать"),
                id="activate_custom_personality",
                on_click=on_custom_personality_activate,
            ),
            Button(
                Const("🗑 Удалить"),
                id="delete_custom_personality",
                on_click=on_custom_personality_delete,
            ),
        ),
        Back(Const("👈 Назад")),
        getter=custom_personality_getter,
        state=PersonalitySettings.custom_person_select,
        parse_mode=ParseMode.HTML,
    ),
)
