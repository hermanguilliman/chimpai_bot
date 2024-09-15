from decimal import Decimal
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.services.repository import Repo


async def on_new_model_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение модели в бд по нажатию кнопки"""
    # Извлекаем сопоставление коротких id с полными названиями
    model_mapping = manager.dialog_data.get("model_mapping", {})

    # Находим полное название модели по короткому id
    full_model_name = model_mapping.get(
        item_id, item_id
    )  # Если не найдено, оставляем как есть

    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    await repo.update_settings(user_id=user_id, model=full_model_name)

    await callback.answer(f"Модель {full_model_name} успешно установлена!")
    await manager.done()


async def on_basic_personality_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение личности в бд по нажатию кнопки"""
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    await repo.select_basic_personality(user_id=user_id, name=item_id)
    await callback.answer(f"Выбрана личность: {item_id}!")
    await manager.done()


async def on_custom_personality_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение кастомной личности в бд по нажатию кнопки"""
    manager.dialog_data["custom_name"] = item_id
    await manager.next()


async def on_custom_personality_activate(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    name = manager.dialog_data.get("custom_name")
    await repo.set_custom_personality(user_id=user_id, name=name)
    await callback.answer(f"Выбрана личность:  {name}!")
    await manager.done()


async def on_custom_personality_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    name = manager.dialog_data.get("custom_name")
    await repo.delete_custom_personality(user_id=user_id, name=name)
    await callback.answer(f"Личность {name} удалена!")
    await manager.done()


async def on_max_length_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    await repo.update_max_token(user_id=user_id, max_tokens=item_id)
    await callback.answer(f"Новая длина ответа составляет {item_id} токенов")
    await manager.done()


# кнопка сброса значения температуры
async def on_reset_temp(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    manager.dialog_data["temperature"] = "0.7"


# кнопка увеличения значения температуры
async def on_increase_temp(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    maximum = Decimal("1.0")
    counter = Decimal(manager.dialog_data.get("temperature"))
    if counter >= maximum:
        await callback.answer("Больше нельзя!")
    else:
        manager.dialog_data["temperature"] = str(counter + Decimal("0.1"))


# кнопка уменьшения значения температуры
async def on_decrease_temp(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    minimal = Decimal("0")
    counter = Decimal(manager.dialog_data.get("temperature"))
    if counter <= minimal:
        await callback.answer("Меньше нельзя!")
    else:
        manager.dialog_data["temperature"] = str(counter - Decimal("0.1"))


async def on_temperature_selected(
    callback: ChatEvent, select: Any, manager: DialogManager
):
    # кнопка выбора температуры
    repo: Repo = manager.middleware_data.get("repo")
    user_id = manager.bg()._event_context.user.id
    temperature = manager.dialog_data.get("temperature")
    await repo.update_temperature(
        user_id=user_id, temperature=str(temperature)
    )
    await callback.answer(f"Задана температура: {temperature}")
    await manager.done()
