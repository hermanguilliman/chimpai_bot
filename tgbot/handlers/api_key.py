import re

from aiogram.types import Message, ParseMode
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from tgbot.services.repository import Repo


async def api_key_handler(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg().user.id
    repo: Repo = manager.data["repo"]
    dialog_data = manager.current_context().dialog_data
    new_api_key = message.text
    is_valid_key = bool(re.match("sk-[a-zA-Z0-9]{48}$", new_api_key))

    if not is_valid_key:
        await message.answer(
            "⛔️ <b>Ошибка API ключа!</b>\n Подсказка: Ключ должен выглядеть как sk-...",
            parse_mode=ParseMode.HTML,
        )
        await manager.done()
        return

    dialog_data["api_key"] = new_api_key
    await repo.update_api_key(user_id, new_api_key)
    await message.answer(
        "<b>✅ Новый API ключ успешно установлен!</b>", parse_mode=ParseMode.HTML
    )
    await manager.done()
