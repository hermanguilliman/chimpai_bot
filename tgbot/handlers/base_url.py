from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from tgbot.services.repository import Repo


async def input_base_url_handler(
    message: Message, message_input: MessageInput, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    new_base_url = message.text
    if (
        not (
            new_base_url.startswith("http://")
            or new_base_url.startswith("https://")
        )
        or " " in new_base_url
    ):
        await message.answer(
            "<b>❌ Ошибка: Введите корректный HTTP или HTTPS адрес без пробелов!</b>",
            parse_mode=ParseMode.HTML,
        )
        return
    await repo.set_chat_custom_base_url_to_user(user_id, new_base_url)
    await message.answer(
        "<b>✅ Адрес API сервера установлен!</b>",
        parse_mode=ParseMode.HTML,
    )
    await manager.done()
