from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from tgbot.services.repository import Repo


async def input_chat_api_key_handler(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    new_api_key = message.text
    manager.dialog_data["api_key"] = new_api_key
    await repo.update_chat_api_key(user_id, new_api_key)
    await message.answer(
        "<b>✅ Новый API ключ успешно установлен!</b>",
        parse_mode=ParseMode.HTML,
    )
    await manager.back()


async def input_summary_api_key_handler(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    new_api_key = message.text
    manager.dialog_data["api_key"] = new_api_key
    await repo.update_summary_api_key(user_id, new_api_key)
    await message.answer(
        "<b>✅ Новый API ключ успешно установлен!</b>",
        parse_mode=ParseMode.HTML,
    )
    await manager.back()
