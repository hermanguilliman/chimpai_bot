from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput


async def search_engines(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    tags = message.text
    manager.dialog_data["search_query"] = tags
