from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.misc.states import Main
from tgbot.services.repository import Repo


async def reset_personality(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg().user.id
    await repo.delete_personality(user_id)
    await callback.answer("Личность удалена!")
    await manager.done()
    await manager.start(Main.main)
