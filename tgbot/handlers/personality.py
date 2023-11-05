from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from tgbot.misc.states import Personality
from tgbot.services.repository import Repo


async def new_personality_name(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    new_name = message.text
    if len(new_name) <= 20:
        manager.dialog_data["name"] = new_name
        await manager.switch_to(Personality.text)
    else:
        await message.answer(
            "❗️ Ошибка! Максимальная длина имени 20 знаков!", parse_mode=ParseMode.HTML
        )
        return


async def new_personality_text(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg().user.id
    repo: Repo = manager.middleware_data.get("repo")
    personality: Personality = await repo.get_personality(user_id=user_id)

    name = manager.dialog_data.get("name")
    text = message.text

    if not personality:
        await repo.add_new_personality(user_id=user_id, name=name, text=text)
    else:
        await repo.update_personality(
            user_id=user_id,
            name=name,
            text=text,
        )

    await message.answer(
        f"Личность <b>{name}</b> - сохранена", parse_mode=ParseMode.HTML
    )
    await manager.done()
    return
