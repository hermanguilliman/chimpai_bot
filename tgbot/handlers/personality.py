from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from tgbot.misc.states import NewPersonality, PersonalitySettings
from tgbot.services.repository import Repo


async def new_personality_name(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    new_name = message.text
    is_exists = await repo.is_custom_personality_exists(
        user_id=user_id, name=new_name
    )

    if is_exists:
        await message.answer(
            f"⛔️ <b>{new_name}</b> уже существует! Придумайте другое имя! ⛔️",
            parse_mode=ParseMode.HTML,
        )
        return

    if len(new_name) > 20:
        await message.answer(
            "❗️ Ошибка! Максимальная длина имени 20 знаков!",
            parse_mode=ParseMode.HTML,
        )
        return

    manager.dialog_data["name"] = new_name
    await manager.switch_to(NewPersonality.text)


async def new_personality_text(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")

    name = manager.dialog_data.get("name")
    text = message.text

    await repo.add_custom_personality(user_id=user_id, name=name, text=text)
    await message.answer(
        f'👌 Личность "<b>{name}</b>" успешно добавлена!',
        parse_mode=ParseMode.HTML,
    )
    await manager.done()
    return


async def update_personality_text(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    """Обновляет описание личности"""
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    name = manager.dialog_data.get("custom_name")
    new_text = message.text
    await repo.update_personality_text(
        user_id=user_id, name=name, new_text=new_text
    )
    await message.answer(
        f'👌 Описание личности "<b>{name}</b>" успешно изменено!',
        parse_mode=ParseMode.HTML,
    )
    await manager.switch_to(PersonalitySettings.custom_person_select)


async def update_personality_name(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    """Обновляет имя личности"""
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    name = manager.dialog_data.get("custom_name")
    new_name = message.text
    is_exists = await repo.is_custom_personality_exists(
        user_id=user_id, name=new_name
    )
    if name == new_name:
        await message.answer(
            f"⚠️ <b>Хотите переименовать {name} на {new_name}? Это одно и то же имя!</b>",
            parse_mode=ParseMode.HTML,
        )
        return
    if is_exists:
        await message.answer(
            f"⛔️ <b>{new_name}</b> уже существует! Придумайте другое имя! ⛔️",
            parse_mode=ParseMode.HTML,
        )
        return

    if len(new_name) > 20:
        await message.answer(
            "❗️ Ошибка! Максимальная длина имени 20 знаков!",
            parse_mode=ParseMode.HTML,
        )
        return

    await repo.update_personality_name(
        user_id=user_id, name=name, new_name=new_name
    )
    await message.answer(
        f'👌 Личность "<b>{name}</b>" переименована на "<b>{new_name}</b>"!',
        parse_mode=ParseMode.HTML,
    )
    manager.dialog_data["custom_name"] = new_name
    await manager.switch_to(PersonalitySettings.custom_person_select)
