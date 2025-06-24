from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.services.repository import Repo


async def toggle_summary_type(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    settings = await repo.get_settings(user_id)

    # Переключаем формат
    new_type = (
        "short"
        if settings.summary_settings.summary_type == "detailed"
        else "detailed"
    )
    await repo.update_summary_type(user_id, type=new_type)

    # Обновляем данные диалога
    manager.dialog_data["summary_type"] = new_type
    await callback.answer(f"Формат экспорта изменён на {new_type}")
    await manager.update({})
