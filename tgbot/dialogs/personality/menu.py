from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Group,
    Row,
    ScrollingGroup,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.settings import (
    on_basic_personality_selected,
    on_custom_personality_activate,
    on_custom_personality_delete_confirm,
    on_custom_personality_selected,
)
from tgbot.getters.settings import (
    basic_person_getter,
    custom_person_list_getter,
    custom_personality_getter,
)
from tgbot.handlers.personality import (
    update_personality_name,
    update_personality_text,
)
from tgbot.misc.states import NewPersonality, PersonalitySettings

personality_menu_dialog = Dialog(
    # Список предустановленных личностей
    Window(
        Const("<b>🎭 Выберите одну из предустановленных личностей бота.</b>"),
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
    # Список кастомных личностей
    Window(
        Const(
            "<b>Список созданных вами личностей:</b>\n",
            when="persons",
        ),
        Const(
            "<b>Вы еще не добавили ни одну личность 😩</b>",
            when=~F["persons"],
        ),
        ScrollingGroup(
            Select(
                Format("{item}"),
                items="persons",
                item_id_getter=lambda x: x,
                id="select_person",
                on_click=on_custom_personality_selected,
                when="persons",
            ),
            id="scrolling_persons",
            width=2,
            height=8,
            when="persons",
        ),
        Row(
            SwitchTo(
                Const("👈 Назад"),
                id="back",
                state=PersonalitySettings.basic_list,
            ),
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
    # Просмотр карточки личности
    Window(
        Format(
            "<b>Перед вами карточка личности:\n{custom_name}</b>\n",
            when="custom_name",
        ),
        Format("<b>Описание личности:</b>\n{custom_desc}", when="custom_desc"),
        Row(
            Button(
                Const("✅ Использовать"),
                id="activate_custom_personality",
                on_click=on_custom_personality_activate,
            ),
            SwitchTo(
                Const("🗑 Удалить"),
                id="delete_custom_personality",
                state=PersonalitySettings.custom_person_delete_confirm,
            ),
        ),
        Row(
            SwitchTo(
                Const("🪪 Изменить имя"),
                id="edit_custom_personality_name",
                state=PersonalitySettings.custom_person_edit_name,
            ),
            SwitchTo(
                Const("📖 Изменить описание"),
                id="edit_custom_personality_desc",
                state=PersonalitySettings.custom_person_edit_description,
            ),
        ),
        Back(Const("👈 Назад")),
        getter=custom_personality_getter,
        state=PersonalitySettings.custom_person_select,
        parse_mode=ParseMode.HTML,
    ),
    # Редактирование имени кастомной личности
    Window(
        Format("<b>Вы редактируете: {custom_name}</b>\n", when="custom_name"),
        Const("\n🪪 <b>Отправьте новое имя личности</b>"),
        MessageInput(
            update_personality_name,
            content_types=[ContentType.TEXT],
        ),
        SwitchTo(
            Const("👈 Назад"),
            id="back_to_select",
            state=PersonalitySettings.custom_person_select,
        ),
        state=PersonalitySettings.custom_person_edit_name,
        getter=custom_personality_getter,
        parse_mode=ParseMode.HTML,
    ),
    # Редактирование описания кастомной личности
    Window(
        Format("<b>Вы редактируете: {custom_name}</b>\n", when="custom_name"),
        Const("\n📖 <b>Отправьте новое описание личности</b>"),
        MessageInput(
            update_personality_text,
            content_types=[ContentType.TEXT],
        ),
        SwitchTo(
            Const("👈 Назад"),
            id="back_to_select",
            state=PersonalitySettings.custom_person_select,
        ),
        state=PersonalitySettings.custom_person_edit_description,
        getter=custom_personality_getter,
        parse_mode=ParseMode.HTML,
    ),
    # Удаление кастомной личности
    Window(
        Const("<b>Вы уверены?</b>\n"),
        Format(
            "<b>Сейчас личность {custom_name} будет удалена!</b>",
            when="custom_name",
        ),
        Button(
            Const("♻️ Да, удалить!"),
            id="delete_confirm",
            on_click=on_custom_personality_delete_confirm,
        ),
        Back(Const("🙅‍♂️ Я передумал")),
        state=PersonalitySettings.custom_person_delete_confirm,
        getter=custom_personality_getter,
        parse_mode=ParseMode.HTML,
    ),
)
