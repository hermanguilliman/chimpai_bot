from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Back
from aiogram_dialog.widgets.input import MessageInput
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from tgbot.dialogs.settings import Settings
from aiogram.types import CallbackQuery, ContentType, Message, ChatActions, ParseMode
from loguru import logger

class Main(StatesGroup):
    main = State()
    neural = State()


async def neural_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager):
    repo: Repo = manager.data['repo']
    openai = manager.data['openai']
    settings: AISettings = await repo.get_user_settings(message.from_id)
    await message.answer_chat_action(ChatActions.TYPING)
    try:
        if settings is not None:
            logger.debug('Создание запроса к нейросети')
            ai_text_answer = await openai.get_answer(
                api_key=settings.api_key,
                max_tokens=settings.max_tokens,
                model=settings.model,
                temperature=settings.temperature,
                prompt=message.text,
                )
        else:
            await message.answer('Настройки не найдены. Попробуйте выполнить /start')

        if ai_text_answer is not None:
            await message.answer(ai_text_answer)
        else:
            await message.answer('Что-то пошло не так, сообщение от AI не получено')
    
    except:
        logger.error('Ошибка получения запроса!')
    
            


async def show_settings(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    """ Стартует диалог с настройками"""
    data = manager.current_context().dialog_data
    await manager.start(Settings.select, data=data)


async def get_main_data(repo: Repo, dialog_manager: DialogManager, **kwargs) -> dict:
    # Здесь происходит первичный запрос данных из команды запустившей диалог и бд 
    start_data = dialog_manager.current_context().start_data
    user_id:int = start_data.get('user_id')
    full_name:str = start_data.get('full_name')
    settings: AISettings = await repo.get_user_settings(user_id)

    if settings is None:
        base_view:dict = {
        'user_id': user_id,
        'full_name': full_name,
        'api_key': 'Error',
        'model': 'Error',
        'max_length': 'Error',
        'temperature': 'Error',
    }
    else:
        base_view:dict = {
            'user_id': user_id,
            'full_name': full_name,
            'api_key': '...' + settings.api_key[-10:] if settings.api_key else 'не установлен',
            'model': settings.model,
            'max_length': settings.max_tokens,
            'temperature': settings.temperature,
        }

    # обновляем текущий контекст?
    dialog_manager.current_context().dialog_data.update(base_view)
    return base_view


main_dialog = Dialog(
    Window(
        # Главное окно
        Const("<b>ChimpAI 🐵 [v0.2]</b>"),
        # Format("Привет, <b>{full_name}</b>!\n", when='full_name'),
        # Format("🔑 API ключ: <b>{api_key}</b>", when='api_key'),
        # Format("🤖 Выбрана модель: <b>{model}</b>", when='model'),
        # Format("🔋 Длина ответа: <b>{max_length}</b>", when='max_length'),
        # Format("🌡 Температура: <b>{temperature}</b>", when='temperature'),
        Row(                
            SwitchTo(Const("🤖 НейроЧат"), id='neural', state=Main.neural),
            Button(Const("📝 Параметры"), id='settings', on_click=show_settings),
        ),
        state=Main.main,
        getter=get_main_data,
        parse_mode=ParseMode.HTML,
        preview_data={
            'full_name':'братик',
        }
    ),
    Window(
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),

        Const("<b>🤖 Введите запрос для нейросети:</b>"),
        Back(Const('Вернуться')),
        state=Main.neural,
        parse_mode=ParseMode.HTML,
    )
)