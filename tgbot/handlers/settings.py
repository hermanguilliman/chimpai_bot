import re
from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.input import MessageInput
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from typing import Any
from decimal import Decimal
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from tgbot.services.openai import OpenAIService
from aiogram_dialog.widgets.kbd import Button


async def api_key_handler(message: Message, message_input: MessageInput,
                       manager: DialogManager):

    user_id = manager.bg().user.id
    repo: Repo = manager.data['repo']
    dialog_data = manager.current_context().dialog_data
    new_api_key = message.text
    is_valid_key = bool(re.match('sk-[a-zA-Z0-9]{48}$', new_api_key))

    if not is_valid_key:
        await message.answer(
            f'⛔️ <b>Ошибка API ключа!</b>\n Подсказка: Ключ должен выглядеть как sk-...',
            parse_mode=ParseMode.HTML)
        await manager.done()
        return
        
    dialog_data["api_key"] = new_api_key
    await repo.update_user_api_key(user_id, new_api_key)
    await message.answer(f'<b>Новый API ключ успешно установлен!</b>', parse_mode=ParseMode.HTML)
    await manager.done()


async def on_new_model_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager,
                         item_id: str):
    """Обновляет значение модели в бд по нажатию кнопки"""
    repo: Repo = manager.data['repo']
    user_id = manager.bg().user.id
    await repo.update_user_settings_model(user_id=user_id, model=item_id)
    await callback.answer(f'Модель {item_id} успешно установлена!')
    await manager.done()


async def on_max_length_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager,
                         item_id: str):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    repo: Repo = manager.data['repo']
    user_id = manager.bg().user.id
    await repo.update_user_max_tokens(user_id=user_id, max_tokens=item_id)
    await callback.answer(f'Новая длина ответа составляет {item_id} токенов')
    await manager.done()


async def get_data_model_selector(openai: OpenAIService, dialog_manager: DialogManager, **kwargs):
    # Получаем список моделей доступных в OpenAI
    repo: Repo = dialog_manager.data['repo']
    settings: AISettings = await repo.get_user_settings(dialog_manager.bg().user.id)
    engines = await openai.get_engines(api_key=settings.api_key)
    engine_ids = [engine['id'] for engine in engines['data']]
    return {
        'models': engine_ids,
    }


async def on_temperature_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager):
    repo: Repo = manager.data['repo']
    user_id = manager.bg().user.id
    temperature = manager.current_context().dialog_data.get('temperature')
    await repo.update_temperature(user_id=user_id, temperature=str(temperature))
    await callback.answer(f'Задана температура: {temperature}')
    await manager.done()


# Геттер температуры
async def temp_getter(dialog_manager: DialogManager, **kwargs):
    # При первом запуске получаем значение из предыдущего диалога?
    dialog_data = dialog_manager.current_context().dialog_data
    if len(dialog_data)==0:
        dialog_manager.current_context().dialog_data.update(dialog_manager.current_context().start_data)
    return dialog_data
    

# кнопка сброса значения температуры
async def on_reset_temp(callback: CallbackQuery, button: Button,
                   manager: DialogManager):
    manager.current_context().dialog_data["temperature"] = '0.7'


# кнопка увеличения значения температуры
async def on_increase_temp(callback: CallbackQuery, button: Button,
                   manager: DialogManager):
    maximum = Decimal('1.0')
    counter = Decimal(manager.current_context().dialog_data.get("temperature"))
    if counter >= maximum:
        await callback.answer('Больше нельзя!')
    else:
        manager.current_context().dialog_data["temperature"] = str(counter + Decimal('0.1'))


# кнопка уменьшения значения температуры
async def on_decrease_temp(callback: CallbackQuery, button: Button,
                   manager: DialogManager):
    minimal = Decimal('0')
    counter = Decimal(manager.current_context().dialog_data.get("temperature"))
    if counter <= minimal:
        await callback.answer('Меньше нельзя!')
    else:
        manager.current_context().dialog_data["temperature"] = str(counter - Decimal('0.1'))


async def main_settings_getter(dialog_manager: DialogManager, **kwargs):
    dialog_manager.current_context().dialog_data.update(dialog_manager.current_context().start_data)
    return dialog_manager.current_context().dialog_data

