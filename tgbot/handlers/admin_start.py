from aiogram import Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ChatActions
from tgbot.models.user import Users
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from tgbot.dialogs.admin_main import Main
from aiogram_dialog import DialogManager, StartMode

async def admin_start(m: Message, repo: Repo, dialog_manager: DialogManager):
    user: Users | None = await repo.get_user(m.from_user.id)
    if isinstance(user, Users):
        if user.full_name != m.from_user.full_name:
            # update full name if changed
            await repo.update_user_full_name(
                user_id=m.from_user.id,
                fullname=m.from_user.full_name)

    else:
        # register new user
        await repo.add_user(
            user_id=m.from_user.id,
            fullname=m.from_user.full_name,
            language_code=m.from_user.language_code,
        )

    # точка входа в основной диалог
    await dialog_manager.start(Main.main, mode=StartMode.RESET_STACK)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, 
        commands=["start"], 
        state="*", 
        is_admin=True
        )
