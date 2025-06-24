from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.misc.states import MainMenu
from tgbot.models.models import Users
from tgbot.services.repository.personalities import CustomPersonalityService
from tgbot.services.repository.users import UserService


async def admin_start_handler(
    m: Message,
    user_service: UserService,
    custom_personality_service: CustomPersonalityService,
    dialog_manager: DialogManager,
):
    user: Users | None = await user_service.get_user(m.from_user.id)
    if not user:
        # регистрация нового пользователя
        await user_service.add_user(
            user_id=m.from_user.id,
        )

    args = m.text.split()[1] if len(m.text.split()) > 1 else ""

    if args.startswith("share_"):
        token = args[6:]
        personality = await custom_personality_service.copy_custom_personality_by_shared_token(
            shared_token=token, new_user_id=m.from_user.id
        )
        if personality:
            await m.answer(
                f"✅ Личность «{personality.name}» успешно добавлена!"
            )
        else:
            await m.answer("❌ Личность не была добавлена")

    await dialog_manager.start(MainMenu.select, mode=StartMode.RESET_STACK)
