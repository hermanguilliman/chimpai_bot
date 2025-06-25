from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.services.repository.settings import SettingsService


async def toggle_summary_type(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    user_id = callback.from_user.id
    settings = await settings_service.get_settings(user_id)

    # Переключаем формат
    new_type = (
        "short"
        if settings.summary_settings.summary_type == "detailed"
        else "detailed"
    )
    await settings_service.update_summary_type(user_id, type=new_type)

    # Обновляем данные диалога
    manager.dialog_data["summary_type"] = new_type
    if new_type == "short":
        await callback.answer("Формат экспорта изменён на краткий")
    else:
        await callback.answer("Формат экспорта изменён на подробный")
    await manager.update({})


async def on_delete_summary_api_key(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    user_id = callback.from_user.id
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    await settings_service.delete_summary_api_key(user_id)
    await callback.answer("API ключ Пересказчика удалён. Сервис отключен.")
    await manager.done()
