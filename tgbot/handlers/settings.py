from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.dialogs.main import Main
from aiogram_dialog import DialogManager, StartMode

async def admin_settings(m: Message, dialog_manager: DialogManager):
    data = {
        "full_name" : m.from_user.full_name,
        "user_id" : m.from_user.id,
    }
    # точка входа в основной диалог
    await dialog_manager.start(Main.main, mode=StartMode.RESET_STACK, data=data)


def register_admin_settings(dp: Dispatcher):
    dp.register_message_handler(
        admin_settings, 
        commands=["settings"], 
        state="*", 
        is_admin=True
        )
