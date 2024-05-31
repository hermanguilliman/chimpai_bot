from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from tgbot.misc.states import NewPersonality
from tgbot.services.repository import Repo


async def new_personality_name(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    repo: Repo = manager.middleware_data.get("repo")
    new_name = message.text
    is_exists = await repo.is_custom_personality_exists(
        user_id=manager.bg().user.id, name=new_name)
    if is_exists:
        await message.answer(
            f"⛔️ <b>{new_name}</b> уже существует! Придумайте другое имя! ⛔️",
            parse_mode=ParseMode.HTML,
        )
        return

    if len(new_name) <= 20:
        manager.dialog_data["name"] = new_name
        await manager.switch_to(NewPersonality.text)
    else:
        await message.answer(
            "❗️ Ошибка! Максимальная длина имени 20 знаков!",
            parse_mode=ParseMode.HTML
        )
        return


async def new_personality_text(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg().user.id
    repo: Repo = manager.middleware_data.get("repo")

    name = manager.dialog_data.get("name")
    text = message.text

    await repo.add_custom_personality(user_id=user_id, name=name, text=text)
    await message.answer(
        f"👌 Личность \"<b>{name}</b>\" успешно добавлена!",
        parse_mode=ParseMode.HTML
    )
    await manager.done()
    return
