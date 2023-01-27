from aiogram import Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from tgbot.misc.states import Main
from tgbot.models.user import Users
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo

async def admin_start(m: Message, repo: Repo):
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
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_settings = KeyboardButton(text='/settings')
    markup.add(btn_settings)
    await m.answer("\nAdmin permissions granted!\n\nWelcome to OpenAI bot!", reply_markup=markup)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
