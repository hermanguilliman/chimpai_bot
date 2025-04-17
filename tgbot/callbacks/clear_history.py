from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.services.repository import Repo


async def clear_context(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    await repo.clear_conversation_history(user_id)
    await callback.answer(
        "🗑 История беседы очищена!",
    )
