from decimal import Decimal
from typing import Any

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.misc.states import NeuralChatSettings, PersonalitySettings
from tgbot.services.repository.api_urls import BaseUrlService
from tgbot.services.repository.personalities import (
    BasicPersonalityService,
    CustomPersonalityService,
)
from tgbot.services.repository.settings import SettingsService


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

    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    user_id = callback.from_user.id
    await settings_service.update_settings(
        user_id=user_id, model=full_model_name
    )

    await callback.answer(f"Модель {full_model_name} успешно установлена!")
    await manager.switch_to(state=NeuralChatSettings.select)


async def on_basic_personality_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение личности в бд по нажатию кнопки"""
    basic_personality_service: BasicPersonalityService = (
        manager.middleware_data.get("basic_personality_service")
    )
    user_id = callback.from_user.id
    await basic_personality_service.select_basic_personality(
        user_id=user_id, name=item_id
    )
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
    custom_personality_service: CustomPersonalityService = (
        manager.middleware_data.get("custom_personality_service")
    )
    user_id = callback.from_user.id
    name = manager.dialog_data.get("custom_name")
    await custom_personality_service.set_custom_personality(
        user_id=user_id, name=name
    )
    await callback.answer(f"Выбрана личность:  {name}!")
    await manager.done()


async def on_custom_personality_delete_confirm(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    custom_personality_service: CustomPersonalityService = (
        manager.middleware_data.get("custom_personality_service")
    )
    user_id = callback.from_user.id
    name = manager.dialog_data.get("custom_name")
    await custom_personality_service.delete_custom_personality(
        user_id=user_id, name=name
    )
    await callback.message.answer(
        f'♻️ Личность "<b>{name}</b>" удалена!', parse_mode=ParseMode.HTML
    )
    await manager.switch_to(PersonalitySettings.custom_list)


async def on_max_length_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    user_id = callback.from_user.id
    await settings_service.update_max_token(
        user_id=user_id, max_tokens=item_id
    )
    await callback.answer(f"Новая длина ответа составляет {item_id} токенов")
    await manager.switch_to(state=NeuralChatSettings.select)


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
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    user_id = callback.from_user.id
    temperature = manager.dialog_data.get("temperature")
    await settings_service.update_temperature(
        user_id=user_id, temperature=str(temperature)
    )
    await callback.answer(f"Задана температура: {temperature}")
    await manager.switch_to(state=NeuralChatSettings.select)


async def on_clear_search_query(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    manager.dialog_data.pop("search_query", None)


async def on_base_url_selected(
    callback: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    base_url_service: BaseUrlService = manager.middleware_data.get(
        "base_url_service"
    )
    user_id = callback.from_user.id
    await base_url_service.set_chat_base_url(user_id=user_id, name=item_id)
    await callback.answer(f"Выбран API: {item_id}!")
    await manager.done()


async def toggle_export_format(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    user_id = callback.from_user.id
    settings = await settings_service.get_settings(user_id)

    # Переключаем формат
    new_format = (
        "html"
        if settings.chat_settings.export_format == "markdown"
        else "markdown"
    )
    await settings_service.update_chat_export_format(
        user_id, export_format=new_format
    )

    # Обновляем данные диалога
    manager.dialog_data["export_format"] = new_format
    await callback.answer(f"Формат экспорта изменён на {new_format.upper()}")
    await manager.update({})


async def on_delete_chat_api_key(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    user_id = callback.from_user.id
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    await settings_service.delete_chat_api_key(user_id)
    await callback.answer("API ключ чата удалён. Сервис отключен.")
    await manager.done()


async def on_share_personality(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    user_id = callback.from_user.id
    personality_name = manager.dialog_data.get("custom_name")
    custom_personality_service: CustomPersonalityService = (
        manager.middleware_data.get("custom_personality_service")
    )
    personality = await custom_personality_service.get_custom_personality(
        user_id=user_id, personality_name=personality_name
    )

    if not personality.shared_token:
        shared_token = await custom_personality_service.generate_shared_token(
            user_id=user_id, personality_name=personality_name
        )
    else:
        shared_token = personality.shared_token

    share_link = f"https://t.me/chimpaibot?start=share_{shared_token}"
    await callback.message.answer(
        f"📩 <b>Личность {personality.name} доступна по ссылке:</b>\n{share_link}",
        parse_mode=ParseMode.HTML,
    )
