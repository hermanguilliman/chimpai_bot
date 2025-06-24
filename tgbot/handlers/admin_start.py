from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.misc.states import MainMenu
from tgbot.models.models import Users
from tgbot.services.repository.users import UserService


async def admin_start_handler(
    m: Message, user_service: UserService, dialog_manager: DialogManager
):
    user: Users | None = await user_service.get_user(m.from_user.id)
    if not user:
        # регистрация нового пользователя
        await user_service.add_user(
            user_id=m.from_user.id,
        )

    await dialog_manager.start(MainMenu.select, mode=StartMode.RESET_STACK)
