from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ContentType, ParseMode
from typing import Any
from decimal import Decimal
from aiogram_dialog import Dialog, DialogManager, Window, ChatEvent, Data
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Cancel, Select, SwitchTo, Group
from aiogram_dialog.widgets.input import MessageInput
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from tgbot.services.openai import OpenAIService


class Settings(StatesGroup):
    select = State()
    api_key = State()
    model = State()
    max_length = State()
    temperature = State()

async def api_key_handler(message: Message, message_input: MessageInput,
                       manager: DialogManager):

    user_id = manager.current_context().start_data['user_id']
    repo: Repo = manager.data['repo']
    dialog_data = manager.current_context().dialog_data
    new_api_key = message.text
    if len(new_api_key) != 51:
        await message.answer(
            f'⛔️ <b>Неправильная длина API ключа!</b> ⛔️\nКлюч должен состоять из 51 знака и начинается с sk-...',
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
    user_id = manager.current_context().start_data['user_id']
    await repo.update_user_settings_model(user_id=user_id, model=item_id)
    await callback.answer(f'Модель {item_id} успешно установлена!')
    await manager.done()


async def on_max_length_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager,
                         item_id: str):
    """Обновляет значение максимальной длины по нажатию кнопки"""
    repo: Repo = manager.data['repo']
    user_id = manager.current_context().start_data['user_id']
    await repo.update_user_max_tokens(user_id=user_id, max_tokens=item_id)
    await callback.answer(f'Новая длина ответа составляет {item_id} токенов')
    await manager.done()


async def get_data_model_selector(openai: OpenAIService, dialog_manager: DialogManager, **kwargs):
    # Получаем список моделей доступных в OpenAI
    engines = await openai.get_engines()
    engine_ids = [engine['id'] for engine in engines['data']]
    return {
        'models': engine_ids,
    }

async def on_temperature_selected(callback: ChatEvent, select: Any,
                         manager: DialogManager):
    repo: Repo = manager.data['repo']
    user_id = manager.current_context().start_data['user_id']
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


# Диалог настроек
settings_dialog = Dialog(
    Window(
        # Окно выбора настроек
        Const('<b>Выберите параметр, который хотели бы изменить:</b>'),
        Group(
        SwitchTo(Format('🔑 API ключ: {api_key}'), id='set_api_key', state=Settings.api_key, when='api_key'),
        SwitchTo(Format('🤖 Модель: {model}'), id='set_model', state=Settings.model, when='model'),
        SwitchTo(Format('🔋 Длина ответа: {max_length}'), id='set_max_length', state=Settings.max_length, when='max_length'),
        SwitchTo(Format('🌡️ Температура {temperature}'), id='set_temperature', state=Settings.temperature, when='temperature'),
        width=1),
        Cancel(Const('🤚 Отмена')),
        state=Settings.select,
        parse_mode=ParseMode.HTML,
        getter=main_settings_getter,
    ),
    Window(
        # Список доступных моделей
        MessageInput(api_key_handler, content_types=[ContentType.TEXT]),
        Const("<b>Укажите новый API ключ:</b>"),
        Cancel(Const('🤚 Отмена')),
        state=Settings.api_key,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        # Список доступных моделей
        Const("<b>Выберите модель из списка:</b>"),
        Group(
            Select(
                Format("🤖 {item}"),
                # нужно кинуть сюда список моделей
                items='models',
                item_id_getter=lambda x: x,
                id='select_max_new_model',
                on_click=on_new_model_selected,
            ),
            width=1,
        ),
        Cancel(Const('🤚 Отмена')),
        state=Settings.model,
        parse_mode=ParseMode.HTML,
        getter=get_data_model_selector,
    ),
    Window(
        # окно выбора максимального числа токенов на запрос,
        # для разных моделей диапазон отличается
        # например от 1 до 4000 для модели text-davinci-003
        Const("<b>Укажите максимальное число токенов расходуемое для ответа нейросети:</b>"),
        Group(
            Select(
                Format("🔋 {item}"),
                items=list(range(100, 4000+1, 100)),
                item_id_getter=lambda x: x,
                id='select_max_length',
                on_click=on_max_length_selected,
            ),
            width=5,
        ),
        Cancel(Const('🤚 Отмена')),
        state=Settings.max_length,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        # окно выбора температуры 
        # от 0.00 до 1.00 с двумя знаками после запятой
        Const("Выберите новое значение температуры и нажмите на градусник, чтобы подтвердить выбор. \nДопустимый диапазон значений от 0.0 до 1.0"),
        Group(
            Button(Format('🌡 Установить значение: {temperature}'), id='new_temperature', when='temperature', on_click=on_temperature_selected),
            width=1,
        ),
        Group(
            Button(Const('🔻 0.1'), id='decrease', on_click=on_decrease_temp),
            Button(Const('0.1 🔺'), id='increase', on_click=on_increase_temp),
            width=2,
        ),
        Group(
            Button(Const('🌚 Как было'), id='reset_temp', on_click=on_reset_temp),
            Cancel(Const('🤚 Отмена')),
            width=2,
            
        ),
        state=Settings.temperature,
        parse_mode=ParseMode.HTML,
        getter=temp_getter,
    ),
)