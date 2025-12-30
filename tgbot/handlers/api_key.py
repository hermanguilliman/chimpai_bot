from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from tgbot.services.repository.settings import SettingsService


async def input_chat_api_key_handler(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    new_api_key = message.text
    manager.dialog_data["api_key"] = new_api_key
    await settings_service.update_chat_api_key(user_id, new_api_key)
    await message.answer(
        "<b>✅ Новый API ключ успешно установлен!</b>",
        parse_mode=ParseMode.HTML,
    )
    await manager.back()
