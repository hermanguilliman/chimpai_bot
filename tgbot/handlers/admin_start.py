from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.misc.states import Main
from tgbot.models.user import Users
from tgbot.services.repository import Repo


async def admin_start(m: Message, repo: Repo, dialog_manager: DialogManager):
    user: Users | None = await repo.get_user(m.from_user.id)
    if not user:
        # регистрация нового пользователя
        await repo.add_user(
            user_id=m.from_user.id,
        )

    await dialog_manager.start(Main.main, mode=StartMode.RESET_STACK)
