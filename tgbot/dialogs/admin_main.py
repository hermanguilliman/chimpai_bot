from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Back
from aiogram_dialog.widgets.input import MessageInput
from tgbot.models.aisettings import AISettings
from tgbot.services.repository import Repo
from tgbot.dialogs.openai_settings import Settings
from aiogram.types import CallbackQuery, ContentType, Message, ChatActions, ParseMode
from loguru import logger


class Main(StatesGroup):
    main = State()
    neural = State()


async def neural_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,):
    repo: Repo = manager.data['repo']
    openai = manager.data['openai']
    settings: AISettings = await repo.get_user_settings(message.from_id)
    
    prompt = message.text
    if message.reply_to_message:
        prompt = message.text + f'\n"{message.reply_to_message.text}"'
    
    await message.answer('<b>⌛️ Запрос отправлен. Ожидание ответа...</b>', parse_mode=ParseMode.HTML)
    await message.answer_chat_action(ChatActions.TYPING)

    try:
        if settings is not None:
            logger.debug('Создание запроса к нейросети')
            ai_text_answer = await openai.get_answer(
                api_key=settings.api_key,
                max_tokens=settings.max_tokens,
                model=settings.model,
                temperature=settings.temperature,
                prompt=prompt,
                )
        else:
            await message.answer('Настройки не найдены. Попробуйте выполнить /start')

        if ai_text_answer:
            """выдача успешного запроса"""
            await message.reply(ai_text_answer)
        else:
            await message.answer('Что-то пошло не так, ответ от OpenAI не получен')
    
    except:
        await message.answer('Ошибка получения ответа!')
        logger.error('Ошибка получения ответа!')
    

async def show_settings(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    """ Стартует диалог с настройками"""
    data = manager.current_context().dialog_data
    await manager.start(Settings.select, data=data)


async def get_main_data(repo: Repo, dialog_manager: DialogManager, **kwargs) -> dict:
    # Здесь происходит первичный запрос данных из команды запустившей диалог и бд 
    user_id:int = dialog_manager.bg().user.id
    full_name:str = dialog_manager.bg().user.full_name
    settings: AISettings = await repo.get_user_settings(user_id)
    chimpai:int = dialog_manager.current_context().dialog_data.get('chimpai', 'ChimpAI')

    base_view:dict = {
        'user_id': user_id,
        'chimpai': chimpai,
        'full_name': full_name,
        'api_key': '✅ Установлен' if settings.api_key else '❌ Отсутствует',
        'model': settings.model if settings.model else 'отсутствует',
        'max_length': settings.max_tokens if settings.max_tokens else '❌ Отсутствует',
        'temperature': settings.temperature if settings.temperature else '❌ Отсутствует',
    }

    # обновляем текущий контекст?
    dialog_manager.current_context().dialog_data.update(base_view)
    return base_view


main_dialog = Dialog(
    Window(
        # Главное окно
        Format("<b>{chimpai} 🐵 v0.2</b>\n"),
        Format('<b>Конфигурация:</b>\n{model} / max: {max_length} / temp: {temperature}'),
        Row(                
            SwitchTo(Const("🤖 Нейро-Чат"), id='neural', state=Main.neural),
            Button(Const("📝 Настройки"), id='settings', on_click=show_settings),
        ),
        state=Main.main,
        getter=get_main_data,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),
        Const("<b>🤖 Введите новый запрос:</b>"),
        Back(Const('↩️ Назад')),
        state=Main.neural,
        parse_mode=ParseMode.HTML,
    ),
)