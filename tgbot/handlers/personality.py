import re
from aiogram.types import Message, ParseMode
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from tgbot.services.repository import Repo
from tgbot.misc.states import Personality


async def new_personality_name(message: Message, message_input: MessageInput,
                       manager: DialogManager):
    dialog_data = manager.current_context().dialog_data
    new_name = message.text
    if len(new_name) <= 20:
        dialog_data["name"] = new_name
        await manager.switch_to(Personality.text)
    else:
        await message.answer(
            f'❗️ Ошибка! Максимальная длина имени 20 знаков!', parse_mode=ParseMode.HTML)
        return


async def new_personality_text(message: Message, message_input: MessageInput,
                       manager: DialogManager):

    user_id = manager.bg().user.id
    repo: Repo = manager.data['repo']
    dialog_data = manager.current_context().dialog_data
    personality: Personality = await repo.get_personality(user_id=user_id)

    name = dialog_data.get('name')
    text = message.text

    if not personality:
        await repo.add_new_personality(user_id=user_id, name=name, text=text)
    else:
        await repo.update_personality(
            user_id=user_id, 
            name=name,
            text=text,
            )
    
    await message.answer(f'Личность <b>{name}</b> - сохранена', parse_mode=ParseMode.HTML)
    await manager.done()
    return


    