from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.misc.states import Main
from tgbot.models.user import Users
from tgbot.services.repository import Repo


async def admin_start(m: Message, repo: Repo, dialog_manager: DialogManager):
    user: Users | None = await repo.get_user(m.from_user.id)
    if isinstance(user, Users):
        if user.full_name != m.from_user.full_name:
            # update full name if changed
            await repo.update_full_name(
                user_id=m.from_user.id, fullname=m.from_user.full_name
            )

    else:
        # register new user
        await repo.add_user(
            user_id=m.from_user.id,
            fullname=m.from_user.full_name,
            language_code=m.from_user.language_code,
        )

    await dialog_manager.start(Main.main, mode=StartMode.RESET_STACK)
