from decimal import Decimal
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.misc.personality import personality_base
from tgbot.services.repository import Repo


async def on_new_model_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение модели в бд по нажатию кнопки"""
    repo: Repo = manager.data["repo"]
    user_id = manager.bg().user.id
    await repo.update_settings(user_id=user_id, model=item_id)
    await callback.answer(f"Модель {item_id} успешно установлена!")
    await manager.done()


async def on_new_personality_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение личности в бд по нажатию кнопки"""
    repo: Repo = manager.data["repo"]
    user_id = manager.bg().user.id
    personality = await repo.get_personality(user_id=user_id)

    for person in personality_base:
        if person["person"] == item_id:
            text = person["message"]

            if not personality:
                await repo.add_new_personality(user_id=user_id, name=item_id, text=text)
            else:
                await repo.update_personality(user_id=user_id, name=item_id, text=text)

    await callback.answer(f"Выбрана личность: {item_id}!")
    await manager.done()


async def on_max_length_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    repo: Repo = manager.data["repo"]
    user_id = manager.bg().user.id
    await repo.update_max_token(user_id=user_id, max_tokens=item_id)
    await callback.answer(f"Новая длина ответа составляет {item_id} токенов")
    await manager.done()


# кнопка сброса значения температуры
async def on_reset_temp(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    manager.current_context().dialog_data["temperature"] = "0.7"


# кнопка увеличения значения температуры
async def on_increase_temp(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    maximum = Decimal("1.0")
    counter = Decimal(manager.current_context().dialog_data.get("temperature"))
    if counter >= maximum:
        await callback.answer("Больше нельзя!")
    else:
        manager.current_context().dialog_data["temperature"] = str(
            counter + Decimal("0.1")
        )


# кнопка уменьшения значения температуры
async def on_decrease_temp(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    minimal = Decimal("0")
    counter = Decimal(manager.current_context().dialog_data.get("temperature"))
    if counter <= minimal:
        await callback.answer("Меньше нельзя!")
    else:
        manager.current_context().dialog_data["temperature"] = str(
            counter - Decimal("0.1")
        )


async def on_temperature_selected(
    callback: ChatEvent, select: Any, manager: DialogManager
):
    # кнопка выбора температуры
    repo: Repo = manager.data["repo"]
    user_id = manager.bg().user.id
    temperature = manager.current_context().dialog_data.get("temperature")
    await repo.update_temperature(user_id=user_id, temperature=str(temperature))
    await callback.answer(f"Задана температура: {temperature}")
    await manager.done()
