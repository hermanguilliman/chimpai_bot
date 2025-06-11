from decimal import Decimal
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.misc.states import TTSSettings
from tgbot.services.repository import Repo


async def on_tts_voice_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение модели в бд по нажатию кнопки"""
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    await repo.update_tts_voice(user_id=user_id, tts_voice=item_id)
    await callback.answer(f"Выбран голос {item_id}!")
    await manager.switch_to(state=TTSSettings.select)


async def on_tts_speed_selected(
    callback: ChatEvent, select: Any, manager: DialogManager
):
    # кнопка выбора температуры
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    tts_speed = manager.dialog_data.get("tts_speed")
    await repo.update_tts_speed(user_id=user_id, tts_speed=str(tts_speed))
    await callback.answer(f"Задана скорость речи: {tts_speed}")
    await manager.switch_to(state=TTSSettings.select)


async def on_increase_tts_speed(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    maximum = Decimal("4.0")
    counter = Decimal(manager.dialog_data.get("tts_speed"))
    if counter >= maximum:
        await callback.answer("Больше нельзя!")
    else:
        manager.dialog_data["tts_speed"] = str(counter + Decimal("0.1"))


async def on_big_increase_tts_speed(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    maximum = Decimal("4.0")
    counter = Decimal(manager.dialog_data.get("tts_speed"))
    if counter >= maximum:
        await callback.answer("Больше нельзя!")
    else:
        manager.dialog_data["tts_speed"] = str(counter + Decimal("0.5"))


async def on_decrease_tts_speed(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    minimal = Decimal("0.3")
    counter = Decimal(manager.dialog_data.get("tts_speed"))
    if counter <= minimal:
        await callback.answer("Меньше нельзя!")
    else:
        manager.dialog_data["tts_speed"] = str(counter - Decimal("0.1"))


async def on_big_decrease_tts_speed(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    minimal = Decimal("0.3")
    counter = Decimal(manager.dialog_data.get("tts_speed"))
    if counter <= minimal:
        await callback.answer("Меньше нельзя!")
    else:
        manager.dialog_data["tts_speed"] = str(counter - Decimal("0.5"))


async def on_reset_tts_speed(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    manager.dialog_data["tts_speed"] = "1.0"
