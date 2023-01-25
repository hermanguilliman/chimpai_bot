from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.services.repository import Repo
from tgbot.models.user import Users


async def user_start(m: Message, repo: Repo):
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
    await m.answer("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
