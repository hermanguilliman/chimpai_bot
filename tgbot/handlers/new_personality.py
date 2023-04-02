import re
from aiogram.types import Message, ParseMode
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from tgbot.services.repository import Repo
from tgbot.misc.states import Personality


async def new_person_name(message: Message, message_input: MessageInput,
                       manager: DialogManager):
    dialog_data = manager.current_context().dialog_data
    new_name = message.text
    if len(new_name) <= 20:
        dialog_data["personality_name"] = new_name
        await manager.switch_to(Personality.text)
    else:
        await message.answer(
            f'❗️ Ошибка! Максимальная длина имени 20 знаков!', parse_mode=ParseMode.HTML)
        return


async def new_person_text(message: Message, message_input: MessageInput,
                       manager: DialogManager):

    user_id = manager.bg().user.id
    repo: Repo = manager.data['repo']
    dialog_data = manager.current_context().dialog_data
    personality_name = dialog_data.get('personality_name')
    personality_text = message.text
    
    await repo.update_personality(
        user_id=user_id, 
        personality_name=personality_name,
        personality_text=personality_text,
        )
    
    await message.answer(f'Личность <b>{personality_name}</b> - сохранена', parse_mode=ParseMode.HTML)
    await manager.done()
    return


    